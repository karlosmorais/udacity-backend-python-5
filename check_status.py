import boto3
import time
import subprocess
import sys

cf = boto3.client('cloudformation', region_name='us-east-2')
stack_name = 'simple-jwt-api-pipeline'

print("Waiting for stack to complete...")
while True:
    try:
        response = cf.describe_stacks(StackName=stack_name)
        status = response['Stacks'][0]['StackStatus']
        print(f"Status: {status}")
        
        if status in ['CREATE_COMPLETE', 'UPDATE_COMPLETE']:
            print("Stack creation complete!")
            break
        elif status in ['CREATE_FAILED', 'ROLLBACK_IN_PROGRESS', 'ROLLBACK_COMPLETE']:
            print("Stack creation failed!")
            sys.exit(1)
        
        time.sleep(10)
    except Exception as e:
        print(f"Error checking stack: {e}")
        time.sleep(10)

print("Getting Service IP...")
cmd = ['kubectl', 'get', 'services', 'simple-jwt-api', '-o', 'wide']
try:
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
except Exception as e:
    print(f"Error getting service: {e}")
