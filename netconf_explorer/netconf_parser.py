import xml.etree.ElementTree as ET
import yaml
with open("devices.yaml", "r") as f:
    devices = yaml.safe_load(f)

for device in devices["devices"]:
    netconf_args = device['netconf_args']
    with open(f"config_{netconf_args["host"]}.xml", "r") as f:
        xml_data = f.read()

    print(xml_data)