from fastapi import APIRouter, Request
from typing import List, Dict

router = APIRouter()

@router.get("/")
async def get_predictions(request: Request) -> Dict:
    """Get upcoming predictions"""
    orchestrator = request.app.state.orchestrator
    
    if hasattr(orchestrator, 'get_predictions'):
        # AWS Bedrock mode
        predictions = orchestrator.get_predictions()
        return {
            "predictions": predictions,
            "time_window": "24-48 hours",
            "average_confidence": 87.5
        }
    elif hasattr(orchestrator, 'get_latest_predictions'):
        # Simulation mode
        return {
            "predictions": orchestrator.get_latest_predictions(10),
            "time_window": "24-48 hours",
            "average_confidence": 87.5
        }
    else:
        return {"predictions": [], "time_window": "24-48 hours"}
