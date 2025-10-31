#!/bin/bash

# MSP AI Orchestrator - Start Both Frontend and Backend Services
# This script runs the Node.js frontend (port 5000) and Python backend (port 8000) together

set -e

echo "================================================================================"
echo "🚀 Starting MSP AI Orchestrator - Full Stack Application"
echo "================================================================================"
echo "📦 Frontend: Node.js + React + Vite (port 5000)"
echo "🐍 Backend: Python + FastAPI + AWS Bedrock (port 8000)"
echo "================================================================================"
echo ""

# Trap SIGINT and SIGTERM to gracefully shutdown both services
cleanup() {
    echo ""
    echo "🛑 Shutting down services..."
    kill -TERM $FRONTEND_PID $BACKEND_PID 2>/dev/null || true
    wait
    echo "✅ All services stopped"
    exit 0
}

trap cleanup SIGINT SIGTERM EXIT

# Start Python backend in background
echo "🐍 Starting Python FastAPI backend on port 8000..."
python -u run_backend.py &
BACKEND_PID=$!
echo "   Backend PID: $BACKEND_PID"

# Give backend a moment to initialize
sleep 2

# Start Node.js frontend in background
echo "📦 Starting Node.js frontend on port 5000..."
npm run dev &
FRONTEND_PID=$!
echo "   Frontend PID: $FRONTEND_PID"

echo ""
echo "================================================================================"
echo "✅ Both services started successfully!"
echo "================================================================================"
echo "🌐 Frontend: http://localhost:5000"
echo "🔌 Backend API: http://localhost:8000"
echo "📡 WebSocket: ws://localhost:8000/ws"
echo "================================================================================"
echo ""
echo "🟢 Waiting for services... (Press Ctrl+C to stop)"
echo ""

# Wait for either process to exit
wait -n

# If we get here, one process died - kill the other and exit
echo "⚠️  One service died, stopping all services..."
kill -TERM $FRONTEND_PID $BACKEND_PID 2>/dev/null || true
wait
exit 1
