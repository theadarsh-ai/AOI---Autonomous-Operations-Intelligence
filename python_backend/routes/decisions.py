from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

@router.get("/")
async def get_decisions() -> List[Dict]:
    """Get recent autonomous decisions"""
    return []

@router.get("/{decision_id}")
async def get_decision(decision_id: str) -> Dict:
    """Get specific decision details"""
    return {"id": decision_id}
