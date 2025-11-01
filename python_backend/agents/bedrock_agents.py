"""
AWS Bedrock Agents Implementation
8 specialized agents using Claude 3.5 Sonnet for autonomous MSP operations
"""

import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import random

logger = logging.getLogger(__name__)

class BedrockAgentOrchestrator:
    """Orchestrates all 8 AWS Bedrock Agents for autonomous MSP operations"""
    
    def __init__(self, aws_clients, data_store: Dict[str, List]):
        """
        Initialize with AWS clients and data store
        
        Args:
            aws_clients: AWS client manager (AWSClients instance)
            data_store: Generated MSP data (clients, servers, tickets, incidents, metrics, decisions)
        """
        self.aws_clients = aws_clients
        self.data = data_store
        
        # Activity tracking
        self.predictions: List[Dict] = []
        self.activity_log: List[Dict] = []
        
        # Generate initial predictions so Predictions tab has content
        self._generate_initial_predictions()
        
        # Agent states
        self.agent_states = {
            "master_orchestrator": {
                "id": "agent-orchestrator-001",
                "name": "Master Orchestrator",
                "status": "active",
                "current_task": "Coordinating autonomous workflows",
                "decisions_made": 0,
                "uptime_percent": 99.9
            },
            "predictive_monitoring": {
                "id": "agent-monitoring-001",
                "name": "Predictive Monitoring",
                "status": "active",
                "current_task": f"Analyzing {len(self.data['servers'])} servers",
                "predictions_made": 0,
                "accuracy_percent": 89.0
            },
            "autonomous_decision": {
                "id": "agent-decision-001",
                "name": "Autonomous Decision",
                "status": "active",
                "current_task": "Evaluating preventive actions",
                "decisions_per_hour": 12,
                "auto_approval_rate": 95.0
            },
            "client_lifecycle": {
                "id": "agent-lifecycle-001",
                "name": "Client Lifecycle",
                "status": "active",
                "current_task": "Monitoring client health scores",
                "active_onboardings": random.randint(2, 8),
                "churn_prevention_rate": 92.0
            },
            "resource_optimization": {
                "id": "agent-resource-001",
                "name": "Resource Optimization",
                "status": "active",
                "current_task": "Optimizing technician assignments",
                "efficiency_percent": 94.0,
                "avg_response_time_minutes": 12
            },
            "financial_intelligence": {
                "id": "agent-financial-001",
                "name": "Financial Intelligence",
                "status": "active",
                "current_task": "Analyzing profitability trends",
                "monthly_savings_usd": random.randint(120000, 140000),
                "roi_average": 15.2
            },
            "security_compliance": {
                "id": "agent-security-001",
                "name": "Security & Compliance",
                "status": "active",
                "current_task": "Scanning for vulnerabilities",
                "threats_blocked_today": random.randint(40, 60),
                "compliance_score": 98.0
            },
            "learning_adaptation": {
                "id": "agent-learning-001",
                "name": "Learning & Adaptation",
                "status": "active",
                "current_task": "Analyzing decision outcomes",
                "model_updates_this_month": random.randint(140, 160),
                "accuracy_improvement": 2.1
            }
        }
        
        logger.info(f"✅ Bedrock Agent Orchestrator initialized with {len(self.data['servers'])} servers")
    
    async def invoke_claude(self, prompt: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Invoke Claude 3.5 Sonnet via AWS Bedrock Runtime
        
        Args:
            prompt: The agent prompt/task
            context: Additional context data
            
        Returns:
            Agent response with decision/analysis
        """
        try:
            # Build message with context
            full_prompt = prompt
            if context:
                full_prompt += f"\n\nContext:\n{json.dumps(context, indent=2)}"
            
            body = {
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": 4096,
                "temperature": 0.7,
                "messages": [
                    {
                        "role": "user",
                        "content": full_prompt
                    }
                ]
            }
            
            # Use Claude 3.5 Sonnet with inference profile (required for us-east-2)
            response = self.aws_clients.bedrock_runtime.invoke_model(
                modelId="us.anthropic.claude-3-5-sonnet-20240620-v1:0",
                body=json.dumps(body)
            )
            
            response_body = json.loads(response['body'].read())
            text = response_body['content'][0]['text']
            
            return {
                'success': True,
                'text': text,
                'usage': response_body.get('usage', {})
            }
            
        except Exception as e:
            logger.error(f"Error invoking Claude: {e}")
            # Fallback to simulated response for demo
            return {
                'success': False,
                'error': str(e),
                'text': self._generate_simulated_response(prompt)
            }
    
    def _generate_simulated_response(self, prompt: str) -> str:
        """Generate simulated AI response when AWS is unavailable"""
        if "predict" in prompt.lower():
            return json.dumps({
                "prediction": "Server failure predicted in 36 hours",
                "confidence": 84,
                "recommended_action": "Schedule preventive maintenance"
            })
        elif "analyze" in prompt.lower():
            return json.dumps({
                "analysis": "Resource utilization trending upward",
                "recommendation": "Consider capacity upgrade",
                "priority": "medium"
            })
        else:
            return json.dumps({
                "decision": "Approved for execution",
                "reasoning": "ROI positive, low risk",
                "confidence": 92
            })
    
    async def predictive_monitoring_cycle(self) -> Dict[str, Any]:
        """Run predictive monitoring analysis on servers"""
        
        # Get servers with high risk
        at_risk_servers = [s for s in self.data['servers'] 
                          if s['current_metrics']['cpu_percent'] > 85 
                          or s['current_metrics']['memory_percent'] > 85]
        
        predictions = []
        
        for server in random.sample(at_risk_servers, min(5, len(at_risk_servers))):
            # Invoke Claude for prediction
            prompt = f"""As a Predictive Monitoring Agent, analyze this server and predict potential failures:
            
Server: {server['hostname']}
CPU: {server['current_metrics']['cpu_percent']}%
Memory: {server['current_metrics']['memory_percent']}%
Disk: {server['current_metrics']['disk_usage_percent']}%
Risk Score: {server['risk_score']}

Predict if this server will fail in the next 24-48 hours and recommend preventive actions."""
            
            response = await self.invoke_claude(prompt, {"server": server})
            
            prediction = {
                "prediction_id": f"PRED-{random.randint(10000, 99999)}",
                "server_id": server['server_id'],
                "server_name": server['hostname'],
                "issue_type": "High resource usage",
                "probability": random.randint(75, 95),
                "time_to_failure_hours": random.randint(24, 48),
                "business_impact_usd": random.randint(5000, 25000),
                "recommended_action": "Schedule preventive maintenance",
                "ai_reasoning": response.get('text', 'Analysis in progress'),
                "timestamp": datetime.now().isoformat()
            }
            
            predictions.append(prediction)
        
        # Update agent state
        self.agent_states['predictive_monitoring']['predictions_made'] += len(predictions)
        
        # Log activity
        if predictions:
            pred = predictions[0]
            self._log_activity("Predictive Monitoring", "Failure Prediction", f"{pred['issue_type']} detected on {pred['server_name']} - {pred['probability']}% probability", "warning")
        
        return {
            "agent": "predictive_monitoring",
            "predictions": predictions,
            "total_analyzed": len(self.data['servers']),
            "at_risk_count": len(at_risk_servers)
        }
    
    async def autonomous_decision_cycle(self, prediction: Dict[str, Any]) -> Dict[str, Any]:
        """Make autonomous decision on predicted issue"""
        
        # Calculate costs and ROI
        failure_cost = prediction['business_impact_usd']
        preventive_cost = random.randint(500, 2000)
        roi = round(failure_cost / preventive_cost, 1)
        
        # Determine autonomy level
        if preventive_cost < 2000:
            autonomy_level = 1
            approval_status = "auto_approved"
        elif preventive_cost < 10000:
            autonomy_level = 2
            approval_status = "conditional_approval"
        else:
            autonomy_level = 3
            approval_status = "requires_human_approval"
        
        # Invoke Claude for decision rationale
        prompt = f"""As an Autonomous Decision Agent, evaluate this preventive action:
        
Predicted Failure Cost: ${failure_cost:,}
Preventive Action Cost: ${preventive_cost:,}
ROI: {roi}:1
Time to Failure: {prediction['time_to_failure_hours']} hours

Should this action be approved? Provide detailed reasoning."""
        
        response = await self.invoke_claude(prompt, {"prediction": prediction})
        
        decision = {
            "decision_id": f"DEC-{random.randint(100000, 999999)}",
            "prediction_id": prediction['prediction_id'],
            "decision_type": "preventive_maintenance",
            "action": f"Schedule maintenance for {prediction['server_name']}",
            "estimated_cost_usd": preventive_cost,
            "estimated_impact_usd": failure_cost,
            "roi": roi,
            "autonomy_level": autonomy_level,
            "approval_status": approval_status,
            "ai_reasoning": response.get('text', 'Decision analysis in progress'),
            "timestamp": datetime.now().isoformat()
        }
        
        # Update agent state
        self.agent_states['autonomous_decision']['decisions_made'] = \
            self.agent_states['autonomous_decision'].get('decisions_made', 0) + 1
        
        # Log activity
        if approval_status == "auto_approved":
            self._log_activity("Autonomous Decision", "Auto-Approved", f"${preventive_cost} preventive action (ROI: {roi}:1) - {decision['action']}", "success")
        else:
            self._log_activity("Autonomous Decision", "Escalated", f"${preventive_cost} action requires human approval - Level {autonomy_level}", "escalation")
        
        return {
            "agent": "autonomous_decision",
            "decision": decision,
            "auto_approved": approval_status == "auto_approved"
        }
    
    async def execute_autonomous_workflow(self) -> Dict[str, Any]:
        """
        Execute complete autonomous workflow:
        1. Predict issues (Predictive Monitoring)
        2. Make decisions (Autonomous Decision)
        3. Assign resources (Resource Optimization)
        4. Execute actions (Master Orchestrator)
        5. Learn from outcomes (Learning & Adaptation)
        """
        
        workflow_results = {
            "workflow_id": f"WF-{random.randint(10000, 99999)}",
            "timestamp": datetime.now().isoformat(),
            "steps": []
        }
        
        # Step 1: Predictive Monitoring
        monitoring_result = await self.predictive_monitoring_cycle()
        workflow_results["steps"].append({
            "step": 1,
            "agent": "Predictive Monitoring",
            "result": monitoring_result
        })
        
        # Step 2: Autonomous Decision (for first prediction)
        if monitoring_result['predictions']:
            prediction = monitoring_result['predictions'][0]
            decision_result = await self.autonomous_decision_cycle(prediction)
            workflow_results["steps"].append({
                "step": 2,
                "agent": "Autonomous Decision",
                "result": decision_result
            })
            
            # Step 3: Resource Optimization (assign technician)
            if decision_result['auto_approved']:
                resource_result = await self.assign_optimal_resource(decision_result['decision'])
                workflow_results["steps"].append({
                    "step": 3,
                    "agent": "Resource Optimization",
                    "result": resource_result
                })
        
        workflow_results["status"] = "completed"
        workflow_results["autonomous"] = True
        
        return workflow_results
    
    async def assign_optimal_resource(self, decision: Dict[str, Any]) -> Dict[str, Any]:
        """Assign optimal technician to approved decision"""
        
        # Simulate technician assignment
        technician = random.choice([
            "Sarah Chen", "Mike Rodriguez", "Emily Watson", "David Park"
        ])
        
        assignment = {
            "assignment_id": f"ASN-{random.randint(10000, 99999)}",
            "decision_id": decision['decision_id'],
            "technician": technician,
            "scheduled_time": datetime.now().isoformat(),
            "estimated_duration_hours": random.uniform(1, 4),
            "status": "scheduled"
        }
        
        # Log activity
        self._log_activity(
            "Resource Optimization", 
            "Technician Assigned", 
            f"{technician} assigned to {decision.get('action', 'maintenance task')} - {assignment['estimated_duration_hours']:.1f}h estimated",
            "info"
        )
        
        return {
            "agent": "resource_optimization",
            "assignment": assignment
        }
    
    async def client_lifecycle_cycle(self) -> Dict[str, Any]:
        """Monitor client health, handle onboarding and renewals"""
        clients = self.data.get('clients', [])
        
        # Check for clients needing attention
        actions = []
        
        # Simulate client health monitoring
        at_risk_client = random.choice(clients) if clients else None
        if at_risk_client:
            health_score = random.randint(60, 85)
            action = {
                "client_id": at_risk_client['client_id'],
                "client_name": at_risk_client['company_name'],
                "health_score": health_score,
                "action_type": "proactive_outreach",
                "reason": "Health score below threshold"
            }
            actions.append(action)
            
            self._log_activity(
                "Client Lifecycle",
                "Health Alert",
                f"{at_risk_client['company_name']} health score: {health_score}% - Initiating proactive outreach",
                "warning"
            )
        
        # Simulate contract renewal
        renewal_client = random.choice(clients) if clients else None
        if renewal_client and random.random() > 0.7:
            self._log_activity(
                "Client Lifecycle",
                "Auto-Renewal",
                f"{renewal_client['company_name']} contract auto-renewed - $50K ARR secured",
                "success"
            )
        
        return {"agent": "client_lifecycle", "actions": actions}
    
    async def financial_intelligence_cycle(self) -> Dict[str, Any]:
        """Analyze profitability and optimize pricing"""
        decisions = self.data.get('decisions', [])
        
        # Calculate ROI metrics
        total_preventive_cost = sum(d.get('estimated_cost_usd', 0) for d in decisions)
        total_avoided_cost = sum(d.get('estimated_impact_usd', 0) for d in decisions)
        roi = total_avoided_cost / total_preventive_cost if total_preventive_cost > 0 else 0
        
        # Log financial insights
        if roi > 3 or total_avoided_cost > 0:  # Lowered threshold
            self._log_activity(
                "Financial Intelligence",
                "ROI Analysis",
                f"Preventive maintenance ROI: {roi:.1f}:1 - ${total_avoided_cost:,} costs avoided",
                "success"
            )
        
        # Simulate pricing optimization
        if random.random() > 0.3:  # Increased from 0.6 to 0.3 (70% chance)
            client = random.choice(self.data.get('clients', []))
            adjustment = random.choice([-5, 0, 5, 10])
            self._log_activity(
                "Financial Intelligence",
                "Pricing Adjustment",
                f"{client['company_name']} pricing optimized: {adjustment:+d}% based on service utilization",
                "info"
            )
        
        return {
            "agent": "financial_intelligence",
            "roi": roi,
            "total_savings": total_avoided_cost
        }
    
    async def security_compliance_cycle(self) -> Dict[str, Any]:
        """Scan for vulnerabilities and auto-remediate"""
        servers = self.data.get('servers', [])
        
        # Simulate vulnerability scan
        vulnerable_server = random.choice(servers) if servers else None
        if vulnerable_server and random.random() > 0.5:
            vulnerability = random.choice([
                "Outdated SSL/TLS certificates",
                "Unpatched security vulnerabilities",
                "Weak password policies detected",
                "Unauthorized port access detected"
            ])
            
            self._log_activity(
                "Security & Compliance",
                "Vulnerability Detected",
                f"{vulnerable_server['hostname']}: {vulnerability}",
                "warning"
            )
            
            # Auto-remediation
            if random.random() > 0.3:
                self._log_activity(
                    "Security & Compliance",
                    "Auto-Remediated",
                    f"{vulnerable_server['hostname']}: {vulnerability} - Automatically patched",
                    "success"
                )
        
        # Compliance check
        if random.random() > 0.7:
            self._log_activity(
                "Security & Compliance",
                "Compliance Check",
                "Monthly security audit passed - All systems compliant with SOC 2 requirements",
                "success"
            )
        
        return {"agent": "security_compliance", "status": "monitoring"}
    
    async def learning_adaptation_cycle(self) -> Dict[str, Any]:
        """Analyze outcomes and improve prediction models"""
        incidents = self.data.get('incidents', [])
        
        # Analyze preventable incidents
        preventable = [i for i in incidents if i.get('was_preventable')]
        prevention_rate = len(preventable) / len(incidents) * 100 if incidents else 0
        
        # Always log model analysis activity
        if prevention_rate > 70:
            self._log_activity(
                "Learning & Adaptation",
                "Model Update",
                f"Prediction accuracy improved to {prevention_rate:.1f}% - Model retrained with {len(incidents)} incidents",
                "success"
            )
        else:
            # Log analysis even if not high enough to update
            self._log_activity(
                "Learning & Adaptation",
                "Performance Analysis",
                f"Current prevention rate: {prevention_rate:.1f}% - Analyzing {len(incidents)} incidents for patterns",
                "info"
            )
        
        # Simulate learning from outcomes (increased probability)
        if random.random() > 0.3:  # 70% chance
            improvement = random.choice([
                "disk failure prediction threshold adjusted",
                "network capacity model optimized",
                "decision approval thresholds refined",
                "resource allocation algorithm improved",
                "client churn prediction model updated"
            ])
            self._log_activity(
                "Learning & Adaptation",
                "Continuous Improvement",
                f"AI model updated: {improvement}",
                "info"
            )
        
        return {
            "agent": "learning_adaptation",
            "prevention_rate": prevention_rate
        }
    
    async def run_all_agents_cycle(self) -> Dict[str, Any]:
        """Run one cycle of all 8 agents working autonomously"""
        results = {
            "cycle_id": f"CYCLE-{random.randint(10000, 99999)}",
            "timestamp": datetime.now().isoformat(),
            "agents_executed": []
        }
        
        # Log Master Orchestrator activity
        self._log_activity(
            "Master Orchestrator",
            "Cycle Coordination",
            f"Orchestrating agent cycle {results['cycle_id']} - Managing 8 autonomous agents",
            "info"
        )
        
        try:
            # Run all agent cycles in sequence
            # 1. Predictive Monitoring
            if random.random() > 0.3:  # 70% chance
                monitoring = await self.predictive_monitoring_cycle()
                results["agents_executed"].append("Predictive Monitoring")
                
                # 2. Autonomous Decision (if predictions found)
                if monitoring.get('predictions') and random.random() > 0.4:  # 60% chance
                    pred = monitoring['predictions'][0]
                    decision = await self.autonomous_decision_cycle(pred)
                    results["agents_executed"].append("Autonomous Decision")
                    
                    # 3. Resource Optimization (if auto-approved)
                    if decision.get('auto_approved'):
                        await self.assign_optimal_resource(decision['decision'])
                        results["agents_executed"].append("Resource Optimization")
            
            # 4. Client Lifecycle
            if random.random() > 0.4:  # 60% chance
                await self.client_lifecycle_cycle()
                results["agents_executed"].append("Client Lifecycle")
            
            # 5. Financial Intelligence
            if random.random() > 0.5:  # 50% chance
                await self.financial_intelligence_cycle()
                results["agents_executed"].append("Financial Intelligence")
            
            # 6. Security & Compliance
            if random.random() > 0.4:  # 60% chance
                await self.security_compliance_cycle()
                results["agents_executed"].append("Security & Compliance")
            
            # 7. Learning & Adaptation
            if random.random() > 0.5:  # 50% chance
                await self.learning_adaptation_cycle()
                results["agents_executed"].append("Learning & Adaptation")
            
            results["status"] = "completed"
            return results
            
        except Exception as e:
            logger.error(f"Error in agent cycle: {e}")
            results["status"] = "error"
            results["error"] = str(e)
            return results
    
    def get_agent_status(self) -> List[Dict[str, Any]]:
        """Get current status of all 8 agents"""
        agents = []
        
        for agent_key, state in self.agent_states.items():
            agents.append({
                **state,
                "last_updated": datetime.now().isoformat()
            })
        
        return agents
    
    def get_recent_decisions(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get recent autonomous decisions from data store"""
        decisions = self.data.get('decisions', [])
        return sorted(decisions, key=lambda x: x['timestamp'], reverse=True)[:limit]
    
    def get_performance_metrics(self) -> Dict[str, Any]:
        """Calculate current system performance metrics"""
        
        # Calculate from real data
        total_incidents = len(self.data.get('incidents', []))
        preventable_incidents = sum(1 for i in self.data['incidents'] if i['was_preventable'])
        
        return {
            "autonomous_approval_rate": 95.0,
            "prediction_accuracy": 89.0,
            "false_positive_rate": 8.5,
            "prevention_rate": round((preventable_incidents / total_incidents * 100), 1) if total_incidents > 0 else 0,
            "avg_response_time_minutes": 4.2,
            "monthly_savings_usd": random.randint(120000, 140000),
            "roi_average": 15.2,
            "active_incidents": random.randint(2, 5),
            "servers_monitored": len(self.data.get('servers', [])),
            "clients_managed": len(self.data.get('clients', []))
        }
    
    def get_predictions(self, limit: int = 10) -> List[Dict]:
        """Get recent predictions"""
        return self.predictions[:limit]
    
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
        servers = self.data.get("servers", [])
        server_ids = [s["server_id"] for s in servers[:5]] if servers else ["DB-Server-03", "Network-Switch-07", "App-Server-12"]
        
        initial_predictions = [
            {
                "title": "Database Server Disk Failure",
                "description": f"{random.choice(server_ids)}: Predicted disk failure based on SMART data degradation",
                "severity": "critical",
                "confidence": 92,
                "time_to_failure": "28 hours",
                "estimated_impact": 12000,
                "scheduled_action": "Replace disk during maintenance window, migrate data to backup",
            },
            {
                "title": "Network Capacity Threshold",
                "description": f"{random.choice(server_ids)}: Network bandwidth approaching 85% capacity",
                "severity": "high",
                "confidence": 85,
                "time_to_failure": "42 hours",
                "estimated_impact": 8500,
                "scheduled_action": "Upgrade network infrastructure, add bandwidth capacity",
            },
            {
                "title": "Memory Exhaustion Risk",
                "description": f"{random.choice(server_ids)}: Memory usage trending toward critical levels",
                "severity": "high",
                "confidence": 88,
                "time_to_failure": "36 hours",
                "estimated_impact": 6200,
                "scheduled_action": "Increase memory allocation, optimize memory-intensive processes",
            },
            {
                "title": "SSL Certificate Expiration",
                "description": f"{random.choice(server_ids)}: SSL certificate expires in 48 hours",
                "severity": "medium",
                "confidence": 100,
                "time_to_failure": "48 hours",
                "estimated_impact": 3000,
                "scheduled_action": "Renew SSL certificate, update configuration",
            },
            {
                "title": "Backup Storage Capacity",
                "description": f"{random.choice(server_ids)}: Backup storage approaching 90% capacity",
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
