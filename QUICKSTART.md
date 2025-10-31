# 🚀 Quick Start Guide - MSP AI Orchestrator

## ✅ What's Been Built

A **complete hybrid architecture** combining:
- **Python Backend**: FastAPI + **Strands Agents** framework (AWS official SDK)
- **React Frontend**: Professional real-time dashboard with live visualizations
- **8 Specialized AI Agents**: Using Strands tools for autonomous decision-making
- **WebSocket Integration**: Real-time updates between backend and frontend

---

## 📊 Current Status

### ✅ Frontend (Running)
The **React dashboard is live** at http://localhost:5000 with:
- 8 agent status cards with live updates
- Autonomous decision log feed
- Predictive timeline for 24-48 hour forecasts
- Performance analytics charts
- Escalation queue for human approvals
- Dark/Light mode support

### 🐍 Backend (Ready to Start)
The **Python backend with Strands Agents** is fully configured and ready to run.

---

## 🎯 How to Use

### Option 1: View the Frontend Now (Mock Data)

The React frontend is already running with realistic mock data:

**🌐 Dashboard**: http://localhost:5000

You can explore all features:
- Agent activity monitoring
- Decision logs with ROI calculations
- Prediction cards
- Analytics charts
- Escalation approvals

### Option 2: Start Python Backend (Simulation Mode)

To enable real autonomous agent orchestration using **Strands Agents**:

**Terminal 1** (Keep current workflow running):
```bash
# Frontend continues running on port 5000
```

**Terminal 2** (New terminal):
```bash
# Start Python backend with Strands Agents
python python_backend/main.py
```

The backend will start on **port 8000** in **simulation mode** (no AWS credentials needed):
- ✅ API: http://localhost:8000
- ✅ API Docs: http://localhost:8000/docs
- ✅ WebSocket: ws://localhost:8000/ws

**Features in Simulation Mode**:
- ✅ Strands Agents framework initialized
- ✅ All 8 agents with specialized tools
- ✅ Autonomous decision-making logic
- ✅ Real-time WebSocket updates
- ✅ Predictive monitoring workflows
- ⚠️ Mock mode (no actual AWS Bedrock calls)

### Option 3: Full AWS Bedrock Integration

To use **real AWS Bedrock with Claude Sonnet**:

#### Prerequisites
1. AWS account with Bedrock access
2. Claude 4 Sonnet model access enabled in AWS Bedrock
3. AWS credentials configured

#### Setup

**Step 1**: Add AWS Credentials to Replit Secrets

Click "🔒 Secrets" in the left sidebar and add:
```
AWS_ACCESS_KEY_ID = your_key_here
AWS_SECRET_ACCESS_KEY = your_secret_here
AWS_DEFAULT_REGION = us-west-2
```

**Step 2**: Enable Claude Model Access

