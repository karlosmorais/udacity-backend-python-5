import boto3
import sys

client = boto3.client('codepipeline', region_name='us-east-2')
pipelines = client.list_pipelines()['pipelines']
pipeline_name = next((p['name'] for p in pipelines if 'simple-jwt-api' in p['name']), None)

if not pipeline_name:
    print("Pipeline not found!")
    sys.exit(1)

print(f"Checking errors for {pipeline_name}...")
response = client.list_action_executions(pipelineName=pipeline_name, maxResults=5)
for action_exec in response['actionExecutionDetails']:
    if action_exec['status'] == 'Failed':
        print(f"Action: {action_exec['actionName']}")
        print(f"Stage: {action_exec['stageName']}")
        print(f"Error: {action_exec['output']['executionResult']['externalExecutionSummary']}")
        break
