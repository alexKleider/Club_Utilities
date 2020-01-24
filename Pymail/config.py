#!/usr/bin/env python

# File: config.py
"""
SSL (Secure Sockets Layer) is a deprecated successor to 
TLS (Transport Layer Security)
"""

import sys
import os

def getpw(service):
    """
    Passwords are in highly restricted dot files.
    Each file contains only the password.
    """
    with open(
        os.path.expanduser('~/.pw.{}'.format(service)), 'r') as f_obj:
        return f_obj.read().strip()


config = {
    "easy": {
        "host": "mailout.easydns.com",
        "tls_port": "587",
        "ssl_port": "465",  # SSL deprecated predecessor to TLS
#       "port": "2025",
        "port": "587",
        "protocol": "smtp",
        "auth": "on",
        "tls_starttls": "on",
        "user": "kleider.ca",
#       "from": "akleider@sonic.net",
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

    ### For testing only: comment out above two lines.
    pws = set()
    for key in config:
        pws.add(config[key]["password"])
    print("Passwords are:")
    print(repr(pws))

