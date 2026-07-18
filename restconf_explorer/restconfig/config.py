from napalm import get_network_driver
import yaml
from napalm.base.exceptions import ConnectAuthError, ConnectionException, CommandTimeoutException



restconf_config = """
ip access-list restconf-lab
   10 permit tcp any any eq 6020
   20 permit ip any any
!
system control-plane
   ip access-group restconf-lab in
!
security pki certificate generate self-signed restconf.crt key restconf.key generate rsa 2048 parameters common-name restconf
management security
   ssl profile restconf
      certificate restconf.crt key restconf.key
management api restconf
   transport https default
      ssl profile restconf
"""
with open('devices.yaml', "r") as f:
    devices = yaml.safe_load(f)
for device in devices['devices']:
    driver = get_network_driver(device['driver'])
    device_instance = driver(
            hostname=device['hostname'],
            username=device['username'],
            password=device['password']
        )
    try:
        device_instance.open()
        device_instance.load_merge_candidate(config=restconf_config)
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

