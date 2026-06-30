import pandas as pd
from netmiko import ConnectHandler

inventory_data = []
# devices info
arista_devices = [
    {
        'device_type': 'arista_eos',
        'host': '172.20.20.2',
        'username': 'admin',
        'password': 'admin'
    },
    {
        'device_type': 'arista_eos',
        'host': '172.20.20.3',
        'username': 'admin',
        'password': 'admin'
    },
    {
        'device_type': 'arista_eos',
        'host': '172.20.20.4',
        'username': 'admin',
        'password': 'admin'
    }
]

for device in arista_devices:
    with ConnectHandler(**device) as connection:
     output = connection.send_command('show version', use_textfsm=True)
     device_dict = output[0]  
     inventory_data.append(device_dict)
     connection.disconnect()

df = pd.DataFrame(inventory_data)
df.to_csv('network_inventory.csv', index=False)     
     