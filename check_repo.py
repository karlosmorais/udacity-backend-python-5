import requests
import json

url = "https://api.github.com/repos/karlosmorais/udacity-backend-python-5"
auth = ("karlosmorais", "token")

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
