from nornir import InitNornir
from nornir_napalm.plugins.tasks import napalm_configure
from nornir_utils.plugins.functions import print_result

# 1. Initialize Nornir
nr = InitNornir(config_file="nornir/config.yaml")

# 2. Define Arista EOS configuration commands
vlan_config = """
vlan 10
   name WEB_TIER
!
vlan 20
   name APP_TIER
!
vlan 30
   name DB_TIER
"""

# 3. Deploy configuration (Dry Run mode)
print("=== Previewing Configuration Changes (Dry Run) ===")
dry_run_results = nr.run(
    task=napalm_configure,
    configuration=vlan_config,
    dry_run=False,
)
print_result(dry_run_results)
