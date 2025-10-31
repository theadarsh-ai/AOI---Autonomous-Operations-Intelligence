# 🐍 Python Backend Setup - MSP AI Orchestrator

## Current Status

✅ **Python backend is fully configured and ready to run!**

The backend uses the **Strands Agents framework** (AWS official SDK) to create autonomous AI agents powered by AWS Bedrock.

## Quick Start

### Step 1: Open a New Terminal

Since the React frontend is running in the current terminal, open a **new terminal** (Shell tab in Replit).

### Step 2: Start the Python Backend

```bash
python run_backend.py
```

You should see:
```
============================================================
🚀 MSP AI Orchestrator - Python Backend
============================================================
📡 API Server: http://localhost:8000
📚 API Docs: http://localhost:8000/docs
🔌 WebSocket: ws://localhost:8000/ws
============================================================

INFO:agents.strands_orchestrator:✅ Using mock mode (Bedrock credentials not configured)
INFO:agents.strands_orchestrator:✅ Strands Agents initialized successfully
INFO:__main__:🚀 Starting Autonomous MSP AI System in simulation mode...
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### Step 3: Verify Connection

The React dashboard should automatically connect via WebSocket. Look for:
- Connection status badge turns **green** with "Live"
- Agents start updating with real-time status
- Decision log shows new autonomous decisions every few seconds

## What's Running

### Simulation Mode (Default)

Without AWS credentials, the system runs in **simulation mode**:
- ✅ All 8 Strands Agents initialized
- ✅ Autonomous decision-making logic active
- ✅ WebSocket broadcasting real-time updates
- ✅ Predictive monitoring workflows simulated
- ⚠️ Using mock data (no actual AWS Bedrock API calls)

This is perfect for:
- Testing the complete system
- Demonstrating autonomous workflows
- Development and iteration

### API Endpoints Available

```bash
# System Status
curl http://localhost:8000/
curl http://localhost:8000/api/health

# Get All Agents
curl http://localhost:8000/api/agents

# Get Recent Decisions
curl http://localhost:8000/api/decisions

# Get Predictions
curl http://localhost:8000/api/predictions

# Get Metrics
curl http://localhost:8000/api/metrics

# Interactive API Docs
open http://localhost:8000/docs
```

## Enable AWS Bedrock (Optional)

To use **real AWS Bedrock with Claude Sonnet 4**:

### Prerequisites

1. AWS account with Bedrock access
2. Claude 4 Sonnet model access enabled in AWS Bedrock console
3. AWS credentials

### Setup

**Add to Replit Secrets** (🔒 icon in left sidebar):
```
AWS_ACCESS_KEY_ID = your_access_key
AWS_SECRET_ACCESS_KEY = your_secret_key
AWS_DEFAULT_REGION = us-west-2
```

**Restart the backend**:
```bash
# Stop current backend (Ctrl+C)
python run_backend.py
```

You should see:
```
✅ AWS credentials detected - Bedrock integration enabled
✅ Using AWS Bedrock with Claude Sonnet
```

## Architecture

### 8 Specialized Strands Agents

Each agent has custom tools (AWS Bedrock Action Groups):

1. **Master Orchestrator** - Coordinates all agents
2. **Predictive Monitoring** - Analyzes metrics, predicts failures
   - Tools: `analyze_system_metrics`, `predict_failure`, `calculate_business_impact`
3. **Autonomous Decision** - Evaluates and approves actions
   - Tools: `evaluate_action_approval`, `calculate_roi`, `execute_approved_decision`
4. **Client Lifecycle** - Manages client onboarding and health
5. **Resource Optimization** - Assigns technicians and schedules
   - Tools: `find_optimal_technician`, `optimize_maintenance_schedule`
6. **Financial Intelligence** - Analyzes profitability and pricing
7. **Security & Compliance** - Scans and remediates vulnerabilities
   - Tools: `scan_vulnerabilities`, `auto_remediate_vulnerability`
8. **Learning & Adaptation** - Improves models based on outcomes

### Autonomous Workflow

Every 5-10 seconds, the orchestrator simulates:

1. **Monitoring** agent detects anomaly → predicts failure in 36 hours
2. **Decision** agent calculates ROI (15:1) → auto-approves $800 preventive action
3. **Resource** agent assigns optimal technician
4. **WebSocket** broadcasts update to React frontend
5. **Learning** agent tracks outcome for model improvement

All without human intervention!

## Project Structure

```
python_backend/
├── main.py                      # FastAPI application
├── agents/
│   ├── strands_orchestrator.py  # Master orchestrator using Strands
│   ├── websocket_manager.py     # Real-time connections
│   └── tools/                   # Strands Agent Tools
│       ├── monitoring_tools.py  # @tool decorated functions
│       ├── decision_tools.py
│       ├── resource_tools.py
│       └── security_tools.py
└── routes/                      # API endpoints
    ├── agents.py
    ├── decisions.py
    ├── predictions.py
    └── metrics.py
```

## Troubleshooting

### Backend won't start

```bash
# Check if port 8000 is already in use
lsof -ti:8000 | xargs kill -9

# Try again
python run_backend.py
```

### WebSocket not connecting

1. Make sure backend is running on port 8000
2. Check browser console for connection errors
3. Verify CORS is enabled (already configured)

### Import errors

```bash
# Verify packages are installed
pip list | grep strands
pip list | grep fastapi

# If missing, they should auto-install via Replit
```

## Next Steps

1. ✅ **Start backend** - Open new terminal, run `python run_backend.py`
2. ✅ **Watch live updates** - Frontend dashboard shows real-time agent activity
3. ✅ **Explore API** - Visit http://localhost:8000/docs
4. ⏭️ **Add AWS Bedrock** - Configure credentials for real Claude Sonnet integration
5. ⏭️ **Customize agents** - Modify tools in `python_backend/agents/tools/`

---

**Built with Strands Agents + AWS Bedrock + FastAPI** 🚀
