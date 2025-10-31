from fastapi import APIRouter
from typing import Dict

router = APIRouter()

@router.get("/")
async def get_metrics() -> Dict:
    """Get system-wide metrics"""
    return {
        "autonomous_actions": 95,
        "prevention_savings": 128000,
        "prediction_accuracy": 89,
        "active_incidents": 3
    }
