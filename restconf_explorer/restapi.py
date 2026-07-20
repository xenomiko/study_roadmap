import os
import requests
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception



def is_retryable(exception):
    if isinstance(exception, requests.HTTPError) and exception.response is not None:
        return exception.response.status_code == 429  
    if isinstance(exception, (requests.ConnectionError, requests.Timeout)):
        return True
    return False

class MerakiController:
    def __init__(self):
        self.api_key = os.environ.get("MERAKI_API_KEY")
        if not self.api_key:
            raise ValueError("MERAKI_API_KEY environment variable is not set.")
        self.headers ={
           "X-Cisco-Meraki-API-Key": self.api_key
            } 
        
    
    @retry(
                retry= retry_if_exception(is_retryable),
                stop=stop_after_attempt(5),
                wait=wait_exponential(multiplier= 1 ,min= 1 ,max= 10),
                reraise= True
            )
    
    def send_get(self, url,params= None):
        response = requests.get(url, headers=self.headers, timeout=10, params= params)
        response.raise_for_status()
        return response
        
     
    def get_orgs(self):
        URL = "https://api.meraki.com/api/v1/organizations"
        response = self.send_get(URL) 
        return response.json()
    

    def get_networks(self, org_id):
        URL = f"https://api.meraki.com/api/v1/organizations/{org_id}/networks?perPage=1000"
        all_networks = []
        while URL:
            response = self.send_get(URL)
            
            page_data = response.json()
            all_networks.extend(page_data)
            if "next" in response.links:
                URL = response.links["next"]["url"]
            else:
                    URL= None         
        return all_networks    

    @retry(
        retry=retry_if_exception(is_retryable),
        stop=stop_after_attempt(5),
        wait=wait_exponential(multiplier=1, min=1, max=10),
        reraise=True,
)
    def send_post(self, URL, payload= None):
            response = requests.post(URL, headers= self.headers, json= payload, timeout= 10)                   
            response.raise_for_status()
            return response
    

    def create_network(self,org_id, network_name,product_types = None, timezone = None):
        payload = {
                "name": network_name,
        }
        if product_types is not None:
            payload["productTypes"] = product_types
        else:
            product_types = ["appliance"]    
        if timezone is not None:
            payload["timeZone"] = timezone    
        URL =   f"https://api.meraki.com/api/v1/organizations/{org_id}/networks"  
        
        response = self.send_post(URL, payload=payload) 
        return response.json()
