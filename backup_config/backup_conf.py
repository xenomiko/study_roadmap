from netmiko import ConnectHandler, ConnectionException, NetMikoTimeoutException, NetMikoAuthenticationException, SSHException
import subprocess

devices = [
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
    }
]
try:
 for device in devices:
    with ConnectHandler(**device) as net_connect:
      output = net_connect.send_command('show running-config')
      with open(f"{device['host']}_backup.conf", 'w') as backup_file:
            backup_file.write(output)
    subprocess.run(['git', 'add', f"{device['host']}_backup.conf"])
    subprocess.run(['git', 'commit', '-m', f"Backup of {device['host']} configuration"])            
except (ConnectionException, NetMikoTimeoutException, NetMikoAuthenticationException, SSHException) as e:
    print(f"Error connecting to device: {e}")            
                     