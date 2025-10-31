import asyncio
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

from .base_agent import BaseAgent, AgentStatus
from .monitoring_agent import MonitoringAgent
from .decision_agent import DecisionAgent
from .lifecycle_agent import LifecycleAgent
from .resource_agent import ResourceAgent
from .financial_agent import FinancialAgent
from .security_agent import SecurityAgent
from .learning_agent import LearningAgent

logger = logging.getLogger(__name__)

class AgentOrchestrator:
    """
    Master Orchestrator Agent - Coordinates all sub-agents and maintains global state
    Simulates AWS Bedrock Agent orchestration with Claude 3.5 Sonnet
    """
    
    def __init__(self):
        self.running = False
        self.agents: Dict[str, BaseAgent] = {}
        self.decisions_log: List[Dict] = []
        self.predictions: List[Dict] = []
        self.metrics = {
            "autonomous_actions": 0,
            "total_decisions": 0,
            "prevention_savings": 0,
            "prediction_accuracy": 89.0,
            "active_incidents": 3
        }
        
        # Initialize all agents
        self._initialize_agents()
        
    def _initialize_agents(self):
        """Initialize all 8 specialized agents"""
        self.agents = {
            "monitoring": MonitoringAgent(),
            "decision": DecisionAgent(),
            "lifecycle": LifecycleAgent(),
            "resource": ResourceAgent(),
            "financial": FinancialAgent(),
            "security": SecurityAgent(),
            "learning": LearningAgent()
        }
        logger.info(f"✅ Initialized {len(self.agents)} specialized agents")
    
    async def run(self):
        """Main orchestration loop - runs autonomously"""
        self.running = True
        logger.info("🤖 Master Orchestrator: Starting autonomous operation...")
        
        # Start all agents
        tasks = [agent.run() for agent in self.agents.values()]
        
        # Start orchestration loop
        tasks.append(self._orchestration_loop())
        
        await asyncio.gather(*tasks)
    
    async def _orchestration_loop(self):
        """Continuously orchestrate agent activities and make decisions"""
        while self.running:
            try:
                # Simulate predictive monitoring detecting an issue
                if random.random() < 0.1:  # 10% chance per cycle
                    await self._handle_predicted_issue()
                
                # Update metrics
                await self._update_metrics()
                
                # Simulate learning and adaptation
                if random.random() < 0.05:  # 5% chance per cycle
                    await self._trigger_learning_update()
                
                await asyncio.sleep(5)  # Run every 5 seconds
                
            except Exception as e:
                logger.error(f"Error in orchestration loop: {e}")
                await asyncio.sleep(1)
    
    async def _handle_predicted_issue(self):
        """Simulate autonomous decision-making workflow"""
        # Step 1: Monitoring agent detects anomaly
        prediction = await self.agents["monitoring"].predict_failure()
        
        if not prediction:
            return
        
        self.predictions.append(prediction)
        logger.info(f"🔍 Prediction: {prediction['title']}")
        
        # Step 2: Decision agent evaluates and approves action
        decision = await self.agents["decision"].evaluate_action(prediction)
        
        if decision["approved"]:
            self.decisions_log.insert(0, decision)
            self.metrics["autonomous_actions"] += 1
            self.metrics["total_decisions"] += 1
            self.metrics["prevention_savings"] += decision["cost"] * decision["roi"]
            
            logger.info(f"✅ Auto-approved: {decision['decision_type']} (ROI: {decision['roi']}:1)")
            
            # Step 3: Resource agent assigns technician
            if decision["autonomy_level"] <= 2:
                await self.agents["resource"].assign_technician(decision)
        else:
            logger.info(f"⚠️ Escalated: {decision['decision_type']}")
    
    async def _update_metrics(self):
        """Update system-wide metrics"""
        # Simulate gradual improvement in accuracy
        self.metrics["prediction_accuracy"] += random.uniform(-0.1, 0.3)
        self.metrics["prediction_accuracy"] = min(95.0, self.metrics["prediction_accuracy"])
        
        # Update active incidents
        if random.random() < 0.1:
            self.metrics["active_incidents"] = max(0, self.metrics["active_incidents"] + random.choice([-1, 1]))
    
    async def _trigger_learning_update(self):
        """Trigger learning agent to update models"""
        await self.agents["learning"].update_models()
        logger.info("🧠 Learning Agent: Updated prediction models")
    
    def get_agent_statuses(self) -> List[Dict]:
        """Get current status of all agents"""
        statuses = []
        for agent_id, agent in self.agents.items():
            statuses.append(agent.get_status())
        return statuses
    
    def get_latest_decision(self) -> Optional[Dict]:
        """Get the most recent decision"""
        return self.decisions_log[0] if self.decisions_log else None
    
    def get_current_metrics(self) -> Dict:
        """Get current system metrics"""
        return {
            **self.metrics,
            "autonomous_percentage": round((self.metrics["autonomous_actions"] / max(1, self.metrics["total_decisions"])) * 100, 1)
        }
    
    def get_current_time(self) -> str:
        """Get current timestamp"""
        return datetime.now().strftime("%H:%M:%S")
    
    def is_running(self) -> bool:
        return self.running
    
    def get_agent_count(self) -> int:
        return len(self.agents)
    
    def get_active_agents_count(self) -> int:
        return sum(1 for agent in self.agents.values() if agent.status == AgentStatus.ACTIVE)
