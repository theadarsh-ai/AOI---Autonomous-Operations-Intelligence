from fastapi import APIRouter, Request
from typing import List, Dict

router = APIRouter()

@router.get("/")
async def get_activity_log(request: Request, limit: int = 50) -> Dict:
    """Get agent activity log"""
    orchestrator = request.app.state.orchestrator
    
    if hasattr(orchestrator, 'get_activity_log'):
        return {
            "activities": orchestrator.get_activity_log(limit),
            "total_count": len(orchestrator.activity_log) if hasattr(orchestrator, 'activity_log') else 0
        }
    else:
        return {"activities": [], "total_count": 0}
