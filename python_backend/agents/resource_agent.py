import random
from typing import Dict
from .base_agent import BaseAgent, AgentStatus

class ResourceAgent(BaseAgent):
    """Resource Optimization Agent - Assigns technicians and optimizes schedules"""
    
    def __init__(self):
        super().__init__("Resource Optimization", "resource")
        self.decisions_per_hour = 14
        self.accuracy = 86.0
        self.update_activity("Optimizing technician assignments")
    
    async def assign_technician(self, decision: Dict):
        """Simulate technician assignment based on skills and availability"""
        technicians = ["Sarah Chen", "Mike Rodriguez", "Amanda Park", "John Smith"]
        assigned = random.choice(technicians)
        self.update_activity(f"Assigned {assigned} to {decision['decision_type']}")
