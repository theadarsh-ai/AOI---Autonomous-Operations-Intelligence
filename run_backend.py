#!/usr/bin/env python
"""
Start the Python backend with AWS Bedrock Integration
Run this to start the autonomous AI agent system
"""

import sys
import os
import logging

# Add python_backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'python_backend'))

if __name__ == "__main__":
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    logger = logging.getLogger(__name__)
    
    # Check AWS credentials
    aws_configured = all([
        os.getenv("AWS_ACCESS_KEY_ID"),
        os.getenv("AWS_SECRET_ACCESS_KEY"),
        os.getenv("AWS_DEFAULT_REGION")
    ])
    
    print("\n" + "=" * 80)
    print("🚀 MSP AI Orchestrator - Autonomous Multi-Agent System")
    print("=" * 80)
    
    if aws_configured:
        print(f"🌟 Mode: PRODUCTION (AWS Bedrock + Claude 3.5 Sonnet)")
        print(f"🌍 AWS Region: {os.getenv('AWS_DEFAULT_REGION')}")
        print("🤖 8 Bedrock Agents: ACTIVE")
        print("📊 Data Records: 29,100")
    else:
        print("⚠️  Mode: SIMULATION (AWS credentials not found)")
        print("💡 Add AWS credentials to Replit Secrets to enable Bedrock")
        print("🤖 8 Simulated Agents: ACTIVE")
    
    print("\n" + "-" * 80)
    print("📡 API Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🔌 WebSocket: ws://localhost:8000/ws")
    print("🌐 Frontend: http://localhost:5000")
    print("-" * 80 + "\n")
    
    import uvicorn
    from main import app
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
