import yaml
from jinja2 import Environment, FileSystemLoader
from deplooy import deploy_config
with open('devices.yaml', 'r') as file:
    devices = yaml.safe_load(file)
env = Environment(loader=FileSystemLoader("."))
for hostname, device_info  in devices["devices"].items():
  print(f"DEBUG [{hostname}] Keys found in YAML: {list(device_info.keys())}")
  output = ""
  for template_name in device_info.get("templates", []):
   template = env.get_template(template_name)
   output += template.render(hostname=hostname, **device_info) +"\n"
  with open(f'{hostname}.cfg', 'w') as f:
    f.write(output)
  deploy_config(hostname, device_info, output)