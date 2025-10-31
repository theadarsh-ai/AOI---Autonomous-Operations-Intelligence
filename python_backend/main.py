from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import os
import logging

from agents.strands_orchestrator import StrandsAgentOrchestrator
from agents.websocket_manager import ConnectionManager
from routes import agents, decisions, predictions, metrics

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

manager = ConnectionManager()

# Check if AWS credentials are configured for Bedrock
use_bedrock = all([
    os.getenv("AWS_ACCESS_KEY_ID"),
    os.getenv("AWS_SECRET_ACCESS_KEY"),
    os.getenv("AWS_DEFAULT_REGION")
])

orchestrator = StrandsAgentOrchestrator(use_bedrock=use_bedrock)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    if use_bedrock:
        logger.info("🚀 Starting Autonomous MSP AI System with AWS Bedrock + Strands Agents...")
    else:
        logger.info("🚀 Starting Autonomous MSP AI System in simulation mode...")
        logger.info("💡 Configure AWS credentials to enable Bedrock integration")
    
    asyncio.create_task(orchestrator.run())
    asyncio.create_task(broadcast_updates())
    yield
    # Shutdown
    logger.info("🛑 Shutting down Autonomous MSP AI System...")

app = FastAPI(
    title="MSP AI Orchestrator - Strands Agents + AWS Bedrock",
    description="Autonomous Multi-Agent Management System powered by Strands Agents framework",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
        "framework": "Strands Agents + AWS Bedrock",
        "status": "operational",
        "bedrock_enabled": use_bedrock,
        "agents": orchestrator.get_agent_count(),
        "version": "2.0.0"
    }

@app.get("/api/health")
async def health():
    return {
        "status": "healthy",
        "orchestrator": orchestrator.is_running(),
        "bedrock_enabled": use_bedrock,
        "framework": "Strands Agents"
    }

@app.get("/api/status")
async def get_status():
    """Get complete system status"""
    return {
        "agents": orchestrator.get_agent_statuses(),
        "recent_decisions": orchestrator.decisions_log[:10],
        "predictions": orchestrator.get_latest_predictions(),
        "metrics": orchestrator.get_current_metrics()
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"Received from client: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info("Client disconnected")

async def broadcast_updates():
    """Broadcast real-time updates to all connected clients"""
    while True:
        await asyncio.sleep(3)  # Send updates every 3 seconds
        
        update = {
            "type": "system_update",
            "timestamp": orchestrator.get_current_time(),
            "agents": orchestrator.get_agent_statuses(),
            "recent_decision": orchestrator.get_latest_decision(),
            "predictions": orchestrator.get_latest_predictions(3),
            "metrics": orchestrator.get_current_metrics()
        }
        
        await manager.broadcast(update)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
