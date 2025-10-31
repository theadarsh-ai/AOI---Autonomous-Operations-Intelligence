#!/usr/bin/env python
"""
Start the Python backend with Strands Agents
Run this in a separate terminal while the frontend runs
"""

import sys
import os

# Add python_backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python_backend'))

if __name__ == "__main__":
    import uvicorn
    from main import app
    
    print("=" * 60)
    print("🚀 MSP AI Orchestrator - Python Backend")
    print("=" * 60)
    print("📡 API Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    print("=" * 60)
    print()
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )
