"""
AWS Configuration and Client Management
Handles all AWS service connections for the MSP AI Orchestrator
"""

import os
import boto3
from botocore.config import Config
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)

class AWSClients:
    """Centralized AWS client management with credentials from environment"""
    
    def __init__(self):
        # Get credentials from environment variables (Replit Secrets)
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
        self.aws_region = os.getenv('AWS_DEFAULT_REGION', 'us-east-1')
        
        if not all([self.aws_access_key_id, self.aws_secret_access_key]):
            raise ValueError("AWS credentials not found in environment variables!")
        
        # Configure boto3 with retry logic
        self.config = Config(
            region_name=self.aws_region,
            retries={'max_attempts': 3, 'mode': 'adaptive'}
        )
        
        logger.info(f"✅ AWS Configuration loaded for region: {self.aws_region}")
        
        # Initialize clients
        self._bedrock_runtime = None
        self._bedrock_agent = None
        self._bedrock_agent_runtime = None
        self._dynamodb = None
        self._s3 = None
        self._lambda_client = None
        self._eventbridge = None
    
    @property
    def bedrock_runtime(self):
        """Bedrock Runtime for direct model invocation"""
        if self._bedrock_runtime is None:
            self._bedrock_runtime = boto3.client(
                'bedrock-runtime',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                config=self.config
            )
            logger.info("✅ Bedrock Runtime client initialized")
        return self._bedrock_runtime
    
    @property
    def bedrock_agent(self):
        """Bedrock Agent for agent management"""
        if self._bedrock_agent is None:
            self._bedrock_agent = boto3.client(
                'bedrock-agent',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                config=self.config
            )
            logger.info("✅ Bedrock Agent client initialized")
        return self._bedrock_agent
    
    @property
    def bedrock_agent_runtime(self):
        """Bedrock Agent Runtime for invoking agents"""
        if self._bedrock_agent_runtime is None:
            self._bedrock_agent_runtime = boto3.client(
                'bedrock-agent-runtime',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                config=self.config
            )
            logger.info("✅ Bedrock Agent Runtime client initialized")
        return self._bedrock_agent_runtime
    
    @property
    def dynamodb(self):
        """DynamoDB for operational data storage"""
        if self._dynamodb is None:
            self._dynamodb = boto3.resource(
                'dynamodb',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                config=self.config
            )
            logger.info("✅ DynamoDB client initialized")
        return self._dynamodb
    
    @property
    def s3(self):
        """S3 for document and data storage"""
        if self._s3 is None:
            self._s3 = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                config=self.config
            )
            logger.info("✅ S3 client initialized")
        return self._s3
    
    @property
    def lambda_client(self):
        """Lambda for action group functions"""
        if self._lambda_client is None:
            self._lambda_client = boto3.client(
                'lambda',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                config=self.config
            )
            logger.info("✅ Lambda client initialized")
        return self._lambda_client
    
    @property
    def eventbridge(self):
        """EventBridge for event-driven workflows"""
        if self._eventbridge is None:
            self._eventbridge = boto3.client(
                'events',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                config=self.config
            )
            logger.info("✅ EventBridge client initialized")
        return self._eventbridge
    
    def test_connection(self) -> Dict[str, Any]:
        """Test AWS connection and permissions"""
        results = {
            'region': self.aws_region,
            'services': {}
        }
        
        try:
            # Test Bedrock Runtime
            models = self.bedrock_runtime.list_foundation_models()
            results['services']['bedrock_runtime'] = {
                'status': 'connected',
                'models_available': len(models.get('modelSummaries', []))
            }
        except Exception as e:
            results['services']['bedrock_runtime'] = {'status': 'error', 'error': str(e)}
        
        try:
            # Test DynamoDB
            tables = list(self.dynamodb.tables.all())
            results['services']['dynamodb'] = {
                'status': 'connected',
                'tables_count': len(tables)
            }
        except Exception as e:
            results['services']['dynamodb'] = {'status': 'error', 'error': str(e)}
        
        try:
            # Test S3
            buckets = self.s3.list_buckets()
            results['services']['s3'] = {
                'status': 'connected',
                'buckets_count': len(buckets.get('Buckets', []))
            }
        except Exception as e:
            results['services']['s3'] = {'status': 'error', 'error': str(e)}
        
        return results


# Global AWS clients instance
aws_clients: Optional[AWSClients] = None

def get_aws_clients() -> AWSClients:
    """Get or create global AWS clients instance"""
    global aws_clients
    if aws_clients is None:
        aws_clients = AWSClients()
    return aws_clients


def invoke_claude(
    prompt: str,
    model_id: str = "anthropic.claude-3-5-sonnet-20241022-v2:0",
    max_tokens: int = 4096,
    temperature: float = 0.7
) -> Dict[str, Any]:
    """
    Invoke Claude 3.5 Sonnet via AWS Bedrock
    
    Args:
        prompt: The input prompt
        model_id: Bedrock model ID
        max_tokens: Maximum tokens to generate
        temperature: Sampling temperature
        
    Returns:
        Response dictionary with generated text
    """
    clients = get_aws_clients()
    
    body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": max_tokens,
        "temperature": temperature,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    try:
        response = clients.bedrock_runtime.invoke_model(
            modelId=model_id,
            body=json.dumps(body)
        )
        
        response_body = json.loads(response['body'].read())
        
        return {
            'success': True,
            'text': response_body['content'][0]['text'],
            'stop_reason': response_body.get('stop_reason'),
            'usage': response_body.get('usage', {})
        }
    except Exception as e:
        logger.error(f"Error invoking Claude: {e}")
        return {
            'success': False,
            'error': str(e)
        }


import json
