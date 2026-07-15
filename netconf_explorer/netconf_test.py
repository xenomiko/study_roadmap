import yaml
import inspect
from ncclient import manager
from xml.dom.minidom import parseString
with open("devices.yaml", "r") as f:
    devices= yaml.safe_load(f)
interface_filter = """
<filter>
   <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface>
            <name>Management0</name>
        </interface>
   </interfaces>
</filter>
"""
for device in devices["devices"]:
    netconf_args =  device["netconf_args"]
    with manager.connect(**netconf_args) as m:
     response = m.get_config(source='running', filter=interface_filter)
     dom =  parseString(response.xml)
     print(dom.toprettyxml(indent=""))