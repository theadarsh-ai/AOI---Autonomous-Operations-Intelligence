#!/usr/bin/env python3
"""Test with inference profile format"""

import os
import json
import boto3
from botocore.config import Config

region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-2')
print(f"\n🔍 Testing Bedrock with Inference Profile")
print(f"Region: {region}\n")

# Check credentials
print("Credentials:")
print(f"  Access Key: {os.environ.get('AWS_ACCESS_KEY_ID', 'NOT SET')[:12]}...")
print(f"  Has Secret: {'Yes' if os.environ.get('AWS_SECRET_ACCESS_KEY') else 'No'}")
print(f"  Session Token: {'Yes' if os.environ.get('AWS_SESSION_TOKEN') else 'No'}\n")

try:
    config = Config(region_name=region)
    bedrock_runtime = boto3.client('bedrock-runtime', region_name=region)
    
    # Try inference profile format (us. prefix for US region)
    model_id = "us.anthropic.claude-3-5-sonnet-20240620-v1:0"
    print(f"Testing model: {model_id}\n")
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 50,
        "messages": [{"role": "user", "content": "Say 'Working!'"}]
    }
    
    print("📤 Invoking...")
    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        body=json.dumps(body)
    )
    
    result = json.loads(response['body'].read())
    print(f"✅ SUCCESS: {result['content'][0]['text']}\n")
    
except Exception as e:
    print(f"❌ Error: {e}\n")
    
    # Try listing what we CAN access
    print("Attempting to list available services...")
    try:
        sts = boto3.client('sts', region_name=region)
        identity = sts.get_caller_identity()
        print(f"\n✅ STS Working - Account: {identity.get('Account', 'Unknown')}")
        print(f"   User ARN: {identity.get('Arn', 'Unknown')}")
    except Exception as e2:
        print(f"❌ STS also failed: {e2}")
