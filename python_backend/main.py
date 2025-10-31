from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import os
import logging
import json

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

# Initialize orchestrator based on AWS availability
orchestrator = None
aws_clients = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global orchestrator, aws_clients
    
    # Load generated data
    logger.info("📊 Loading generated MSP data...")
    try:
        # Try different paths
        import os
        possible_paths = [
            'generated_data.json',
            'python_backend/generated_data.json',
            os.path.join(os.path.dirname(__file__), 'generated_data.json')
        ]
        
        data_store = None
        for path in possible_paths:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    data_store = json.load(f)
                logger.info(f"✅ Loaded {data_store['summary']['total_records']:,} records from {path}")
                break
        
        if data_store is None:
            raise FileNotFoundError("Could not find generated_data.json")
            
    except FileNotFoundError as e:
        logger.warning(f"⚠️  Generated data not found: {e}")
        logger.info("📊 Generating data on-the-fly...")
        from data_generator import MSPDataGenerator
        generator = MSPDataGenerator()
        data_store = generator.generate_all_data()
    
    # Startup
    if use_bedrock:
        logger.info("🚀 Starting Autonomous MSP AI System with AWS Bedrock...")
        try:
            from aws_config import get_aws_clients
            from agents.bedrock_agents import BedrockAgentOrchestrator
            
            aws_clients = get_aws_clients()
            
            # Test AWS connection
            logger.info("🔍 Testing AWS connection...")
            connection_test = aws_clients.test_connection()
            logger.info(f"✅ AWS Connection Status: {connection_test}")
            
            # Initialize Bedrock orchestrator
            orchestrator = BedrockAgentOrchestrator(aws_clients, data_store)
            logger.info("✅ AWS Bedrock Agent Orchestrator initialized!")
            logger.info(f"🤖 Managing {len(data_store['servers'])} servers across {len(data_store['clients'])} clients")
            
        except Exception as e:
            logger.error(f"❌ Error initializing AWS Bedrock: {e}")
            logger.info("⚠️  Falling back to simulation mode")
            from agents.strands_orchestrator import StrandsAgentOrchestrator
            orchestrator = StrandsAgentOrchestrator(use_bedrock=False)
    else:
        logger.info("🚀 Starting Autonomous MSP AI System in simulation mode...")
        logger.info("💡 Configure AWS credentials to enable Bedrock integration")
        from agents.strands_orchestrator import StrandsAgentOrchestrator
        orchestrator = StrandsAgentOrchestrator(use_bedrock=False)
    
    # Make orchestrator available to routes via app state
    app.state.orchestrator = orchestrator
    app.state.use_bedrock = use_bedrock
    
    # Start background tasks
    asyncio.create_task(run_autonomous_workflows())
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
    if use_bedrock and hasattr(orchestrator, 'data'):
        return {
            "service": "MSP AI Orchestrator",
            "framework": "AWS Bedrock Agents + Claude 3.5 Sonnet",
            "status": "operational",
            "bedrock_enabled": True,
            "aws_region": os.getenv("AWS_DEFAULT_REGION"),
            "agents": 8,
            "data_records": orchestrator.data.get('summary', {}).get('total_records', 0),
            "servers_monitored": len(orchestrator.data.get('servers', [])),
            "clients_managed": len(orchestrator.data.get('clients', [])),
            "version": "3.0.0 - Production"
        }
    else:
        return {
            "service": "MSP AI Orchestrator",
            "framework": "Simulation Mode",
            "status": "operational",
            "bedrock_enabled": False,
            "agents": orchestrator.get_agent_count() if hasattr(orchestrator, 'get_agent_count') else 8,
            "version": "3.0.0 - Simulation"
        }

@app.get("/api/health")
async def health():
    health_status = {
        "status": "healthy",
        "bedrock_enabled": use_bedrock,
        "orchestrator_active": orchestrator is not None
    }
    
    if use_bedrock and aws_clients:
        try:
            connection_test = aws_clients.test_connection()
            health_status["aws_services"] = connection_test['services']
        except Exception as e:
            health_status["aws_error"] = str(e)
    
    return health_status

@app.get("/api/status")
async def get_status():
    """Get complete system status"""
    if use_bedrock and hasattr(orchestrator, 'get_agent_status'):
        return {
            "agents": orchestrator.get_agent_status(),
            "recent_decisions": orchestrator.get_recent_decisions(10),
            "predictions": [],
            "metrics": orchestrator.get_performance_metrics()
        }
    else:
        return {
            "agents": orchestrator.get_agent_statuses(),
            "recent_decisions": orchestrator.decisions_log[:10],
            "predictions": orchestrator.get_latest_predictions(),
            "metrics": orchestrator.get_current_metrics()
        }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    logger.info(f"✅ WebSocket client connected. Total connections: {len(manager.active_connections)}")
    try:
        # Keep connection alive - just wait for messages or disconnect
        while True:
            await asyncio.sleep(1)  # Keepalive - prevents tight loop
            # broadcast_updates() will send data to all connections
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.info(f"❌ WebSocket client disconnected. Total connections: {len(manager.active_connections)}")

async def run_autonomous_workflows():
    """Run autonomous agent workflows continuously"""
    await asyncio.sleep(5)  # Wait for startup
    
    while True:
        try:
            if use_bedrock and hasattr(orchestrator, 'execute_autonomous_workflow'):
                logger.info("🤖 Executing autonomous workflow...")
                result = await orchestrator.execute_autonomous_workflow()
                logger.info(f"✅ Workflow completed: {result.get('workflow_id')}")
            
            await asyncio.sleep(30)  # Run every 30 seconds
        except Exception as e:
            logger.error(f"Error in autonomous workflow: {e}")
            await asyncio.sleep(10)

async def broadcast_updates():
    """Broadcast real-time updates to all connected clients"""
    while True:
        await asyncio.sleep(3)  # Send updates every 3 seconds
        
        try:
            if use_bedrock and hasattr(orchestrator, 'get_agent_status'):
                # AWS Bedrock mode
                update = {
                    "type": "system_update",
                    "timestamp": datetime.now().isoformat(),
                    "agents": orchestrator.get_agent_status(),
                    "recent_decision": orchestrator.get_recent_decisions(1)[0] if orchestrator.get_recent_decisions(1) else None,
                    "predictions": [],  # Will be populated by workflows
                    "metrics": orchestrator.get_performance_metrics()
                }
            else:
                # Simulation mode
                update = {
                    "type": "system_update",
                    "timestamp": orchestrator.get_current_time(),
                    "agents": orchestrator.get_agent_statuses(),
                    "recent_decision": orchestrator.get_latest_decision(),
                    "predictions": orchestrator.get_latest_predictions(3),
                    "metrics": orchestrator.get_current_metrics()
                }
            
            await manager.broadcast(update)
        except Exception as e:
            logger.error(f"Error broadcasting updates: {e}")

from datetime import datetime

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
