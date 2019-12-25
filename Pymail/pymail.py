#!/usr/bin/env python

# File: pymail.py

import smtplib
import ssl

def getpw(service):
    with open('pw.{}'.format(service), 'r') as f_obj:
        return f_obj.read().strip()

config = {
    "easydns": {
        "host": "mailout.easydns.com",
        "port": "465",
#       "port": "2025",
        "protocol": "smtp",
        "auth": "on",
        "tls_starttls": "on",
        "user": "kleider.ca",
        "from": "akleider@sonic.net",
        "password": getpw("easydns"),
        "tls": "on",
    },
    "akgmail": {
        "host": "smtp.gmail.com"
        "port": "587"
        "user": "alexkleider@gmail.com"
        "from": "alexkleider@gmail.com"
        "password": getpw("akgmail")

    },
    "clubgmail": {
        "host": "smtp.gmail.com"
        "port": "587"
        "user": "rodandboatclub@gmail.com"
        "from": "rodandboatclub@gmail.com"
        "password": getpw("clubgmail")

    },
}

if __name__ == '__main__':

    account = config["clubgmail"]
    account = config["akgmail"]
    account = config["easydns"]

    pw = account["password"]
    print("Password is '{}'.".format(pw))

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(account["host"], account["port"],
                        context=context) as server:
        server.login(account["user"], pw)

