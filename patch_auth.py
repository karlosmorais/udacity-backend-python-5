import subprocess

try:
    with open('aws-auth-patch.yml', 'r') as f:
        patch_content = f.read()
    
    # We strip metadata for cleaner patch
    import yaml
    patch_dict = yaml.safe_load(patch_content)
    if 'metadata' in patch_dict:
        del patch_dict['metadata']
    
    # Use kubectl patch with --patch argument
    # We need to target the data field specifically or use merge patch
    # The simplest way is to use --patch argument with the YAML content
    # kubectl patch configmap/aws-auth -n kube-system --patch "$(cat aws-auth-patch.yml)"
    
    cmd = ['kubectl', 'patch', 'configmap/aws-auth', '-n', 'kube-system', '--patch', patch_content]
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("Error:", result.stderr)

except Exception as e:
    print(e)
