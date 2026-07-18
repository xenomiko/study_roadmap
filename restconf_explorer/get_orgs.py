import requests
import json
import os
api_key = os.environ.get("MERAKI_API_KEY")
headers = {
    "X-Cisco-Meraki-API-Key": api_key
    }

URL = "https://api.meraki.com/api/v1/organizations"
response = requests.get(URL,headers= headers, timeout=10)
print("My Status Code is:", response.status_code)
if response.status_code == 200:
    print(json.dumps(response.json(), indent=4))
else:
    print(response.text)    


