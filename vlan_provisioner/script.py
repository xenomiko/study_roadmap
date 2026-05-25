import yaml
import typer
from netmiko import ConnectHandler

app = typer.Typer()

@app.command()
def deploy():
    with open("vlans.yaml", "r") as f:
        vlans = yaml.safe_load(f)
    with open("devices.yaml", "r") as f:
        devices = yaml.safe_load(f)
        
    for device in devices['devices']:
        print(f"Connecting to device  {device['host']}")
        
        
        with ConnectHandler(**device) as net_connect:
            net_connect.enable()
            for vlan in vlans['vlans']:
                if vlan['id'] <= 0 or vlan['id'] >= 4095:
                    continue
                    
                check_output = net_connect.send_command(f"show vlan {vlan['id']}")
                
                if "not found" in check_output or "not configured" in check_output:
                    print(f"Configuring VLAN {vlan['id']} on device {device['host']}")
                    commands = [
                        f"vlan {vlan['id']}",
                        f"name {vlan['name']}",

                    ]
                    net_connect.send_config_set(
                        commands,
                        enter_config_mode=True,
                        exit_config_mode=True,
                        cmd_verify=True
                    )
                else:  
                    print(f"VLAN {vlan['id']} already exists on device {device['host']}, skipping configuration.")        

if __name__ == "__main__":
    app()