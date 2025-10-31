from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

# Mock data for agents - will be replaced by orchestrator data
@router.get("/")
async def get_agents() -> List[Dict]:
    """Get all agent statuses"""
    return [
        {
            "id": "orchestrator",
            "name": "Master Orchestrator",
            "status": "active",
            "active_tasks": 8,
            "uptime": "99.9%",
            "decisions_per_hour": 42,
            "accuracy": 94
        }
    ]

@router.get("/{agent_id}")
async def get_agent(agent_id: str) -> Dict:
    """Get specific agent details"""
    return {
        "id": agent_id,
        "name": "Agent Name",
        "status": "active"
    }
