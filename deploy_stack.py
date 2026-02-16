import boto3
import time
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

cf = boto3.client('cloudformation', region_name='us-east-2')

stack_name = 'simple-jwt-api-pipeline'
template_body = open('ci-cd-codepipeline.cfn.yml', 'r').read()

params = [
    {
        'ParameterKey': 'GitHubToken',
        'ParameterValue': os.getenv('GITHUB_TOKEN')
    },
    {
        'ParameterKey': 'GitHubUser',
        'ParameterValue': os.getenv('GITHUB_USER')
    },
    {
        'ParameterKey': 'GitSourceRepo',
        'ParameterValue': os.getenv('GITHUB_REPO')
    },
    {
        'ParameterKey': 'GitBranch',
        'ParameterValue': os.getenv('GITHUB_BRANCH')
    }
]

try:
    print(f"Creating stack {stack_name}...")
    response = cf.create_stack(
        StackName=stack_name,
        TemplateBody=template_body,
        Parameters=params,
        Capabilities=['CAPABILITY_IAM']
    )
    print(f"Stack creation initiated: {response['StackId']}")
except cf.exceptions.AlreadyExistsException:
    print(f"Stack {stack_name} already exists. Updating...")
    try:
        response = cf.update_stack(
            StackName=stack_name,
            TemplateBody=template_body,
            Parameters=params,
            Capabilities=['CAPABILITY_IAM']
        )
        print(f"Stack update initiated: {response['StackId']}")
    except Exception as e:
        print(f"Update failed (might be no changes): {e}")
except Exception as e:
    print(f"Error: {e}")
