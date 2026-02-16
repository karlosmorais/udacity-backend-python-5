import boto3
import json

iam = boto3.client('iam')
role_name = 'UdacityFlaskDeployCBKubectlRole'

try:
    with open('trust.json', 'r') as f:
        trust_policy = json.load(f)
    
    try:
        iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        print(f"Role {role_name} created.")
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"Role {role_name} already exists.")

    with open('iam-role-policy.json', 'r') as f:
        policy_doc = json.load(f)

    iam.put_role_policy(
        RoleName=role_name,
        PolicyName='eks-describe',
        PolicyDocument=json.dumps(policy_doc)
    )
    print("Policy attached.")

except Exception as e:
    print(f"Error: {e}")

ssm = boto3.client('ssm')
try:
    ssm.put_parameter(
        Name='JWT_SECRET',
        Value='myjwtsecret',
        Type='SecureString',
        Overwrite=True
    )
    print("Secret stored.")
except Exception as e:
    print(f"Secret Error: {e}")
