from napalm import get_network_driver

driver = get_network_driver('eos')

device = driver(hostname='172.20.20.2' , username='admin', password='admin')
device.open()

facts = device.get_facts()
print(facts)
device.close()