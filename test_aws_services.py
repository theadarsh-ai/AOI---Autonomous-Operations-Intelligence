#!/usr/bin/env python3
"""Quick AWS Services Health Check"""

import os
import json
import boto3
from botocore.config import Config

def test_bedrock():
    """Test Bedrock Runtime with available Claude model"""
    region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-2')
    
    print("🔍 Testing AWS Bedrock Service\n")
    print(f"Region: {region}")
    
    try:
        config = Config(region_name=region, retries={'max_attempts': 3, 'mode': 'adaptive'})
        
        kwargs = {
            'aws_access_key_id': os.environ.get('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.environ.get('AWS_SECRET_ACCESS_KEY'),
            'config': config
        }
        
        if os.environ.get('AWS_SESSION_TOKEN'):
            kwargs['aws_session_token'] = os.environ.get('AWS_SESSION_TOKEN')
        
        bedrock_runtime = boto3.client('bedrock-runtime', **kwargs)
        
        # Use Claude 3.5 Sonnet v2 (available in us-east-2)
        model_id = "anthropic.claude-3-5-sonnet-20241022-v2:0"
        print(f"Model: {model_id}\n")
        
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [{"role": "user", "content": "Reply with: AWS Bedrock is working!"}]
        }
        
        print("📤 Invoking Claude model...")
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        result = json.loads(response['body'].read())
        text = result['content'][0]['text']
        
        print(f"✅ SUCCESS!\n")
        print(f"Response: {text}\n")
        print(f"Tokens used: {result.get('usage', {})}")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_dynamodb():
    """Test DynamoDB"""
    print("\n🔍 Testing DynamoDB Service\n")
    
    try:
        region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-2')
        config = Config(region_name=region)
        
        kwargs = {
            'aws_access_key_id': os.environ.get('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.environ.get('AWS_SECRET_ACCESS_KEY'),
            'config': config
        }
        
        dynamodb = boto3.client('dynamodb', **kwargs)
        response = dynamodb.list_tables()
        
        tables = response.get('TableNames', [])
        print(f"✅ SUCCESS! Found {len(tables)} tables")
        if tables:
            print(f"Tables: {', '.join(tables)}")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

def test_s3():
    """Test S3"""
    print("\n🔍 Testing S3 Service\n")
    
    try:
        region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-2')
        config = Config(region_name=region)
        
        kwargs = {
            'aws_access_key_id': os.environ.get('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.environ.get('AWS_SECRET_ACCESS_KEY'),
            'config': config
        }
        
        s3 = boto3.client('s3', **kwargs)
        response = s3.list_buckets()
        
        buckets = response.get('Buckets', [])
        print(f"✅ SUCCESS! Found {len(buckets)} buckets")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False

if __name__ == "__main__":
    print("\n" + "="*60)
    print("AWS SERVICES HEALTH CHECK")
    print("="*60 + "\n")
    
    bedrock_ok = test_bedrock()
    dynamodb_ok = test_dynamodb()
    s3_ok = test_s3()
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Bedrock (AI Models): {'✅ WORKING' if bedrock_ok else '❌ FAILED'}")
    print(f"DynamoDB (Database): {'✅ WORKING' if dynamodb_ok else '❌ FAILED'}")
    print(f"S3 (Storage):        {'✅ WORKING' if s3_ok else '❌ FAILED'}")
    print("="*60 + "\n")
    
    if bedrock_ok and dynamodb_ok and s3_ok:
        print("🎉 All AWS services are working!\n")
    else:
        print("⚠️  Some AWS services have issues\n")
