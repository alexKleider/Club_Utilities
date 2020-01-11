#!/usr/bin/env python

# File: send.py

"""
Used to send an email.
Expect command line parameters:
    smtp server for its configuration
    ...
May go to using docopt??
"""

import sys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import config

if not len(sys.argv) > 1:
    print("SMTP server not specified.")
    sys.exit()
arg1 = sys.argv[1]
if not arg1 in config.config:
    print("SMTP server designation invalid.")
    sys.exit()
server = config.config[arg1]
'''
for key in server:
    print("{}: {}".format(key, server[key]))
'''
print("Initiating SMTP: {host} {port}".format(**server))
s = smtplib.SMTP(host=server['host'], port=server['port'])
s.starttls()
s.ehlo
print("Loging in as {user} {password}".format(**server))
s.login(server['user'], server['password'])

msg = MIMEMultipart()
body = """This is a test.
Here's hoping it goes well.
Goog luck.
"""
msg['From'] = server['from']
msg['To'] = 'akleider@sonic.net'
msg['Subject'] = 'test'
msg.attach(MIMEText(body, 'plain'))

s.send_message(msg)
del msg

s.quit()

