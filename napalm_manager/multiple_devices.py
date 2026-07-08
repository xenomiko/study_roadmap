from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException, CommandTimeoutException, ConnectAuthError
import yaml
import pandas as pd

with open('devices.yaml') as f:
    devices = yaml.safe_load(f)

report_data = []

for device in devices['devices']:
    driver = get_network_driver(device['driver'])

    device_instance = driver(
            hostname=device['hostname'],
            username=device['username'],
            password=device['password']
        )
    try:
        device_instance.open()
        facts = device_instance.get_facts()
        report_data.append(facts)
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
    df = pd.DataFrame(report_data)
    if not df.empty:    
        report_df = df.drop(columns=['interface_list'], errors='ignore')
        print(report_df.to_string(index=False))
    else:
        print("No data to display.")            
