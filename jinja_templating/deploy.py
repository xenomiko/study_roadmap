from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

def deploy_config(hostname, device_info, config):
    
    netmiko_params = {
        'device_type': device_info.get('device_type'),
        'host': device_info.get('mgmt_ip'),  
        'username': device_info.get('username'),
        'password': device_info.get('password'),
    }
    
    config_lines = [line for line in config.strip().splitlines() if line]


    try:
        with ConnectHandler(**netmiko_params) as net_connect:
            net_connect.enable()  
            output = net_connect.send_config_set(config_lines)
            print(f"[{hostname}] Deployment Output:\n{output}\n")
            
    except NetmikoTimeoutException:
        print(f"ERROR: [{hostname}] Connection timed out. Check container routing or SSH status.")
    except NetmikoAuthenticationException:
        print(f"ERROR: [{hostname}] Authentication failed. Check your password settings.")
    except Exception as e:
        print(f"ERROR: [{hostname}] Network operation failed: {e}")