#!/bin/bash
echo "🔍 Checking if backend is serving LIVE AWS data..."
echo ""
curl -s http://localhost:8000/api/health 2>&1 | python -m json.tool
echo ""
echo "If you see 'bedrock_enabled: true' above, you have LIVE data!"
echo "If curl fails, run: python run_backend.py"
