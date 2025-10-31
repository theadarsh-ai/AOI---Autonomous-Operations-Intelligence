/**
 * WebSocket connection manager for real-time updates from Python backend
 */

type WebSocketMessage = {
  type: string;
  timestamp: string;
  agents?: any[];
  recent_decision?: any;
  predictions?: any[];
  metrics?: any;
};

type MessageHandler = (message: WebSocketMessage) => void;
type ConnectionHandler = (connected: boolean) => void;

class WebSocketManager {
  private ws: WebSocket | null = null;
  private reconnectTimer: NodeJS.Timeout | null = null;
  private handlers: Set<MessageHandler> = new Set();
  private connectionHandlers: Set<ConnectionHandler> = new Set();
  private url: string;
  private reconnectAttempts = 0;
  private maxReconnectAttempts = 10;

  constructor(url: string = "ws://localhost:5000/ws") {
    this.url = url;
  }

  connect() {
    if (this.ws?.readyState === WebSocket.OPEN) {
      console.log("WebSocket already connected");
      return;
    }

    console.log(`Connecting to WebSocket: ${this.url}`);
    
    try {
      this.ws = new WebSocket(this.url);

      this.ws.onopen = () => {
        console.log("✅ WebSocket connected to Python backend");
        this.reconnectAttempts = 0;
        this.notifyConnectionChange(true);
      };

      this.ws.onmessage = (event) => {
        try {
          const message: WebSocketMessage = JSON.parse(event.data);
          this.handlers.forEach(handler => handler(message));
        } catch (error) {
          console.error("Failed to parse WebSocket message:", error);
        }
      };

      this.ws.onerror = (error) => {
        console.error("WebSocket error:", error);
      };

      this.ws.onclose = () => {
        console.log("WebSocket disconnected");
        this.ws = null;
        this.notifyConnectionChange(false);
        this.scheduleReconnect();
      };
    } catch (error) {
      console.error("Failed to create WebSocket connection:", error);
      this.scheduleReconnect();
    }
  }

  private scheduleReconnect() {
    if (this.reconnectTimer) {
      return;
    }

    if (this.reconnectAttempts >= this.maxReconnectAttempts) {
      console.log("Max reconnect attempts reached. Stopping reconnection.");
      return;
    }

    const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
    this.reconnectAttempts++;

    console.log(`Reconnecting in ${delay}ms... (attempt ${this.reconnectAttempts}/${this.maxReconnectAttempts})`);

    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null;
      this.connect();
    }, delay);
  }

  disconnect() {
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer);
      this.reconnectTimer = null;
    }

    if (this.ws) {
      this.ws.close();
      this.ws = null;
    }

    this.handlers.clear();
    this.connectionHandlers.clear();
  }

  subscribe(handler: MessageHandler) {
    this.handlers.add(handler);
    return () => this.handlers.delete(handler);
  }

  onConnectionChange(handler: ConnectionHandler) {
    this.connectionHandlers.add(handler);
    // Immediately notify of current state
    handler(this.isConnected());
    return () => this.connectionHandlers.delete(handler);
  }

  private notifyConnectionChange(connected: boolean) {
    this.connectionHandlers.forEach(handler => handler(connected));
  }

  send(data: any) {
    if (this.ws?.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    } else {
      console.warn("WebSocket not connected, message not sent");
    }
  }

  isConnected(): boolean {
    return this.ws?.readyState === WebSocket.OPEN;
  }
}

// Singleton instance
export const wsManager = new WebSocketManager();

// Auto-connect when module loads
if (typeof window !== "undefined") {
  wsManager.connect();
}
