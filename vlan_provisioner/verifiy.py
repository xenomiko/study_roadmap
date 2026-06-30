import yaml
from netmiko import ConnectHandler

def verify_deployment():
    # Load your lab profile data
    with open("vlans.yaml", "r") as f:
        vlans = yaml.safe_load(f)
    with open("devices.yaml", "r") as f:
        devices = yaml.safe_load(f)
        
    for device in devices['devices']:
        print(f"\n--- Checking Device: {device['host']} ---")
        
        with ConnectHandler(**device) as net_connect:
            # Grab the clean summary output directly from the engine shell
            vlan_summary = net_connect.send_command("show vlan brief")
            
            for vlan in vlans['vlans']:
                vlan_id = str(vlan['id'])
                
                # Check if the specific VLAN ID is present in the table string
                if vlan_id in vlan_summary:
                    print(f" SUCCESS: VLAN {vlan_id} ('{vlan['name']}') is active on the switch.")
                else:
                    print(f" MISSING: VLAN {vlan_id} was NOT found in the database.")

if __name__ == "__main__":
    verify_deployment()