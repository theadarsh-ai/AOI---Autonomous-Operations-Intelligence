import express, { type Request, Response, NextFunction } from "express";
import { registerRoutes } from "./routes";
import { setupVite, serveStatic, log } from "./vite";
import { spawn } from "child_process";
import http from "http";

const app = express();

// Start Python backend automatically
let pythonBackend: ReturnType<typeof spawn> | null = null;

function startPythonBackend() {
  log("🐍 Starting Python FastAPI backend on port 8000...");
  
  pythonBackend = spawn("python", ["-u", "run_backend.py"], {
    stdio: ["ignore", "pipe", "pipe"],
    detached: false,
  });

  pythonBackend.stdout?.on("data", (data) => {
    const output = data.toString().trim();
    if (output) {
      console.log(`[Python Backend] ${output}`);
    }
  });

  pythonBackend.stderr?.on("data", (data) => {
    const output = data.toString().trim();
    if (output && !output.includes("WARNING")) {
      console.error(`[Python Backend Error] ${output}`);
    }
  });

  pythonBackend.on("close", (code) => {
    if (code !== null && code !== 0) {
      console.error(`[Python Backend] Process exited with code ${code}`);
    }
  });

  log("✅ Python backend started");
}

// Cleanup on exit
process.on("SIGINT", () => {
  log("🛑 Shutting down services...");
  if (pythonBackend) {
    pythonBackend.kill("SIGTERM");
  }
  process.exit(0);
});

process.on("SIGTERM", () => {
  if (pythonBackend) {
    pythonBackend.kill("SIGTERM");
  }
  process.exit(0);
});

// Start Python backend
startPythonBackend();

declare module 'http' {
  interface IncomingMessage {
    rawBody: unknown
  }
}
app.use(express.json({
  verify: (req, _res, buf) => {
    req.rawBody = buf;
  }
}));
app.use(express.urlencoded({ extended: false }));

// Proxy REST API requests to Python backend on port 8000
app.use('/api', (req, res, next) => {
  // Add trailing slash if not present (FastAPI expects trailing slashes)
  let url = req.url;
  if (!url.includes('?') && !url.endsWith('/')) {
    url += '/';
  }
  const path = `/api${url}`;
  log(`[API Proxy] ${req.method} ${path}`);
  
  const options = {
    hostname: 'localhost',
    port: 8000,
    path: path,
    method: req.method,
    headers: {
      'Content-Type': 'application/json',
    },
  };

  const proxyReq = http.request(options, (proxyRes) => {
    let data = '';
    
    proxyRes.on('data', (chunk) => {
      data += chunk;
    });
    
    proxyRes.on('end', () => {
      try {
        const jsonData = JSON.parse(data);
        res.status(proxyRes.statusCode || 200).json(jsonData);
      } catch (error) {
        console.error('[API Proxy] JSON parse error:', error);
        res.status(500).json({ error: 'Failed to parse backend response' });
      }
    });
  });

  proxyReq.on('error', (error) => {
    console.error('[API Proxy] Request error:', error);
    res.status(500).json({ error: 'Backend connection failed' });
  });

  if (req.method !== 'GET' && req.method !== 'HEAD' && req.body) {
    proxyReq.write(JSON.stringify(req.body));
  }

  proxyReq.end();
});

app.use((req, res, next) => {
  const start = Date.now();
  const path = req.path;
  let capturedJsonResponse: Record<string, any> | undefined = undefined;

  const originalResJson = res.json;
  res.json = function (bodyJson, ...args) {
    capturedJsonResponse = bodyJson;
    return originalResJson.apply(res, [bodyJson, ...args]);
  };

  res.on("finish", () => {
    const duration = Date.now() - start;
    if (path.startsWith("/api")) {
      let logLine = `${req.method} ${path} ${res.statusCode} in ${duration}ms`;
      if (capturedJsonResponse) {
        logLine += ` :: ${JSON.stringify(capturedJsonResponse)}`;
      }

      if (logLine.length > 80) {
        logLine = logLine.slice(0, 79) + "…";
      }

      log(logLine);
    }
  });

  next();
});

(async () => {
  const server = await registerRoutes(app);

  app.use((err: any, _req: Request, res: Response, _next: NextFunction) => {
    const status = err.status || err.statusCode || 500;
    const message = err.message || "Internal Server Error";

    res.status(status).json({ message });
    throw err;
  });

  // importantly only setup vite in development and after
  // setting up all the other routes so the catch-all route
  // doesn't interfere with the other routes
  if (app.get("env") === "development") {
    await setupVite(app, server);
  } else {
    serveStatic(app);
  }

  // ALWAYS serve the app on the port specified in the environment variable PORT
  // Other ports are firewalled. Default to 5000 if not specified.
  // this serves both the API and the client.
  // It is the only port that is not firewalled.
  const port = parseInt(process.env.PORT || '5000', 10);
  server.listen({
    port,
    host: "0.0.0.0",
    reusePort: true,
  }, () => {
    log(`serving on port ${port}`);
  });
})();
