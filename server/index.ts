import express, { type Request, Response, NextFunction } from "express";
import { registerRoutes } from "./routes";
import { setupVite, serveStatic, log } from "./vite";
import { spawn } from "child_process";

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
app.use('/api', async (req, res, next) => {
  try {
    const url = `http://localhost:8000${req.url}`;
    const response = await fetch(url, {
      method: req.method,
      headers: {
        'Content-Type': 'application/json',
        ...(req.headers as Record<string, string>),
      },
      body: req.method !== 'GET' && req.method !== 'HEAD' ? JSON.stringify(req.body) : undefined,
    });

    const data = await response.json();
    res.status(response.status).json(data);
  } catch (error) {
    console.error('[API Proxy] Error:', error);
    next(error);
  }
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
