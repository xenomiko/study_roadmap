import yaml
import xmltodict
import json
with open('devices.yaml','r') as f:
    devices = yaml.safe_load(f)

for device in devices["devices"]:
    netconf_args = device["netconf_args"]
    filename = f"config_{netconf_args["host"]}.xml"
    with open(filename, 'r') as file:
        xml_data = file.read()
    parsed_data = xmltodict.parse(xml_data)
    print(type(parsed_data['rpc-reply']['data']['interfaces']['interface']))