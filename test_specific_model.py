#!/usr/bin/env python3
"""Test specific Claude 3 Sonnet model"""

import os
import json
import boto3
from botocore.config import Config

model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')

print(f"\n🔍 Testing: {model_id}")
print(f"Region: {region}\n")

try:
    config = Config(region_name=region)
    bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 100,
        "messages": [{"role": "user", "content": "Say 'Working!' and confirm your model name."}]
    }
    
    print("📤 Invoking model...")
    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    
    result = json.loads(response['body'].read())
    text = result['content'][0]['text']
    
    print(f"✅ SUCCESS!\n")
    print(f"Response: {text}\n")
    print(f"Model ID: {model_id}")
    print(f"Region: {region}")
    
except Exception as e:
    print(f"❌ FAILED: {e}\n")
    
    # Check what models ARE available
    print("Checking available Claude 3 models in your region...")
    try:
        bedrock = boto3.client('bedrock', region_name=region)
        response = bedrock.list_foundation_models()
        
        claude3_models = [
            m for m in response.get('modelSummaries', [])
            if 'claude-3' in m.get('modelId', '').lower()
            and 'sonnet' in m.get('modelId', '').lower()
        ]
        
        if claude3_models:
            print("\n✅ Available Claude 3 Sonnet models:")
            for m in sorted(claude3_models, key=lambda x: x.get('modelId', '')):
                print(f"   - {m.get('modelId')}")
        else:
            print("\n❌ No Claude 3 Sonnet models found in this region")
            
    except Exception as e2:
        print(f"Could not list models: {e2}")
