#!/usr/bin/python

# File: my_ssl.py

## Option 1: Using SMTP_SSL()
import sys
import smtplib
print("Imported smtplib")
import ssl
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

print("'host': '{}'.".format(host))
print("'port': '{}'.".format(port))
print("'user': '{}'.".format(user))
print("'password': '{}'.".format("redacted!"))
print("'from_': '{}'.".format(from_))
print("'to_': '{}'.".format(to_))
print("'message': '{}'.".format(message))
sys.exit()


# Create a secure SSL context
context = ssl.create_default_context()
with smtplib.SMTP_SSL(host, port,
                        context=context) as server:
    server.login(user, password)
    # TODO: Send email here
    server.sendmail(from_, to_, message)
