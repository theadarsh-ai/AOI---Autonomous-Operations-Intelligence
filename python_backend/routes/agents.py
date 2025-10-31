from fastapi import APIRouter, Request
from typing import List, Dict

router = APIRouter()

@router.get("/")
async def get_agents(request: Request) -> List[Dict]:
    """Get all agent statuses from orchestrator"""
    orchestrator = request.app.state.orchestrator
    
    if hasattr(orchestrator, 'get_agent_status'):
        # AWS Bedrock mode
        return orchestrator.get_agent_status()
    elif hasattr(orchestrator, 'get_agent_statuses'):
        # Simulation mode
        return orchestrator.get_agent_statuses()
    else:
        # Fallback
        return []

@router.get("/{agent_id}")
async def get_agent(agent_id: str, request: Request) -> Dict:
    """Get specific agent details"""
    orchestrator = request.app.state.orchestrator
    
    if hasattr(orchestrator, 'get_agent_status'):
        agents = orchestrator.get_agent_status()
        for agent in agents:
            if agent.get('id') == agent_id:
                return agent
    
    return {"id": agent_id, "name": "Agent", "status": "active"}
