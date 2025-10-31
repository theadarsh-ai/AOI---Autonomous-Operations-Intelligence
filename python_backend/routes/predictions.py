from fastapi import APIRouter
from typing import List, Dict

router = APIRouter()

@router.get("/")
async def get_predictions() -> List[Dict]:
    """Get upcoming predictions"""
    return []
