#!/usr/bin/env python

# File: pymail.py

import sys

def getpw(service):
    with open('.pw.{}'.format(service), 'r') as f_obj:
        return f_obj.read().strip()

def pseudo_recipient(plus_name, email):
    parts = email.split('@')
    return parts[0] + '+' + plus_name + '@' + parts[1]

config = {
    "easy": {
        "host": "mailout.easydns.com",
        "tls_port": "587",
        "ssl_port": "465",
#       "port": "2025",
        "protocol": "smtp",
        "auth": "on",
        "tls_starttls": "on",
        "user": "kleider.ca",
        "from": "akleider@sonic.net",
        "password": getpw("easy"),
        "tls": "on",
    },
    "akg": {
        "host": "smtp.gmail.com",
        "tls_port": "587",
        "ssl_port": "465",
        "user": "alexkleider@gmail.com",
        "from": "alexkleider@gmail.com",
        "password": getpw("akg"),

    },
    "clubg": {
        "host": "smtp.gmail.com",
        "tls_port": "587",
        "ssl_port": "465",
        "user": "rodandboatclub@gmail.com",
        "from": "rodandboatclub@gmail.com",
        "password": getpw("clubg"),

    },
}

if __name__ == '__main__':

    print("Redacted for security reasons!!")
    sys.exit()

    ### For testing only: 
    pws = set()
    for key in config:
        pws.add(config[key]["password"])
    print("Passwords are:")
    print(repr(pws))

