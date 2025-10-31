"""
Generate 5000+ realistic MSP operational data records
Creates comprehensive dataset for testing autonomous agent workflows
"""

import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import uuid

class MSPDataGenerator:
    """Generates realistic MSP operational data at scale"""
    
    def __init__(self, seed: int = 42):
        random.seed(seed)
        
        # Realistic data pools
        self.company_names = [
            "Acme Corp", "TechStart Inc", "Global Solutions", "DataFlow Systems",
            "CloudFirst", "SecureNet", "InfoTech", "Digital Dynamics",
            "Smart Systems", "Innovate Inc", "NextGen Tech", "Alpha Solutions",
            "Beta Corp", "Gamma Systems", "Delta Tech", "Epsilon Inc",
            "Zeta Solutions", "Theta Corp", "Lambda Tech", "Omega Systems"
        ] * 30  # 600 potential unique companies
        
        self.server_types = [
            "DB-PROD", "WEB-PROD", "APP-PROD", "DB-DEV", "WEB-DEV", "APP-DEV",
            "DC-SERVER", "FILE-SERVER", "MAIL-SERVER", "DNS-SERVER",
            "BACKUP-SERVER", "CACHE-SERVER", "ANALYTICS", "MONITORING"
        ]
        
        self.issue_types = [
            "High CPU Usage", "Memory Leak", "Disk Space Low", "Network Latency",
            "SSL Certificate Expiring", "Backup Failure", "Service Down",
            "Security Vulnerability", "Performance Degradation", "Database Deadlock"
        ]
        
        self.technician_names = [
            "Sarah Chen", "Mike Rodriguez", "Emily Watson", "David Park",
            "Rachel Kim", "John Smith", "Maria Garcia", "Alex Johnson",
            "Lisa Anderson", "Tom Wilson", "Jennifer Lee", "Chris Martinez",
            "Amanda Brown", "Kevin Nguyen", "Michelle Davis", "Robert Taylor"
        ]
        
        self.skills = [
            "Windows Server", "Linux", "AWS", "Azure", "Network Security",
            "SQL Server", "MySQL", "PostgreSQL", "Active Directory",
            "VMware", "Docker", "Kubernetes", "Firewall Management",
            "Backup & Recovery", "Monitoring & Alerting"
        ]
    
    def generate_clients(self, count: int = 500) -> List[Dict[str, Any]]:
        """Generate realistic client records"""
        clients = []
        
        for i in range(count):
            client_id = f"CLT-{str(uuid.uuid4())[:8].upper()}"
            
            client = {
                "client_id": client_id,
                "company_name": self.company_names[i],
                "industry": random.choice([
                    "Healthcare", "Finance", "Retail", "Manufacturing",
                    "Technology", "Education", "Legal", "Consulting"
                ]),
                "monthly_recurring_revenue": random.randint(2000, 50000),
                "server_count": random.randint(5, 200),
                "employee_count": random.randint(20, 5000),
                "contract_start_date": (datetime.now() - timedelta(days=random.randint(30, 1095))).isoformat(),
                "contract_tier": random.choice(["Basic", "Professional", "Enterprise", "Premium"]),
                "health_score": random.randint(60, 100),
                "satisfaction_score": round(random.uniform(3.5, 5.0), 1),
                "compliance_required": random.choice([[], ["HIPAA"], ["SOC2"], ["GDPR"], ["HIPAA", "SOC2"]]),
                "status": random.choice(["active", "active", "active", "active", "at_risk", "onboarding"])
            }
            
            clients.append(client)
        
        return clients
    
    def generate_servers(self, clients: List[Dict], count: int = 2000) -> List[Dict[str, Any]]:
        """Generate realistic server infrastructure records"""
        servers = []
        
        for i in range(count):
            client = random.choice(clients)
            server_id = f"SRV-{str(uuid.uuid4())[:8].upper()}"
            server_type = random.choice(self.server_types)
            
            # Realistic metric ranges based on server type
            is_critical = server_type.endswith("-PROD")
            base_cpu = random.uniform(20, 80) if not is_critical else random.uniform(40, 95)
            base_memory = random.uniform(30, 75) if not is_critical else random.uniform(50, 90)
            
            server = {
                "server_id": server_id,
                "client_id": client["client_id"],
                "hostname": f"{server_type}-{random.randint(1, 99):02d}",
                "server_type": server_type,
                "os": random.choice([
                    "Windows Server 2022", "Windows Server 2019",
                    "Ubuntu 22.04 LTS", "CentOS 7", "RHEL 8"
                ]),
                "cpu_cores": random.choice([4, 8, 16, 32]),
                "ram_gb": random.choice([16, 32, 64, 128]),
                "disk_size_gb": random.choice([500, 1000, 2000, 4000]),
                "current_metrics": {
                    "cpu_percent": round(base_cpu + random.uniform(-5, 5), 1),
                    "memory_percent": round(base_memory + random.uniform(-5, 5), 1),
                    "disk_usage_percent": round(random.uniform(30, 85), 1),
                    "network_mbps": round(random.uniform(10, 500), 1),
                    "uptime_days": random.randint(1, 365)
                },
                "last_backup": (datetime.now() - timedelta(hours=random.randint(1, 48))).isoformat(),
                "last_patched": (datetime.now() - timedelta(days=random.randint(1, 30))).isoformat(),
                "risk_score": random.randint(0, 100),
                "criticality": "critical" if is_critical else random.choice(["high", "medium", "low"]),
                "status": random.choice(["healthy", "healthy", "healthy", "warning", "critical"])
            }
            
            servers.append(server)
        
        return servers
    
    def generate_tickets(self, clients: List[Dict], servers: List[Dict], count: int = 1500) -> List[Dict[str, Any]]:
        """Generate realistic support ticket records"""
        tickets = []
        
        for i in range(count):
            client = random.choice(clients)
            server = random.choice([s for s in servers if s["client_id"] == client["client_id"]] or servers)
            ticket_id = f"TKT-{random.randint(100000, 999999)}"
            
            issue = random.choice(self.issue_types)
            created = datetime.now() - timedelta(hours=random.randint(1, 720))
            
            ticket = {
                "ticket_id": ticket_id,
                "client_id": client["client_id"],
                "server_id": server["server_id"],
                "title": f"{issue} on {server['hostname']}",
                "description": f"Automated detection: {issue} detected on {server['hostname']}. Requires investigation.",
                "priority": random.choice(["low", "medium", "high", "critical"]),
                "status": random.choice([
                    "open", "in_progress", "pending_client", "resolved", "closed"
                ]),
                "category": random.choice([
                    "Performance", "Security", "Backup", "Network", "Hardware", "Software"
                ]),
                "created_date": created.isoformat(),
                "assigned_to": random.choice(self.technician_names),
                "estimated_hours": round(random.uniform(0.5, 8.0), 1),
                "actual_hours": round(random.uniform(0.25, 10.0), 1) if random.random() > 0.3 else None,
                "resolution_time_hours": round(random.uniform(1, 48), 1) if random.random() > 0.4 else None,
                "customer_satisfaction": random.randint(1, 5) if random.random() > 0.5 else None
            }
            
            tickets.append(ticket)
        
        return tickets
    
    def generate_incidents(self, servers: List[Dict], count: int = 800) -> List[Dict[str, Any]]:
        """Generate historical incident data for pattern learning"""
        incidents = []
        
        for i in range(count):
            server = random.choice(servers)
            incident_id = f"INC-{str(uuid.uuid4())[:8].upper()}"
            
            detected = datetime.now() - timedelta(days=random.randint(1, 365))
            resolved = detected + timedelta(hours=random.uniform(1, 72))
            
            incident = {
                "incident_id": incident_id,
                "server_id": server["server_id"],
                "client_id": server["client_id"],
                "incident_type": random.choice(self.issue_types),
                "severity": random.choice(["low", "medium", "high", "critical"]),
                "detected_date": detected.isoformat(),
                "resolved_date": resolved.isoformat(),
                "downtime_minutes": random.randint(0, 480),
                "root_cause": random.choice([
                    "Memory leak in application",
                    "Failed hard drive",
                    "Network configuration error",
                    "Software bug",
                    "Expired SSL certificate",
                    "Insufficient disk space",
                    "DDoS attack",
                    "Database connection pool exhaustion"
                ]),
                "resolution": random.choice([
                    "Restarted service",
                    "Applied patch",
                    "Replaced hardware",
                    "Updated configuration",
                    "Allocated more resources",
                    "Renewed certificate",
                    "Cleaned up disk space"
                ]),
                "business_impact_usd": random.randint(100, 50000),
                "prevention_cost_usd": random.randint(50, 5000),
                "was_preventable": random.choice([True, True, True, False]),
                "predicted_by_ai": random.choice([True, False])
            }
            
            incidents.append(incident)
        
        return incidents
    
    def generate_metrics(self, servers: List[Dict], days: int = 30) -> List[Dict[str, Any]]:
        """Generate time-series metric data for trend analysis"""
        metrics = []
        
        for server in random.sample(servers, min(200, len(servers))):
            for day in range(days):
                timestamp = datetime.now() - timedelta(days=day)
                
                # Add daily volatility to metrics
                for hour in range(0, 24, 6):  # 4 samples per day
                    metric_time = timestamp + timedelta(hours=hour)
                    
                    metric = {
                        "metric_id": f"MET-{str(uuid.uuid4())[:8].upper()}",
                        "server_id": server["server_id"],
                        "timestamp": metric_time.isoformat(),
                        "cpu_percent": round(server["current_metrics"]["cpu_percent"] + random.uniform(-10, 10), 1),
                        "memory_percent": round(server["current_metrics"]["memory_percent"] + random.uniform(-8, 8), 1),
                        "disk_usage_percent": round(server["current_metrics"]["disk_usage_percent"] + random.uniform(-2, 2), 1),
                        "network_in_mbps": round(random.uniform(5, 500), 1),
                        "network_out_mbps": round(random.uniform(5, 500), 1),
                        "response_time_ms": round(random.uniform(10, 500), 1),
                        "error_count": random.randint(0, 50),
                        "connection_count": random.randint(10, 1000)
                    }
                    
                    metrics.append(metric)
        
        return metrics
    
    def generate_decisions(self, count: int = 300) -> List[Dict[str, Any]]:
        """Generate autonomous decision history"""
        decisions = []
        
        for i in range(count):
            decision_id = f"DEC-{str(uuid.uuid4())[:8].upper()}"
            cost = random.randint(100, 15000)
            
            decision = {
                "decision_id": decision_id,
                "timestamp": (datetime.now() - timedelta(hours=random.randint(1, 720))).isoformat(),
                "decision_type": random.choice([
                    "preventive_maintenance", "resource_allocation",
                    "security_remediation", "capacity_upgrade",
                    "vendor_purchase", "contract_renewal"
                ]),
                "action_description": random.choice([
                    "Schedule disk expansion",
                    "Apply security patch",
                    "Assign technician to high-priority ticket",
                    "Renew SSL certificate",
                    "Upgrade server RAM",
                    "Schedule preventive maintenance window"
                ]),
                "estimated_cost_usd": cost,
                "estimated_roi": round(random.uniform(2.0, 20.0), 1),
                "autonomy_level": 1 if cost < 2000 else (2 if cost < 10000 else 3),
                "auto_approved": cost < 2000,
                "approval_status": "auto_approved" if cost < 2000 else random.choice([
                    "pending", "approved", "approved", "rejected"
                ]),
                "predicted_impact": random.choice([
                    "Prevents server outage",
                    "Improves response time by 30%",
                    "Eliminates security vulnerability",
                    "Reduces ticket volume"
                ]),
                "actual_outcome": random.choice([
                    "Success - prevented outage",
                    "Success - performance improved",
                    "Success - security resolved",
                    "Partial - minor issues remain",
                    None
                ]) if random.random() > 0.3 else None,
                "outcome_accuracy": random.randint(70, 100) if random.random() > 0.3 else None
            }
            
            decisions.append(decision)
        
        return decisions
    
    def generate_all_data(self) -> Dict[str, List[Dict[str, Any]]]:
        """Generate complete dataset with all entities"""
        print("🎲 Generating MSP operational data...")
        
        print("  📊 Generating 500 clients...")
        clients = self.generate_clients(500)
        
        print("  🖥️  Generating 2000 servers...")
        servers = self.generate_servers(clients, 2000)
        
        print("  🎫 Generating 1500 tickets...")
        tickets = self.generate_tickets(clients, servers, 1500)
        
        print("  🚨 Generating 800 incidents...")
        incidents = self.generate_incidents(servers, 800)
        
        print("  📈 Generating 24000 metrics...")
        metrics = self.generate_metrics(servers, days=30)
        
        print("  🤖 Generating 300 decisions...")
        decisions = self.generate_decisions(300)
        
        total_records = len(clients) + len(servers) + len(tickets) + len(incidents) + len(metrics) + len(decisions)
        
        print(f"\n✅ Generated {total_records:,} total records!")
        
        return {
            "clients": clients,
            "servers": servers,
            "tickets": tickets,
            "incidents": incidents,
            "metrics": metrics,
            "decisions": decisions,
            "summary": {
                "total_records": total_records,
                "clients_count": len(clients),
                "servers_count": len(servers),
                "tickets_count": len(tickets),
                "incidents_count": len(incidents),
                "metrics_count": len(metrics),
                "decisions_count": len(decisions)
            }
        }
    
    def save_to_json(self, data: Dict[str, Any], filename: str = "msp_data.json"):
        """Save generated data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"💾 Data saved to {filename}")


if __name__ == "__main__":
    generator = MSPDataGenerator()
    data = generator.generate_all_data()
    generator.save_to_json(data, "python_backend/generated_data.json")
