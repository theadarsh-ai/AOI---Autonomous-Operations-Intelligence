# 🧪 Testing Guide - MSP AI Orchestrator

## Quick Test: See It Running in 30 Seconds

### Step 1: Verify Frontend is Running
The React dashboard should already be running. Check the Webview tab or visit the URL shown in the output.

### Step 2: Start Python Backend
Open a **new terminal** (Shell tab) and run:
```bash
python run_backend.py
```

Wait for:
```
✅ Strands Agents initialized successfully
INFO: Uvicorn running on http://0.0.0.0:8000
```

### Step 3: Watch the Magic! ✨

In the React dashboard, you should see:

1. **Connection Status** (top right) → Changes from ⚠️ to 🟢 "Live"
2. **Agent Cards** → Start updating every few seconds with new tasks
3. **Live Decision Feed** → New autonomous decisions appear in real-time
4. **Metrics** → Numbers change as agents make decisions
5. **Predictions** → Timeline updates with new forecasts

---

## What You're Seeing: Autonomous AI in Action

### The Autonomous Workflow (Happens Every 5-10 Seconds)

```
┌─────────────────────────────────────────────────┐
│  1. PREDICTIVE MONITORING AGENT                 │
│  Analyzes 847 servers, 23TB data                │
│  🔍 Detects: CPU spike on DB-PROD-03            │
│  📊 Predicts: 84% chance of failure in 36 hrs   │
│  💰 Calculates: $25K business impact            │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  2. AUTONOMOUS DECISION AGENT                   │
│  Evaluates: Preventive action vs. wait          │
│  💵 ROI Calculation: 15:1 ($800 fix vs $12K)    │
│  ✅ Auto-Approves: Level 1 autonomy             │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  3. RESOURCE OPTIMIZATION AGENT                 │
│  Finds: Sarah Chen (99% match, available)       │
│  ⏰ Schedules: Preventive maintenance           │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  4. EXECUTION (Automatic)                       │
│  📧 Tech assigned → Work order created          │
│  🛠️ Maintenance performed → Issue prevented     │
└──────────────────┬──────────────────────────────┘
                   ↓
┌─────────────────────────────────────────────────┐
│  5. LEARNING & ADAPTATION AGENT                 │
│  Records: Prediction accurate → Model improves  │
│  📈 Accuracy: 87% → 89%                         │
└─────────────────────────────────────────────────┘
```

All of this happens **without human intervention**!

---

## Testing Each Component

### Test 1: WebSocket Connection

**Expected Behavior:**
- Connection status badge shows 🟢 green when backend is running
- Shows "Live" in the last update timestamp
- Console shows: `✅ WebSocket connected to Python backend`

**If Connection Fails:**
```bash
# Check backend is running on port 8000
curl http://localhost:8000/api/health

# Check for errors in backend terminal
# Common issue: Port 8000 already in use
lsof -ti:8000 | xargs kill -9
python run_backend.py
```

---

### Test 2: Real-Time Agent Updates

**What to Watch:**
1. Open the **Agents** tab in the dashboard
2. Watch each agent card
3. Every 5-10 seconds, you should see:
   - Status changes (🟢 Active, 🔄 Processing, etc.)
   - Active Tasks count updates
   - Decisions/hour increments
   - Uptime increases

**Backend Logs to Verify:**
```bash
# In the terminal running the backend, look for:
INFO:agents.strands_orchestrator:🤖 Master Orchestrator: Starting autonomous operation...
INFO:agents.strands_orchestrator:[Agent: predictive_monitoring] Analyzing system metrics...
INFO:agents.strands_orchestrator:[Agent: decision_maker] Evaluating action approval...
```

---

### Test 3: Autonomous Decision Making

**What to Watch:**
1. Go to **Overview** tab
2. Look at the **Live Decision Feed** (right side)
3. Every few seconds, a new decision should appear at the top

**Decision Anatomy:**
```
🔵 Predictive Monitoring • 2s ago
Level 1 Autonomy (Auto-Approved)

Schedule preventive maintenance for DB-PROD-03 
CPU spike detected (84% failure probability)

Cost: $800 | ROI: 15:1
```

**Verify 3 Autonomy Levels:**
- **Level 1** (Green badge): Auto-approved, executed immediately
- **Level 2** (Yellow badge): Supervisor notified, auto-execute after 15min
- **Level 3** (Red badge): Requires human approval

---

### Test 4: Predictions Timeline

**What to Watch:**
1. Go to **Predictions** tab
2. Should see 6-8 predictions sorted by timeframe
3. Each prediction shows:
   - 🔴 Type (outage, performance, cost, security)
   - Probability (%)
   - Time until event (e.g., "36 hours")
   - Preventive cost vs. Failure cost

**Example:**
```
🔴 Outage Prediction
84% probability • 36 hours

DB-PROD-03 expected failure
Business Impact: Critical

Preventive: $800 | Failure: $12,500
```

---

### Test 5: Real-Time Metrics

**What to Watch:**
1. Stay on **Overview** tab
2. Watch the 4 metric cards at the top
3. As decisions are made, metrics update:
   - **Autonomous Actions**: Should stay ~95%
   - **Prevention Savings**: Increases as preventive actions succeed
   - **Prediction Accuracy**: Improves as learning agent updates models
   - **Active Incidents**: Changes as incidents are detected/resolved

---

### Test 6: API Endpoints

Test the backend APIs directly:

