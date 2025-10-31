from fastapi import APIRouter, Request
from typing import List, Dict

router = APIRouter()

@router.get("/")
async def get_decisions(request: Request) -> Dict:
    """Get recent autonomous decisions"""
    orchestrator = request.app.state.orchestrator
    
    if hasattr(orchestrator, 'get_recent_decisions'):
        # AWS Bedrock mode
        decisions = orchestrator.get_recent_decisions(20)
        return {
            "recent_decisions": decisions,
            "total_count": len(decisions)
        }
    elif hasattr(orchestrator, 'decisions_log'):
        # Simulation mode
        return {
            "recent_decisions": orchestrator.decisions_log[:20],
            "total_count": len(orchestrator.decisions_log)
        }
    else:
        return {"recent_decisions": [], "total_count": 0}

@router.get("/{decision_id}")
async def get_decision(decision_id: str, request: Request) -> Dict:
    """Get specific decision details"""
    orchestrator = request.app.state.orchestrator
    
    if hasattr(orchestrator, 'get_recent_decisions'):
        decisions = orchestrator.get_recent_decisions(100)
        for decision in decisions:
            if decision.get('id') == decision_id:
                return decision
    
    return {"id": decision_id}
