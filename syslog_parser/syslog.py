import socket
import re
import time
import smtplib
from email.mime.text import MIMEText

def send_email_alert(device, severity, event):
  smtp_server = 'smtp.gmail.com'
  smtp_port = 587
  sender_email = 'sender@gmail.com'
  sender_password = 'sender_password'
  recipient_email = 'recipient@gmail.com'
  body = f"Alert from device: {device}\nSeverity: {severity}\nEvent: {event}"
  msg = MIMEText(body)
  msg['Subject'] = f"Syslog Alert: {event} on {device}"  
  msg['From'] = sender_email
  msg['To'] = recipient_email
  try:
      with smtplib.SMTP(smtp_server, smtp_port) as server:
         server.starttls()
         server.login(sender_email, sender_password)
         server.sendmail(sender_email, recipient_email, msg.as_string())
         print(f"Email alert sent for device: {device}, event: {event}")
  except Exception as e:
      print(f"Failed to send email alert: {e}") 


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
       send_email_alert(hostname, severity_int, mnemonic)
