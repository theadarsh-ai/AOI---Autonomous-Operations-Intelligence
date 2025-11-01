#!/usr/bin/env python3
"""
List all available Bedrock models in your AWS region
"""

import os
import boto3
from botocore.config import Config

def list_models():
    """List all available Bedrock models"""
    region = os.environ.get('AWS_DEFAULT_REGION', 'us-east-1')
    
    print(f"\n🔍 Listing Bedrock models in region: {region}\n")
    
    try:
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
        
        bedrock = boto3.client('bedrock', **kwargs)
        
        # List foundation models
        response = bedrock.list_foundation_models()
        
        # Filter for Anthropic Claude models
        claude_models = [
            model for model in response.get('modelSummaries', [])
            if 'anthropic' in model.get('modelId', '').lower()
            and 'claude' in model.get('modelId', '').lower()
        ]
        
        if not claude_models:
            print("❌ No Claude models found in this region")
            return
        
        print(f"✅ Found {len(claude_models)} Claude models:\n")
        
        for model in sorted(claude_models, key=lambda x: x.get('modelId', '')):
            model_id = model.get('modelId', 'Unknown')
            model_name = model.get('modelName', 'Unknown')
            provider = model.get('providerName', 'Unknown')
            
            # Check if it's Claude 3 Sonnet
            is_sonnet = 'sonnet' in model_id.lower()
            marker = "🎯" if is_sonnet else "  "
            
            print(f"{marker} {model_id}")
            print(f"   Name: {model_name}")
            print(f"   Provider: {provider}")
            
            # Show inference types if available
            if 'inferenceTypesSupported' in model:
                types = ', '.join(model['inferenceTypesSupported'])
                print(f"   Inference: {types}")
            
            print()
        
        # Highlight recommendation
        print("=" * 60)
        print("💡 Recommended models (marked with 🎯 above):")
        print("=" * 60)
        
        for model in claude_models:
            model_id = model.get('modelId', '')
            if 'sonnet' in model_id.lower():
                print(f"✅ {model_id}")
        
    except Exception as e:
        print(f"❌ Error listing models: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    list_models()
