#!/usr/bin/env/python

# File: my_smtp.py

import smtplib
import pymail

acnt = pymail.config["akg"]

host = acnt["host"]
port = acnt["ssl_port"]
user = acnt["user"]
from_ = acnt["from"]
password = acnt["password"]
to_ = pymail.pseudo_recipient('r1', from_)
message = """Subject: Hi there

This message is sent from Python."""

try:
    smtpObj = smtplib.SMTP(host, port)
    smtpObj.sendmail(from_, to_, message)
    print("Successfully sent email")
except SMTPException:
    print("Error: unable to send email")
