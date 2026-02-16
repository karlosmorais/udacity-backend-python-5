import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

url = f"https://api.github.com/repos/{os.getenv('GITHUB_USER')}/{os.getenv('GITHUB_REPO')}"
auth = (os.getenv('GITHUB_USER'), os.getenv('GITHUB_TOKEN'))

try:
    response = requests.get(url, auth=auth)
    print(f"Status Code: {response.status_code}")
    print(f"Final URL: {response.url}")
    if response.history:
        print("Redirects:")
        for resp in response.history:
            print(f"  {resp.status_code} {resp.url}")
    if response.status_code == 200:
        data = response.json()
        print(f"Default Branch: {data['default_branch']}")
        print(f"Private: {data['private']}")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"Exception: {e}")
