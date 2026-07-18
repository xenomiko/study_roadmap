import os
import requests
import json
import time
import yaml
from requests.exceptions import RequestException
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_result

class MerakiController:
    def __init__(self):
        self.api_key = os.environ.get("MERAKI_API_KEY")
        self.headers ={
           "X-Cisco-Meraki-API-Key": self.api_key
            } 
        
    
    
    @retry(
                retry=retry_if_result(lambda response : response.status_code == 429),
                stop=stop_after_attempt(5),
                wait=wait_exponential(multiplier= 1 ,min= 1 ,max= 10)
            )
    def get_orgs(self):
        URL = "https://api.meraki.com/api/v1/organizations"
        response = requests.get(URL,headers= self.headers, timeout=10)   
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4))
        else:
            print(response.text) 
        return response       
    

    
    def get_networks(self, org_id):
        URL = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"
        response = requests.get(URL, headers= self.headers, timeout= 10)
        if response.status_code == 200:
            print(json.dumps(response.json(), indent=4))
        return response    
            
                        


class AristaRestconf:
    def __init__(self):
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            devices_path = os.path.join(current_dir, "restconfig", "devices.yaml")
            with open(devices_path, "r") as f:
                self.devices = yaml.safe_load(f)
        except Exception as e:
            print(f"error {e}: cant find the file") 
            self.devices = {"devices": []}       



    def send_get_requests(self, device, endpoint, params= None):
        ip = device["ip"]
        hostname = device["hostname"]
        username = device["username"]
        password = device["password"]
        headers = {
                "Accept": "application/yang-data+json",
                "Content-Type": "application/yang-data+json"
            }
        URL = f"https://{ip}:6020/restconf{endpoint}"
        try:
            response = requests.get(URL, auth=(username, password), timeout= 10, verify=False, params= params, headers= headers)
            if response.status_code == 200:
                print(json.dumps(response.json(), indent=4))    
            else :
                print(response.text)
        except RequestException as e:
            print(f"error {e}: couldnt connect to device {hostname}")
    
    def get_interfaces(self):
        for device in self.devices["devices"]:
            params = {"fields": "interface(config)"}
            endpoint = "/data/openconfig-interfaces:interfaces"
            self.send_get_requests(device, endpoint, params=params)        