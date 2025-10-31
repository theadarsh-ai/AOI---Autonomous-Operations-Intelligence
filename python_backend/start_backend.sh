#!/bin/bash

echo "🐍 Starting Python FastAPI backend with Strands Agents..."
echo "📡 Backend will run on http://0.0.0.0:8000"
echo "📚 API docs available at http://0.0.0.0:8000/docs"
echo ""

# Check for AWS credentials
if [ -n "$AWS_ACCESS_KEY_ID" ] && [ -n "$AWS_SECRET_ACCESS_KEY" ]; then
    echo "✅ AWS credentials detected - Bedrock integration enabled"
else
    echo "💡 AWS credentials not found - Running in simulation mode"
    echo "   To enable Bedrock: Add AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION to Secrets"
fi

echo ""
echo "Starting FastAPI server..."
python python_backend/main.py
