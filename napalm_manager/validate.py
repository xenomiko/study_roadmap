from napalm import get_network_driver
import yaml
import pprint
import pandas as pd
from napalm.base.exceptions import ConnectAuthError, ConnectionException, CommandTimeoutException
with open('devices.yaml') as f:
    devices = yaml.safe_load(f)

compliance_data = []


for device in devices['devices']:
    driver = get_network_driver(device['driver'])
    device_instance = driver(
            hostname=device['hostname'],
            username=device['username'],
            password=device['password']
        )
    try:
        device_instance.open()
        report = device_instance.compliance_report(device['compliance_file'])
        if report:
            print(f"\n================ [{device['hostname']}] Compliance Report ================")
            pprint.pprint(report)
            compliance_data.append({
               "Hostname": device['hostname'],
               "Vendor": report.get('get_facts', {}).get('present', {}).get('vendor', {}).get('actual_value', 'Unknown'),
               "Compliant": report.get('complies', False)})
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

df = pd.DataFrame(compliance_data)
df.to_csv('compliance_report.csv', index=False)    