import socket
import re
import time
pattern = r"<(\d+)>.* ([\w-]+) %([A-Z]+)-(\d)-([A-Z]+):"
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('0.0.0.0', 1514))
recent_events = {}
while True:
 data, address = s.recvfrom(1024)
 log_msg = data.decode('utf-8').strip()
 match = re.search(pattern, log_msg)
 if match:
    hostname = match.group(2)
    severity_int = int(match.group(4))
    mnemonic = match.group(5)
    print(f"Parsed Event -> Device: {hostname} | Severity: {severity_int} | Event: {mnemonic}")

    if severity_int <= 5:
       current_time = time.time()
       alert_key = f"{hostname}_{mnemonic}"
       if alert_key in recent_events:
         last_alert_time = recent_events[alert_key]
         time_passed = current_time - last_alert_time
         if time_passed < 60:
           continue
         recent_events[alert_key] = current_time