```bash
# System health
curl http://localhost:8000/api/health

# Get all agents
curl http://localhost:8000/api/agents | python -m json.tool

# Get recent decisions
curl http://localhost:8000/api/decisions | python -m json.tool

# Get predictions
curl http://localhost:8000/api/predictions | python -m json.tool

# Get metrics
curl http://localhost:8000/api/metrics | python -m json.tool
```

**Expected Response Format:**
```json
{
  "agents": [
    {
      "id": "predictive_monitoring",
      "name": "Predictive Monitoring",
      "status": "active",
      "active_tasks": 3,
      "decisions_per_hour": 12,
      "accuracy": 89,
      "uptime": "99.8%"
    }
  ]
}
```

---

### Test 7: Interactive API Documentation

Visit: **http://localhost:8000/docs**

This opens Swagger UI where you can:
1. See all available endpoints
2. Test each endpoint with sample data
3. View request/response schemas
4. Try the WebSocket endpoint

---

## Performance Testing

### Expected Performance Benchmarks

- **WebSocket Latency**: < 50ms for updates
- **Decision Frequency**: 1 decision every 5-10 seconds
- **Frontend Re-render**: Smooth, no lag
- **Memory Usage**: 
  - Frontend: ~50-80MB
  - Backend: ~100-150MB (simulation mode)

### Monitor Resource Usage

```bash
# Backend memory/CPU
top -p $(pgrep -f "python.*main.py")

# Frontend (check browser dev tools)
# Performance → Memory → Take snapshot
```

---

## AWS Bedrock Integration Testing (Optional)

### Prerequisites
1. AWS account with Bedrock access
2. Claude Sonnet 4 enabled in AWS console
3. Valid AWS credentials

### Setup
Add to Replit Secrets:
```
AWS_ACCESS_KEY_ID = your_key
AWS_SECRET_ACCESS_KEY = your_secret
AWS_DEFAULT_REGION = us-west-2
```

### Restart Backend
```bash
# Stop current backend (Ctrl+C)
python run_backend.py
```

### Expected Output
```
✅ AWS credentials detected - Bedrock integration enabled
✅ Using AWS Bedrock with Claude Sonnet
INFO: Strands Agents using real AWS Bedrock API
```

### Verify Bedrock is Active
```bash
# Check backend logs for actual API calls
# Look for:
INFO:strands_agents: Calling Bedrock API for agent: predictive_monitoring
INFO:strands_agents: Received response from Claude Sonnet (213 tokens)
```

### What Changes with Bedrock?
- **Simulation Mode**: Uses pre-defined decision logic
- **Bedrock Mode**: 
  - Claude Sonnet actually analyzes real metrics
  - Generates intelligent, context-aware decisions
  - Learns from historical patterns
  - Provides natural language explanations

---

## Common Issues & Solutions

### Issue: WebSocket Won't Connect

**Symptoms:**
- Connection status stays red
- "Reconnecting in Xms..." keeps appearing
- Console shows: `WebSocket error`

**Solutions:**
```bash
# 1. Verify backend is running
curl http://localhost:8000/api/health

# 2. Check port 8000 isn't blocked
lsof -ti:8000

# 3. Restart backend
pkill -f "python.*main.py"
python run_backend.py

# 4. Clear browser cache and refresh
```

---

### Issue: No Live Updates Appearing

**Symptoms:**
- WebSocket connected (green badge)
- But agent cards/decisions don't update

**Solutions:**
1. Check browser console for errors
2. Verify backend orchestrator is running:
   ```bash
   # Should see logs every few seconds
   tail -f /tmp/python_backend.log
   ```
3. Test WebSocket directly:
   ```javascript
   // In browser console
   const ws = new WebSocket('ws://localhost:8000/ws');
   ws.onmessage = (e) => console.log('Received:', e.data);
   ```

---

### Issue: Backend Crashes or Won't Start

**Symptoms:**
- Import errors
- Module not found
- Port in use

**Solutions:**
```bash
# 1. Verify Python packages installed
pip list | grep -E "(strands|fastapi|uvicorn)"

# 2. Kill conflicting process
lsof -ti:8000 | xargs kill -9

# 3. Check Python version (needs 3.10+)
python --version

# 4. Reinstall dependencies if needed
pip install -r python_backend/requirements.txt
```

---

## Success Criteria Checklist

✅ **MVP Complete** when you can verify:

- [ ] Frontend loads without errors
- [ ] Backend starts successfully
- [ ] WebSocket connection established (green badge)
- [ ] At least one agent card shows live updates
- [ ] At least one decision appears in live feed
- [ ] Metrics update in real-time
- [ ] All 8 agents visible in Agents tab
- [ ] Predictions tab shows predictive timeline
- [ ] API endpoints respond correctly
- [ ] No console errors in browser

🎯 **Production Ready** when you add:
- [ ] AWS Bedrock credentials configured
- [ ] All agents using real Claude Sonnet
- [ ] Integration tests passing
- [ ] Load testing completed
- [ ] Documentation reviewed

---

## Next Steps After Testing

1. ✅ **Customize Agent Behavior**
   - Edit `python_backend/agents/tools/*.py`
   - Add your own decision logic
   - Modify predictive models

2. ✅ **Connect Real Data Sources**
   - Replace mock metrics with actual monitoring data
   - Integrate with your MSP tools (ConnectWise, AutoTask, etc.)
   - Add real client/server data

3. ✅ **Extend Frontend**
   - Add more visualizations
   - Create admin panel for agent configuration
   - Build client-specific dashboards

4. ✅ **Deploy to Production**
   - Use Replit Deployments (publish button)
   - Or export to AWS/Azure/GCP
   - Configure production database

---

**Questions? Issues?**
Check the logs, API docs, or backend terminal output for debugging clues!
