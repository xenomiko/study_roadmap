from ncclient import manager
from xml.dom.minidom import parseString
import yaml

with open("devices.yaml", "r") as f:
    devices =  yaml.safe_load(f)
payload = """
<config xmlns:xc="urn:ietf:params:xml:ns:netconf:base:1.0">
    <interfaces xmlns="http://openconfig.net/yang/interfaces">
        <interface>
            <name>Management0</name>
            <config>
                    <description>awal config b netconf</description>
            </config>
        </interface>
    </interfaces>
</config>
"""    
for device in devices['devices']:
 netconf_args= device['netconf_args']
 try:
  with manager.connect(**netconf_args) as m:
    try:
      response= m.edit_config(target='candidate', config=payload)
      m.commit()

    except Exception as e:
     print(f"An error occurred: {e}")    
     m.discard_changes()
 except Exception as e:
    print(f"An error occurred: {e}")     