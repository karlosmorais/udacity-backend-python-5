import boto3
try:
    print(boto3.client('sts').get_caller_identity()['Account'])
except Exception as e:
    print(e)
