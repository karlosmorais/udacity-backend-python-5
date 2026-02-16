import boto3
import sys
import json

client = boto3.client('codepipeline', region_name='us-east-2')
pipelines = client.list_pipelines()['pipelines']
pipeline_name = next((p['name'] for p in pipelines if 'simple-jwt-api' in p['name']), None)

if not pipeline_name:
    print("Pipeline not found!")
    sys.exit(1)

print(f"Checking executions for {pipeline_name}...")
response = client.list_pipeline_executions(pipelineName=pipeline_name, maxResults=5)
with open('pipeline_status.txt', 'w') as f:
    for execution in response['pipelineExecutionSummaries']:
        f.write(f"ID: {execution['pipelineExecutionId']}\n")
        f.write(f"Status: {execution['status']}\n")
        f.write(f"Start: {execution['startTime']}\n")
        f.write("-" * 20 + "\n")
