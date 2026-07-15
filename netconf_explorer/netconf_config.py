from netmiko import ConnectHandler, ConnectionException, NetMikoTimeoutException, ConfigInvalidException
import yaml
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))

with open('devices.yaml', 'r') as file:
    data = yaml.safe_load(file)

for device in data['devices']:
    template = env.get_template(device['config_commands'])
    rendered_config = template.render(**device)
    
    connection_params = {
        'host': device['host'],
        'username': device['username'],
        'password': device['password'],
        'device_type': device['device_type']
    }
    
    try:
        print(f"Connecting to {device['host']}...")
        with ConnectHandler(**connection_params) as net_connect:
            net_connect.enable()
            output = net_connect.send_config_set(rendered_config.splitlines())
            
            print(f"Configuration applied to {device['host']}:")
            print(output)
            
    except (ConnectionException, NetMikoTimeoutException, ConfigInvalidException) as e:
        print(f"Failed to configure {device['host']}: {e}")