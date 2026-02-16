import boto3
import sys

client = boto3.client('codepipeline', region_name='us-east-2')
# pipeline_name = 'simple-jwt-api-pipeline-CodePipelineGitHub-70azaouEXHN'
pipelines = client.list_pipelines()['pipelines']
pipeline_name = next((p['name'] for p in pipelines if 'simple-jwt-api' in p['name']), None)

if not pipeline_name:
    print("Pipeline not found!")
    sys.exit(1)

print(f"Starting pipeline {pipeline_name}...")
try:
    client.start_pipeline_execution(name=pipeline_name)
    print("Execution started.")
except Exception as e:
    print(f"Error starting execution: {e}")
