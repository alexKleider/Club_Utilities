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


def get_mailings(file_name):
    pass


REPORT_PROGRESS = True

argv_length = len(sys.argv)

if not argv_length > 1:
    print("SMTP server not specified.")
    sys.exit()
arg1 = sys.argv[1]
if not arg1 in config.config:
    print("SMTP server designation invalid.")
    sys.exit()
server = config.config[arg1]

if argv_length == 3:
    mailings = get_mailings(sys.argv[2])
else:
    mailings = [
        {
        'From': 'alex@kleider.ca',
#       'reply-to': 'alexkleider@gmail.com',
#       'To': 'alexkleider@gmail.com',  # Relay access denied
        'To': 'akleider@sonic.net',
        'Subject': 'TEST',
        'body': """This is a test.
Here's hoping it goes well.
Goog luck.
""",
        },
    ]

if REPORT_PROGRESS:
    print("Initiating SMTP: {host} {port}".format(**server))
s = smtplib.SMTP(host=server['host'], port=server['port'])
s.starttls()
s.ehlo
if REPORT_PROGRESS:
    s.login(server['user'], server['password'])
    print("Logged in as {user} {password}".format(**server))

for mailing in mailings:
    msg = MIMEMultipart()
    body = mailing['body']
    del mailing['body']
    for key in mailing:
        msg[key] = mailing[key]
    msg.attach(MIMEText(body, 'plain'))

    if REPORT_PROGRESS:
        for key in mailing:
            print("{}=>{}".format(key, msg[key]))

    s.send_message(msg)
    del msg

s.quit()

