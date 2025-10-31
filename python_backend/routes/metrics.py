from fastapi import APIRouter, Request
from typing import Dict

router = APIRouter()

@router.get("/")
async def get_metrics(request: Request) -> Dict:
    """Get system-wide metrics from orchestrator"""
    orchestrator = request.app.state.orchestrator
    
    if hasattr(orchestrator, 'get_performance_metrics'):
        # AWS Bedrock mode
        return orchestrator.get_performance_metrics()
    elif hasattr(orchestrator, 'get_current_metrics'):
        # Simulation mode
        return orchestrator.get_current_metrics()
    else:
        # Fallback metrics
        return {
            "autonomous_actions": 0,
            "prevention_savings": 0,
            "prediction_accuracy": 0,
            "active_incidents": 0
        }
