# MSP AI Orchestrator - Autonomous Multi-Agent System

**Fully autonomous AI-powered MSP management system** using **AWS Bedrock** and the **Strands Agents framework**. This system operates 24/7 without human intervention, predicting IT problems 24-48 hours before they occur and automatically executing preventive actions.

## 🏗️ Architecture

### Technology Stack
- **Backend**: Python FastAPI + **Strands Agents** (AWS official SDK)
- **Frontend**: React + TypeScript + Tailwind CSS
- **AI Framework**: Strands Agents SDK with AWS Bedrock integration
- **Real-time**: WebSocket connections for live updates
- **Visualization**: Recharts for analytics and performance tracking

### 8 Specialized AI Agents

1. **Master Orchestrator Agent** - Central command coordinating all sub-agents
2. **Predictive Monitoring Agent** - Predicts failures 24-48 hours in advance
3. **Autonomous Decision Agent** - Makes business decisions without human approval
4. **Client Lifecycle Agent** - Automates onboarding and client management
5. **Resource Optimization Agent** - Assigns technicians and optimizes schedules
6. **Financial Intelligence Agent** - Analyzes profitability and pricing
7. **Security & Compliance Agent** - Monitors security and remediates vulnerabilities
8. **Learning & Adaptation Agent** - Analyzes outcomes and improves models

## 🚀 Quick Start

### Option 1: Simulation Mode (No AWS Required)

Run the system in simulation mode without AWS credentials:

```bash
# Start both frontend and backend
bash start.sh
```

The system will run in **simulation mode** with realistic agent orchestration.

- **Frontend**: http://localhost:5000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Option 2: Full AWS Bedrock Integration

To use actual AWS Bedrock with Claude Sonnet:

#### Prerequisites

1. **AWS Account** with Bedrock access enabled
2. **Claude Sonnet model access** in AWS Bedrock console
3. **AWS credentials** configured

#### Setup AWS Credentials

**Method 1: Environment Variables (Recommended for Replit)**

Add these to your Replit Secrets:

```bash
AWS_ACCESS_KEY_ID=your_access_key_here
AWS_SECRET_ACCESS_KEY=your_secret_key_here
AWS_DEFAULT_REGION=us-west-2
```

**Method 2: AWS CLI Configuration**

```bash
aws configure
# Enter your AWS Access Key ID, Secret Access Key, and Region
```

#### Enable Bedrock Model Access

1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Navigate to "Model access" in the left sidebar
3. Request access to **Claude 4 Sonnet** (us.anthropic.claude-sonnet-4-20250514-v1:0)
4. Wait for approval (usually instant)

#### Run with Bedrock

```bash
# Start with AWS Bedrock enabled
bash start.sh
```

The system will automatically detect AWS credentials and use Bedrock.

## 📊 Features

### Real-Time Dashboard
- **Live Agent Activity**: Monitor all 8 agents with real-time status indicators
- **Autonomous Decision Feed**: Stream of auto-approved actions with ROI calculations
- **Predictive Timeline**: Visual timeline showing predicted issues 24-48 hours ahead
- **Performance Analytics**: Charts tracking accuracy, savings, and improvements
- **Escalation Queue**: Level 3 decisions requiring human approval

### Autonomous Operation Levels

**Level 1 - Full Autonomy** (No human approval)
- Preventive maintenance <$2K
- Routine ticket routing
- Standard vulnerability remediation
- Client notifications

**Level 2 - Conditional Autonomy** (Auto-approve with notification)
- Actions costing $2K-$10K
- Service upgrades
- Security updates requiring downtime

**Level 3 - Human-in-the-Loop** (Requires approval)
- Actions >$10K
- Custom contract negotiations
- Major infrastructure changes

## 🔧 API Endpoints

### Agent Status
```bash
GET /api/agents          # All agents
GET /api/agents/{id}     # Specific agent
```

### Decisions
```bash
GET /api/decisions       # Recent autonomous decisions
GET /api/decisions/{id}  # Decision details
```

### Predictions
```bash
GET /api/predictions     # Upcoming failure predictions
```

### System Metrics
```bash
GET /api/metrics         # Real-time system metrics
GET /api/health          # Health check
GET /api/status          # Complete system status
```

### WebSocket
```bash
WS /ws                   # Real-time updates stream
```

## 🛠️ Development

### Backend (Python)

```bash
cd python_backend
python main.py
```

**Strands Agents Tools**: Each agent has specialized tools (AWS Bedrock Action Groups):

- `monitoring_tools.py` - analyze_system_metrics, predict_failure, calculate_business_impact
- `decision_tools.py` - evaluate_action_approval, calculate_roi, execute_approved_decision
- `resource_tools.py` - find_optimal_technician, optimize_maintenance_schedule
- `security_tools.py` - scan_vulnerabilities, auto_remediate_vulnerability

### Frontend (React)

```bash
npm run dev
```

## 📦 Project Structure

```
├── python_backend/
│   ├── main.py                      # FastAPI server
│   ├── agents/
│   │   ├── strands_orchestrator.py  # Master orchestrator using Strands
│   │   ├── websocket_manager.py     # WebSocket connections
│   │   └── tools/                   # Agent tools (Bedrock Action Groups)
│   │       ├── monitoring_tools.py
│   │       ├── decision_tools.py
│   │       ├── resource_tools.py
│   │       └── security_tools.py
│   └── routes/                      # API endpoints
├── client/
│   └── src/
│       ├── components/              # React components
│       ├── pages/
│       │   └── Dashboard.tsx        # Main dashboard
│       └── lib/
│           └── mockData.ts          # Mock data for UI
└── start.sh                         # Startup script
```

## 🔐 Security & Compliance

- **AWS Secrets Manager** integration ready
- **Audit trail** for all autonomous decisions
- **Rollback capability** for failed actions
- **Human override** available for any autonomous decision
- **Compliance monitoring** (HIPAA, SOC2, GDPR)

## 📈 Success Metrics

- **95%** decisions made without human intervention
- **80%** problem prevention before client impact
- **24-48 hour** prediction accuracy > 85%
- **<5 minutes** decision execution time
- **<10%** false positive rate
- **90%+** ROI positive on preventive actions

## 🌐 Production Deployment (Future)

Deploy to **AWS Bedrock AgentCore** for serverless, production-grade operation:

```bash
pip install bedrock-agentcore
agentcore configure --entrypoint python_backend/main.py
agentcore launch
```

## 📚 Resources

- **Strands Agents Docs**: https://strandsagents.com/latest/documentation/docs/
- **AWS Bedrock**: https://aws.amazon.com/bedrock/
- **Strands GitHub**: https://github.com/strands-agents/sdk-python

## 🤝 Contributing

This is an MVP demonstration of autonomous MSP management using AWS Bedrock and Strands Agents framework.

## 📄 License

MIT License - Free to use and modify

---

**Built with**: Strands Agents SDK | AWS Bedrock | FastAPI | React | TypeScript
