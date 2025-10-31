#!/bin/bash

# Start Python backend
echo "🐍 Starting Python FastAPI backend on port 8000..."
python python_backend/main.py &

# Wait a moment for Python to start
sleep 2

# Start Node/React frontend
echo "⚛️  Starting React frontend on port 5000..."
npm run dev
