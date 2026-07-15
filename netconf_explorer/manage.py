import inspect
import yaml
from ncclient import manager
from ncclient.transport.errors import AuthenticationError
with open('devices.yaml', 'r') as file:
    devices = yaml.safe_load(file)
ncclient_valid_args = inspect.signature(manager.connect).parameters.keys()

for device in devices['devices']:
    netconf_args = device['netconf_args']
    try:
        with manager.connect(**netconf_args) as m:
            capabilities = m.server_capabilities
            for capability in capabilities:
                print(capability)
    except AuthenticationError as e:
        print(f"  Authentication Failed on {device['host']}: Check username or password. Error: {e}")