import type { Express } from "express";
import { createServer, type Server } from "http";
import { storage } from "./storage";
import { WebSocketServer, WebSocket } from "ws";

export async function registerRoutes(app: Express): Promise<Server> {
  // put application routes here
  // prefix all routes with /api

  // use storage to perform CRUD operations on the storage interface
  // e.g. storage.insertUser(user) or storage.getUserByUsername(username)

  const httpServer = createServer(app);

  // Set up WebSocket proxy to Python backend on port 8000
  const wss = new WebSocketServer({ noServer: true });

  httpServer.on('upgrade', (request, socket, head) => {
    console.log(`[WebSocket] Upgrade request received for: ${request.url}`);
    
    // Only handle /ws WebSocket connections
    if (request.url === '/ws') {
      console.log('[WebSocket] Handling /ws upgrade...');
      
      wss.handleUpgrade(request, socket, head, (ws) => {
        console.log('[WebSocket Proxy] Frontend client connected, connecting to Python backend...');
        
        // Create connection to Python backend
        const backendWs = new WebSocket('ws://0.0.0.0:8000/ws');

        backendWs.on('open', () => {
          console.log('[WebSocket Proxy] ✅ Connected to Python backend');
        });

        // Forward messages from Python backend to frontend
        backendWs.on('message', (data) => {
          if (ws.readyState === WebSocket.OPEN) {
            ws.send(data);
          }
        });

        // Forward messages from frontend to Python backend
        ws.on('message', (data) => {
          if (backendWs.readyState === WebSocket.OPEN) {
            backendWs.send(data);
          }
        });

        // Handle disconnections
        ws.on('close', () => {
          console.log('[WebSocket Proxy] Frontend disconnected');
          if (backendWs.readyState === WebSocket.OPEN) {
            backendWs.close();
          }
        });

        backendWs.on('close', () => {
          console.log('[WebSocket Proxy] Backend disconnected');
          if (ws.readyState === WebSocket.OPEN) {
            ws.close();
          }
        });

        backendWs.on('error', (error) => {
          console.error('[WebSocket Proxy] Backend error:', error.message);
          if (ws.readyState === WebSocket.OPEN) {
            ws.close();
          }
        });

        ws.on('error', (error) => {
          console.error('[WebSocket Proxy] Frontend error:', error.message);
          if (backendWs.readyState === WebSocket.OPEN) {
            backendWs.close();
          }
        });
      });
    } else {
      console.log(`[WebSocket] Ignoring upgrade for: ${request.url}`);
      socket.destroy();
    }
  });

  return httpServer;
}
