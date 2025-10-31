from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from typing import List
import logging

from agents.orchestrator import AgentOrchestrator
from agents.websocket_manager import ConnectionManager
from routes import agents, decisions, predictions, metrics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

manager = ConnectionManager()
orchestrator = AgentOrchestrator()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start the autonomous agent system
    logger.info("🚀 Starting Autonomous MSP AI System...")
    asyncio.create_task(orchestrator.run())
    asyncio.create_task(broadcast_updates())
    yield
    # Shutdown
    logger.info("🛑 Shutting down Autonomous MSP AI System...")

app = FastAPI(
    title="MSP AI Orchestrator",
    description="Autonomous Multi-Agent Management System powered by AWS Bedrock",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5000", "http://0.0.0.0:5000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agents.router, prefix="/api/agents", tags=["agents"])
app.include_router(decisions.router, prefix="/api/decisions", tags=["decisions"])
app.include_router(predictions.router, prefix="/api/predictions", tags=["predictions"])
app.include_router(metrics.router, prefix="/api/metrics", tags=["metrics"])

@app.get("/")
async def root():
    return {
        "service": "MSP AI Orchestrator",
        "status": "operational",
        "agents": orchestrator.get_agent_count(),
        "version": "1.0.0"
    }

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "orchestrator": orchestrator.is_running(),
        "active_agents": orchestrator.get_active_agents_count()
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            # Keep connection alive and receive any client messages
            data = await websocket.receive_text()
            logger.info(f"Received from client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected")

async def broadcast_updates():
    """Broadcast real-time updates to all connected clients"""
    while True:
        await asyncio.sleep(2)  # Send updates every 2 seconds
        
        # Get latest data from orchestrator
        update = {
            "type": "system_update",
            "timestamp": orchestrator.get_current_time(),
            "agents": orchestrator.get_agent_statuses(),
            "recent_decision": orchestrator.get_latest_decision(),
            "metrics": orchestrator.get_current_metrics()
        }
        
        await manager.broadcast(update)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