1. Go to [AWS Bedrock Console](https://console.aws.amazon.com/bedrock/)
2. Click "Model access" (left sidebar)
3. Request access to **Claude 4 Sonnet**
4. Wait for approval (usually instant)

**Step 3**: Start Backend with Bedrock

```bash
python python_backend/main.py
```

The backend will automatically detect AWS credentials and enable Bedrock:
```
✅ AWS credentials detected - Bedrock integration enabled
✅ Using AWS Bedrock with Claude Sonnet
```

---

## 🔧 API Endpoints

### Backend API (Port 8000)

```bash
# System Status
GET http://localhost:8000/
GET http://localhost:8000/api/health
GET http://localhost:8000/api/status

# Agents
GET http://localhost:8000/api/agents
GET http://localhost:8000/api/agents/{agent_id}

# Decisions
GET http://localhost:8000/api/decisions

# Predictions
GET http://localhost:8000/api/predictions

# Metrics
GET http://localhost:8000/api/metrics

# WebSocket (Real-time)
WS ws://localhost:8000/ws
```

### Test API

```bash
# Check health
curl http://localhost:8000/api/health

# Get all agents
curl http://localhost:8000/api/agents

# View API docs
open http://localhost:8000/docs
```

---

## 🏗️ Architecture

### Python Backend Structure

```
python_backend/
├── main.py                          # FastAPI server
├── agents/
│   ├── strands_orchestrator.py      # Master orchestrator using Strands
│   ├── websocket_manager.py         # Real-time WebSocket connections
│   └── tools/                       # Strands Agent Tools (Bedrock Action Groups)
│       ├── monitoring_tools.py      # Predictive monitoring tools
│       ├── decision_tools.py        # Autonomous decision tools
│       ├── resource_tools.py        # Resource optimization tools
│       └── security_tools.py        # Security & compliance tools
└── routes/                          # API endpoints
    ├── agents.py
    ├── decisions.py
    ├── predictions.py
    └── metrics.py
```

### Strands Agent Tools (AWS Bedrock Action Groups)

Each agent has specialized tools it can invoke autonomously:

**Monitoring Agent**:
- `analyze_system_metrics(system_id, timeframe)` → risk_score
- `predict_failure(metric_data, historical_patterns)` → prediction
- `calculate_business_impact(failure_type, client_id)` → impact_assessment

**Decision Agent**:
- `evaluate_action_approval(action_type, cost, impact)` → approved/escalate
- `calculate_roi(preventive_cost, failure_cost)` → roi_analysis
- `execute_approved_decision(action_plan)` → execution_status

**Resource Agent**:
- `find_optimal_technician(required_skills, availability)` → assignment
- `optimize_maintenance_schedule(client_windows, urgency)` → schedule

**Security Agent**:
- `scan_vulnerabilities(system_id, scan_type)` → scan_results
- `auto_remediate_vulnerability(vulnerability_id, system_id)` → remediation_status

---

## 🎓 How It Works

### Autonomous Workflow Example

1. **Monitoring Agent** detects anomaly → predicts disk failure in 36 hours
2. **Master Orchestrator** receives alert → evaluates severity
3. **Decision Agent** calculates ROI (15:1) → auto-approves $800 preventive maintenance
4. **Resource Agent** assigns best-available technician with required skills
5. **Orchestrator** coordinates execution via workflow
6. **Learning Agent** tracks outcome and updates prediction models

**All autonomous - no human intervention needed for Level 1 & 2 decisions!**

### Autonomy Levels

- **Level 1** (<$2K): Full autonomy ✅
- **Level 2** ($2K-$10K): Conditional autonomy with notification ✅
- **Level 3** (>$10K): Requires human approval ⚠️

---

## 📦 What's Installed

### Python Packages
- ✅ `strands-agents` - AWS official agent framework
- ✅ `strands-agents-tools` - Pre-built agent tools
- ✅ `fastapi` - Modern Python web framework
- ✅ `uvicorn` - ASGI server
- ✅ `websockets` - Real-time communication
- ✅ `boto3` - AWS SDK for Python

### Frontend Stack
- ✅ React + TypeScript
- ✅ Tailwind CSS + Shadcn UI
- ✅ Recharts for analytics
- ✅ Lucide icons
- ✅ TanStack Query

---

## 🔥 Next Steps

### Immediate (5 minutes)
1. **Explore the dashboard** at http://localhost:5000
2. **Start Python backend** in a new terminal: `python python_backend/main.py`
3. **Test the API** at http://localhost:8000/docs

### Soon (30 minutes)
1. **Add AWS credentials** to enable Bedrock
2. **Test autonomous workflows** with real Claude Sonnet
3. **Customize agent tools** in `python_backend/agents/tools/`

### Future (Production)
1. **Deploy to AWS Bedrock AgentCore** for serverless operation
2. **Integrate real RMM/PSA systems** (ConnectWise, Datto, etc.)
3. **Add knowledge bases** with historical incident data
4. **Enable Step Functions** for complex multi-step workflows

---

## 📚 Resources

- **Strands Agents Docs**: https://strandsagents.com
- **AWS Bedrock**: https://aws.amazon.com/bedrock/
- **Strands GitHub**: https://github.com/strands-agents/sdk-python
- **Full README**: See README.md for complete documentation

---

## 🆘 Need Help?

### Common Issues

**Backend won't start**:
```bash
# Make sure you're in the right directory
cd /path/to/workspace
python python_backend/main.py
```

**Port already in use**:
```bash
# Kill existing process
lsof -ti:8000 | xargs kill -9
python python_backend/main.py
```

**AWS Bedrock errors**:
- Check that AWS credentials are in Secrets (not in code)
- Verify Claude 4 Sonnet model access is enabled
- Check region is supported (us-west-2, us-east-1)

### Success Indicators

✅ Backend: "Strands Agents initialized successfully"  
✅ Frontend: Dashboard loads with 8 agent cards  
✅ Bedrock: "Using AWS Bedrock with Claude Sonnet"

---

**Built with Strands Agents + AWS Bedrock + FastAPI + React** 🚀
