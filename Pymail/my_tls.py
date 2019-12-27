#!/usr/bin/env python

# File: _tls.py

## Option 2: Using .starttls()

import smtplib
import ssl

smtp_server = "smtp.gmail.com"
port = 587  # Std port for TLS
sender_email = "my@gmail.com"
password = input("Type your password followed by enter: ")

# Create a secure SSL context
context = ssl.create_default_context()

# Try to log in to server and send email
try:
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()  # Can be omitted  ?? .helo() (SMTP)
    server.starttls(context=context)  # Secure the connection
    server.ehlo()  # Can be omitted  ?? .ehlo() (ESMTP)
    server.login(sender_email, password)
    # TODO: Send email here
except Exception as e:
    # Print any error messages to stdout
    print(e)
finally:
    server.quit()
