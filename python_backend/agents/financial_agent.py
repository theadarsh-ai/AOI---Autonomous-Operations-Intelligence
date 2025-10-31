from .base_agent import BaseAgent, AgentStatus

class FinancialAgent(BaseAgent):
    """Financial Intelligence Agent - Analyzes profitability and pricing"""
    
    def __init__(self):
        super().__init__("Financial Intelligence", "financial")
        self.decisions_per_hour = 12
        self.accuracy = 91.0
        self.update_activity("Analyzing profitability forecasts")
