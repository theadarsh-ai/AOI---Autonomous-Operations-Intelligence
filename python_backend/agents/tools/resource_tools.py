"""
Resource Optimization Agent Tools for Strands framework
"""

from strands import tool
import random

@tool
def find_optimal_technician(required_skills: list[str], availability: str = "immediate", location: str = "any") -> dict:
    """
    Find the best technician for a task based on skills and availability.
    
    Args:
        required_skills: List of required skills
        availability: When technician is needed
        location: Geographic location preference
    
    Returns:
        Optimal technician assignment
    """
    technicians = [
        {"name": "Sarah Chen", "skills": ["database", "networking", "cloud"], "match": 98},
        {"name": "Mike Rodriguez", "skills": ["security", "compliance", "linux"], "match": 92},
        {"name": "Amanda Park", "skills": ["database", "storage", "backup"], "match": 95},
        {"name": "John Smith", "skills": ["networking", "firewall", "vpn"], "match": 88}
    ]
    
    selected = random.choice(technicians)
    
    return {
        "technician": selected["name"],
        "skill_match": selected["match"],
        "availability": "Available now",
        "estimated_response_time": "15 minutes"
    }

@tool
def optimize_maintenance_schedule(client_windows: dict, urgency: str = "medium") -> dict:
    """
    Optimize maintenance window to minimize client disruption.
    
    Args:
        client_windows: Client's available maintenance windows
        urgency: How urgent the maintenance is
    
    Returns:
        Optimized schedule with minimal impact
    """
    times = ["2:00 AM", "3:00 AM", "11:00 PM"]
    
    return {
        "scheduled_time": random.choice(times) + " PST",
        "scheduled_date": "Tomorrow",
        "duration": "2 hours",
        "client_impact": "minimal",
        "notification_sent": True
    }
