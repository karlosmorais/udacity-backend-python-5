import boto3
import time
import sys

client = boto3.client('codepipeline', region_name='us-east-2')
# pipeline_name = 'simple-jwt-api-pipeline-CodePipelineGitHub-70azaouEXHN'
pipelines = client.list_pipelines()['pipelines']
pipeline_name = next((p['name'] for p in pipelines if 'simple-jwt-api' in p['name']), None)

if not pipeline_name:
    print("Pipeline not found!")
    sys.exit(1)

print(f"Checking pipeline {pipeline_name}...")

while True:
    try:
        response = client.get_pipeline_state(name=pipeline_name)
        stage_states = response['stageStates']
        
        all_succeeded = True
        for stage in stage_states:
            name = stage['stageName']
            action_states = stage['actionStates']
            latest_execution = action_states[0].get('latestExecution', {})
            status = latest_execution.get('status', 'Unknown')
            print(f"Stage {name}: {status}")
            
            if status == 'Failed':
                print("Pipeline failed!")
                sys.exit(1)
            if status != 'Succeeded':
                all_succeeded = False
        
        if all_succeeded:
            print("Pipeline execution complete!")
            break
            
        time.sleep(10)
    except Exception as e:
        print(f"Error: {e}")
        time.sleep(10)
