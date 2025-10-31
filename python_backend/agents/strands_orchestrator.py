"""
Master Orchestrator using Strands Agents framework
Coordinates all specialized agents using AWS Bedrock
"""

import asyncio
import logging
from datetime import datetime
from typing import Dict, List, Optional
from strands import Agent, tool
from strands.models import BedrockModel

from .tools.monitoring_tools import (
    analyze_system_metrics,
    predict_failure,
    calculate_business_impact
)
from .tools.decision_tools import (
    evaluate_action_approval,
    calculate_roi,
    execute_approved_decision
)
from .tools.resource_tools import (
    find_optimal_technician,
    optimize_maintenance_schedule
)
from .tools.security_tools import (
    scan_vulnerabilities,
    auto_remediate_vulnerability
)

logger = logging.getLogger(__name__)

class StrandsAgentOrchestrator:
    """
    Master Orchestrator using Strands Agents framework
    Simulates AWS Bedrock multi-agent system with autonomous decision-making
    """
    
    def __init__(self, use_bedrock: bool = False):
        self.running = False
        self.use_bedrock = use_bedrock
        self.decisions_log: List[Dict] = []
        self.predictions: List[Dict] = []
        self.activity_log: List[Dict] = []
        self.metrics = {
            "autonomous_actions": 0,
            "total_decisions": 0,
            "prevention_savings": 0,
            "prediction_accuracy": 89.0,
            "active_incidents": 3
        }
        
        # Generate initial predictions so tab isn't empty
        self._generate_initial_predictions()
        
        # Agent configurations
        self.agent_configs = {
            "orchestrator": {"name": "Master Orchestrator", "active_tasks": 8, "accuracy": 94},
            "monitoring": {"name": "Predictive Monitoring", "active_tasks": 12, "accuracy": 87},
            "decision": {"name": "Autonomous Decision", "active_tasks": 6, "accuracy": 92},
            "lifecycle": {"name": "Client Lifecycle", "active_tasks": 4, "accuracy": 89},
            "resource": {"name": "Resource Optimization", "active_tasks": 2, "accuracy": 86},
            "financial": {"name": "Financial Intelligence", "active_tasks": 5, "accuracy": 91},
            "security": {"name": "Security & Compliance", "active_tasks": 7, "accuracy": 95},
            "learning": {"name": "Learning & Adaptation", "active_tasks": 3, "accuracy": 88}
        }
        
        # Initialize Strands Agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize Strands Agents with AWS Bedrock or mock mode"""
        try:
            if self.use_bedrock:
                # Use AWS Bedrock with Claude Sonnet
                bedrock_model = BedrockModel(
                    model_id="us.anthropic.claude-sonnet-4-20250514-v1:0",
                    temperature=0.3,
                    streaming=False
                )
                logger.info("✅ Using AWS Bedrock with Claude Sonnet")
            else:
                # Mock mode - uses Strands default (requires OpenAI or other provider)
                bedrock_model = None
                logger.info("✅ Using mock mode (Bedrock credentials not configured)")
            
            # Monitoring Agent with tools
            self.monitoring_agent = Agent(
                name="Predictive Monitoring Agent",
                model=bedrock_model,
                tools=[
                    analyze_system_metrics,
                    predict_failure,
                    calculate_business_impact
                ],
                system_prompt="""You are a Predictive Monitoring Agent for an MSP.
                Your job is to analyze system metrics and predict failures 24-48 hours in advance.
                Use your tools to detect anomalies and calculate business impact.
                Be proactive and precise in your predictions."""
            )
            
            # Decision Agent with tools
            self.decision_agent = Agent(
                name="Autonomous Decision Agent",
                model=bedrock_model,
                tools=[
                    evaluate_action_approval,
                    calculate_roi,
                    execute_approved_decision
                ],
                system_prompt="""You are an Autonomous Decision Agent for an MSP.
                Your job is to make business decisions without human approval when within approved parameters.
                Evaluate cost-benefit, calculate ROI, and approve or escalate actions.
                Level 1 (<$2K): Full autonomy
                Level 2 ($2K-$10K): Conditional autonomy with notification
                Level 3 (>$10K): Escalate for human approval"""
            )
            
            # Resource Optimization Agent
            self.resource_agent = Agent(
                name="Resource Optimization Agent",
                model=bedrock_model,
                tools=[
                    find_optimal_technician,
                    optimize_maintenance_schedule
                ],
                system_prompt="""You are a Resource Optimization Agent for an MSP.
                Your job is to assign technicians based on skills and availability,
                and optimize maintenance windows to minimize client disruption."""
            )
            
            # Security & Compliance Agent
            self.security_agent = Agent(
                name="Security & Compliance Agent",
                model=bedrock_model,
                tools=[
                    scan_vulnerabilities,
                    auto_remediate_vulnerability
                ],
                system_prompt="""You are a Security & Compliance Agent for an MSP.
                Your job is to monitor security posture and automatically remediate
                vulnerabilities within approved parameters. Ensure regulatory compliance."""
            )
            
            logger.info("✅ Strands Agents initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing Strands Agents: {e}")
            logger.info("Running in simulation mode without actual Bedrock agents")
    
    async def run(self):
        """Main orchestration loop"""
        self.running = True
        logger.info("🤖 Master Orchestrator: Starting autonomous operation with Strands Agents...")
        
        # Start orchestration loop
        await self._orchestration_loop()
    
    async def _orchestration_loop(self):
        """Continuously orchestrate agent activities"""
        import random
        
        # Log orchestrator start
        self._log_activity("Master Orchestrator", "Started", "Multi-agent orchestration loop active - monitoring all systems", "info")
        
        while self.running:
            try:
                # Simulate predictive monitoring detecting an issue
                if random.random() < 0.15:  # 15% chance per cycle
                    await self._handle_autonomous_workflow()
                
                # Randomly log routine agent activities
                if random.random() < 0.08:  # 8% chance
                    activities = [
                        ("Security & Compliance", "Vulnerability Scan", "Completed security scan - 0 critical issues found"),
                        ("Resource Optimization", "Technician Assignment", "Optimized technician schedules for next 24 hours"),
                        ("Financial Intelligence", "Cost Analysis", "Analyzed profitability across 12 client accounts"),
                        ("Client Lifecycle", "Health Monitoring", "Checked health scores for all active clients"),
                        ("Learning & Adaptation", "Model Update", "Updated prediction models based on recent outcomes"),
                    ]
                    agent, action, details = random.choice(activities)
                    self._log_activity(agent, action, details, "info")
                
                # Update metrics
                self.metrics["prediction_accuracy"] += random.uniform(-0.1, 0.3)
                self.metrics["prediction_accuracy"] = min(95.0, self.metrics["prediction_accuracy"])
                
                await asyncio.sleep(5)  # Run every 5 seconds
                
            except Exception as e:
                logger.error(f"Error in orchestration loop: {e}")
                await asyncio.sleep(1)
    
    async def _handle_autonomous_workflow(self):
        """
        Simulate complete autonomous workflow using Strands Agents:
        1. Monitoring detects issue
        2. Decision agent evaluates
        3. Resource agent assigns technician
        4. Action executed autonomously
        """
        import random
        
        try:
            # Simulated prediction (in real scenario, Strands agent would analyze metrics)
            systems = ["DB-Server-03", "Network-Switch-07", "App-Server-12"]
            issues = [
                {
                    "title": "DB Server Disk Failure",
                    "description": f"{random.choice(systems)}: Predicted disk failure based on SMART data",
                    "severity": "critical",
                    "confidence": random.randint(82, 95),
                    "time_to_failure": f"{random.randint(24, 48)} hours",
                    "estimated_impact": random.randint(8000, 15000),
                    "scheduled_action": "Replace disk, migrate data",
                },
                {
                    "title": "Network Capacity Threshold",
                    "description": f"{random.choice(systems)}: Network approaching capacity limits",
                    "severity": "high",
                    "confidence": random.randint(78, 88),
                    "time_to_failure": f"{random.randint(36, 72)} hours",
                    "estimated_impact": random.randint(5000, 10000),
                    "scheduled_action": "Upgrade network infrastructure",
                }
            ]
            
            prediction = random.choice(issues)
            prediction["id"] = f"pred-{len(self.predictions)}"
            prediction["timestamp"] = datetime.now().strftime("%H:%M:%S")
            
            self.predictions.insert(0, prediction)
            self._log_activity("Predictive Monitoring", "Failure Prediction", f"{prediction['title']} - {prediction['time_to_failure']} (confidence: {prediction['confidence']}%)", "warning")
            logger.info(f"🔍 Prediction: {prediction['title']}")
            
            # Decision evaluation
            preventive_cost = random.randint(500, 2000)
            roi = round(prediction["estimated_impact"] / preventive_cost, 1)
            
            # Determine autonomy level
            if preventive_cost < 2000:
                autonomy_level = 1
                approved = True
            elif preventive_cost < 10000:
                autonomy_level = 2
                approved = True
            else:
                autonomy_level = 3
                approved = False
            
            decision = {
                "id": f"dec-{len(self.decisions_log)}",
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "agent_name": "Autonomous Decision",
                "decision_type": "Preventive Maintenance Scheduled",
                "description": f"{prediction['title']}: {prediction['scheduled_action']}",
                "cost": preventive_cost,
                "roi": roi,
                "autonomy_level": autonomy_level,
                "approved": approved,
                "auto_approved": approved
            }
            
            if approved:
                self.decisions_log.insert(0, decision)
                self.metrics["autonomous_actions"] += 1
                self.metrics["total_decisions"] += 1
                self.metrics["prevention_savings"] += preventive_cost * roi
                self._log_activity("Autonomous Decision", "Auto-Approved", f"${preventive_cost} preventive action (ROI: {roi}:1) - {decision['decision_type']}", "success")
                logger.info(f"✅ Auto-approved: ${preventive_cost} (ROI: {roi}:1)")
            else:
                self._log_activity("Autonomous Decision", "Escalated", f"${preventive_cost} action requires human approval - Autonomy Level {autonomy_level}", "escalation")
                logger.info(f"⚠️ Escalated for approval: ${preventive_cost}")
            
        except Exception as e:
            logger.error(f"Error in autonomous workflow: {e}")
    
    def get_agent_statuses(self) -> List[Dict]:
        """Get current status of all agents"""
        import random
        statuses = []
        for agent_id, config in self.agent_configs.items():
            statuses.append({
                "id": agent_id,
                "name": config["name"],
                "status": random.choice(["active", "processing", "idle"]),
                "active_tasks": config["active_tasks"],
                "uptime": "99.8%",
                "decisions_per_hour": random.randint(6, 42),
                "accuracy": config["accuracy"]
            })
        return statuses
    
    def get_latest_decision(self) -> Optional[Dict]:
        """Get the most recent decision"""
        return self.decisions_log[0] if self.decisions_log else None
    
    def get_latest_predictions(self, limit: int = 3) -> List[Dict]:
        """Get recent predictions"""
        return self.predictions[:limit]
    
    def get_current_metrics(self) -> Dict:
        """Get current system metrics"""
        total = max(1, self.metrics["total_decisions"])
        return {
            **self.metrics,
            "autonomous_percentage": round((self.metrics["autonomous_actions"] / total) * 100, 1)
        }
    
    def get_current_time(self) -> str:
        """Get current timestamp"""
        return datetime.now().strftime("%H:%M:%S")
    
    def is_running(self) -> bool:
        return self.running
    
    def get_agent_count(self) -> int:
        return len(self.agent_configs)
    
    def get_activity_log(self, limit: int = 50) -> List[Dict]:
        """Get recent agent activity"""
        return self.activity_log[:limit]
    
    def _log_activity(self, agent: str, action: str, details: str, level: str = "info"):
        """Log agent activity for real-time monitoring"""
        activity = {
            "id": f"act-{len(self.activity_log)}",
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "agent": agent,
            "action": action,
            "details": details,
            "level": level
        }
        self.activity_log.insert(0, activity)
        # Keep only last 200 activities
        if len(self.activity_log) > 200:
            self.activity_log = self.activity_log[:200]
    
    def _generate_initial_predictions(self):
        """Generate initial predictions so Predictions tab has content"""
        import random
        
        systems = ["DB-Server-03", "Network-Switch-07", "App-Server-12", "Mail-Server-05", "Web-Server-02"]
        
        initial_predictions = [
            {
                "title": "Database Server Disk Failure",
                "description": f"{random.choice(systems)}: Predicted disk failure based on SMART data degradation",
                "severity": "critical",
                "confidence": 92,
                "time_to_failure": "28 hours",
                "estimated_impact": 12000,
                "scheduled_action": "Replace disk during maintenance window, migrate data to backup",
            },
            {
                "title": "Network Capacity Threshold",
                "description": f"{random.choice(systems)}: Network bandwidth approaching 85% capacity",
                "severity": "high",
                "confidence": 85,
                "time_to_failure": "42 hours",
                "estimated_impact": 8500,
                "scheduled_action": "Upgrade network infrastructure, add bandwidth capacity",
            },
            {
                "title": "Memory Exhaustion Risk",
                "description": f"{random.choice(systems)}: Memory usage trending toward critical levels",
                "severity": "high",
                "confidence": 88,
                "time_to_failure": "36 hours",
                "estimated_impact": 6200,
                "scheduled_action": "Increase memory allocation, optimize memory-intensive processes",
            },
            {
                "title": "SSL Certificate Expiration",
                "description": f"{random.choice(systems)}: SSL certificate expires in 48 hours",
                "severity": "medium",
                "confidence": 100,
                "time_to_failure": "48 hours",
                "estimated_impact": 3000,
                "scheduled_action": "Renew SSL certificate, update configuration",
            },
            {
                "title": "Backup Storage Capacity",
                "description": f"{random.choice(systems)}: Backup storage approaching 90% capacity",
                "severity": "medium",
                "confidence": 94,
                "time_to_failure": "72 hours",
                "estimated_impact": 4500,
                "scheduled_action": "Expand backup storage, archive old backups",
            }
        ]
        
        for i, pred in enumerate(initial_predictions):
            pred["id"] = f"pred-{i}"
            pred["timestamp"] = datetime.now().strftime("%H:%M:%S")
            self.predictions.append(pred)
        
        self._log_activity("Predictive Monitoring", "System Initialized", f"Generated {len(initial_predictions)} initial predictions", "info")
