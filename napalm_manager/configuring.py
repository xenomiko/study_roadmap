from napalm import get_network_driver
from jinja2 import Environment, FileSystemLoader
import yaml
from napalm.base.exceptions import ConnectAuthError, ConnectionException, CommandTimeoutException

with open('devices.yaml') as f:
    devices = yaml.safe_load(f)
env = Environment(loader=FileSystemLoader('templates'))
for device in devices['devices']:
    template = env.get_template(device['template'])
    rendered_config = template.render(**device)
    driver = get_network_driver(device['driver'])
    device_instance = driver(
            hostname=device['hostname'],
            username=device['username'],
            password=device['password']
        )
    try:
        device_instance.open()
        device_instance.load_merge_candidate(config=rendered_config)
        diffs = device_instance.compare_config()
        if diffs:
            print(f"[{device['hostname']}] Configuration differences:\n{diffs}")
            device_instance.commit_config()
            print(f"[{device['hostname']}] Configuration committed.")
        else:
            print(f"[{device['hostname']}] No configuration changes needed.")
    except ConnectAuthError as e:
        print(f"[{device['hostname']}] Authentication failed: {e}")
    except ConnectionException as e:
        print(f"[{device['hostname']}] Connection failed/timed out: {e}")
    except CommandTimeoutException as e:
        print(f"[{device['hostname']}] Command timed out: {e}")
    except Exception as e:
        print(f"[{device['hostname']}] Unexpected error: {e}")
    finally:
        try:
            device_instance.close()
        except Exception:
            pass
