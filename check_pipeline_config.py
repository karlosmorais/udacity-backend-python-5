import boto3
import sys
import json

client = boto3.client('codepipeline', region_name='us-east-2')
pipelines = client.list_pipelines()['pipelines']
pipeline_name = next((p['name'] for p in pipelines if 'simple-jwt-api' in p['name']), None)

if not pipeline_name:
    print("Pipeline not found!")
    sys.exit(1)

print(f"Checking pipeline {pipeline_name} config...")
response = client.get_pipeline(name=pipeline_name)
stages = response['pipeline']['stages']
source_stage = next(s for s in stages if s['name'] == 'Source')
action = source_stage['actions'][0]
config = action['configuration']
with open('pipeline_config.txt', 'w') as f:
    f.write(f"Owner: {config.get('Owner')}\n")
    f.write(f"Repo: {config.get('Repo')}\n")
    f.write(f"Branch: {config.get('Branch')}\n")
