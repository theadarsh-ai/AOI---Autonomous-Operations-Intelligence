#!/usr/bin/env python3
"""
Test AWS Bedrock connection with Claude 3 Sonnet
Model ID: anthropic.claude-3-sonnet-20240229-v1:0
"""

import os
import sys
import json
import boto3
from botocore.config import Config

def print_header(title):
    """Print formatted section header"""
    print("\n" + "=" * 60)
    print(f"🔍 {title}")
    print("=" * 60)

def test_credentials():
    """Test if AWS credentials are configured"""
    print_header("AWS Credentials Check")
    
    keys = {
        'AWS_ACCESS_KEY_ID': os.environ.get('AWS_ACCESS_KEY_ID'),
        'AWS_SECRET_ACCESS_KEY': os.environ.get('AWS_SECRET_ACCESS_KEY'),
        'AWS_DEFAULT_REGION': os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    }
    
    for key, value in keys.items():
        if value:
            masked = f"{'*' * 8}{value[-4:]}" if len(value) > 4 else "****"
            print(f"✅ {key}: {masked}")
        else:
            print(f"❌ {key}: NOT SET")
            return False
    
    return True

def test_bedrock_model():
    """Test Claude 3 Sonnet model invocation"""
    print_header("Testing Claude 3 Sonnet Model")
    
    model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
    region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    
    print(f"Model ID: {model_id}")
    print(f"Region: {region}")
    print("")
    
    try:
        # Create Bedrock Runtime client
        config = Config(
            region_name=region,
            retries={'max_attempts': 3, 'mode': 'adaptive'}
        )
        
        kwargs = {
            'aws_access_key_id': os.environ.get('AWS_ACCESS_KEY_ID'),
            'aws_secret_access_key': os.environ.get('AWS_SECRET_ACCESS_KEY'),
            'config': config
        }
        
        if os.environ.get('AWS_SESSION_TOKEN'):
            kwargs['aws_session_token'] = os.environ.get('AWS_SESSION_TOKEN')
        
        bedrock_runtime = boto3.client('bedrock-runtime', **kwargs)
        print("✅ Bedrock Runtime client created")
        
        # Prepare request body
        body = {
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 256,
            "temperature": 0.7,
            "messages": [
                {
                    "role": "user",
                    "content": "Say 'Hello from AWS Bedrock!' and confirm you are Claude 3 Sonnet running on AWS."
                }
            ]
        }
        
        print(f"📤 Invoking model...")
        print("")
        
        # Invoke model
        response = bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        # Parse response
        response_body = json.loads(response['body'].read())
        text = response_body['content'][0]['text']
        usage = response_body.get('usage', {})
        stop_reason = response_body.get('stop_reason', 'N/A')
        
        print("✅ Model invocation successful!")
        print(f"\n📥 Claude's Response:\n")
        print(f"{text}\n")
        print(f"Token usage:")
        print(f"  - Input tokens: {usage.get('input_tokens', 0)}")
        print(f"  - Output tokens: {usage.get('output_tokens', 0)}")
        print(f"  - Stop reason: {stop_reason}")
        
        return True
        
    except Exception as e:
        error_message = str(e)
        print(f"❌ Model invocation failed!")
        print(f"\nError: {error_message}\n")
        
        # Provide helpful troubleshooting
        if "ResourceNotFoundException" in error_message or "ValidationException" in error_message:
            print("💡 Troubleshooting:")
            print("  1. Verify model access is enabled in AWS Console")
            print("  2. Go to: AWS Bedrock → Model Access")
            print("  3. Request access to 'Anthropic Claude 3 Sonnet'")
            print("  4. Wait for approval (usually instant)")
            print(f"  5. Ensure model is available in region: {region}")
        elif "AccessDeniedException" in error_message:
            print("💡 Troubleshooting:")
            print("  1. Check IAM permissions include 'bedrock:InvokeModel'")
            print("  2. Verify credentials have Bedrock access")
        
        return False

def main():
    """Run all tests"""
    print("\n╔" + "=" * 58 + "╗")
    print("║" + " " * 5 + "AWS BEDROCK - CLAUDE 3 SONNET TEST" + " " * 18 + "║")
    print("╚" + "=" * 58 + "╝")
    
    # Test credentials
    if not test_credentials():
        print("\n❌ AWS credentials not properly configured")
        sys.exit(1)
    
    # Test model
    model_ok = test_bedrock_model()
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 Test Summary")
    print("=" * 60)
    
    if model_ok:
        print("✅ PASS - AWS Bedrock with Claude 3 Sonnet is working!")
        print("\n🎉 Your MSP AI agents can now use real Claude intelligence!")
        sys.exit(0)
    else:
        print("❌ FAIL - Claude model is not accessible")
        print("\n⚠️  System will continue using simulation mode")
        sys.exit(1)

if __name__ == "__main__":
    main()
