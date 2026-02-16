import boto3

iam = boto3.client('iam')
roles = iam.list_roles()
for role in roles['Roles']:
    if 'NodeInstanceRole' in role['RoleName'] and 'simple-jwt-api' in role['RoleName']:
        print(role['Arn'])
