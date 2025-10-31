from enum import Enum
from abc import ABC, abstractmethod
from typing import Dict, Optional
import asyncio
import logging

logger = logging.getLogger(__name__)

class AgentStatus(Enum):
    IDLE = "idle"
    ACTIVE = "active"
    PROCESSING = "processing"

class BaseAgent(ABC):
    """Base class for all AI agents"""
    
    def __init__(self, name: str, agent_type: str):
        self.name = name
        self.agent_type = agent_type
        self.status = AgentStatus.IDLE
        self.active_tasks = 0
        self.decisions_per_hour = 0
        self.accuracy = 85.0
        self.uptime = 99.5
        self.recent_activity = ""
    
    async def run(self):
        """Main agent loop - override in subclasses"""
        while True:
            await asyncio.sleep(1)
    
    def get_status(self) -> Dict:
        """Return current agent status"""
        return {
            "id": self.agent_type,
            "name": self.name,
            "status": self.status.value,
            "active_tasks": self.active_tasks,
            "recent_activity": self.recent_activity,
            "uptime": f"{self.uptime}%",
            "decisions_per_hour": self.decisions_per_hour,
            "accuracy": round(self.accuracy, 1)
        }
    
    def update_activity(self, activity: str):
        """Update recent activity"""
        self.recent_activity = activity
        logger.info(f"[{self.name}] {activity}")
