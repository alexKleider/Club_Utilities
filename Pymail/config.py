#!/usr/bin/env python

# File: config.py  (provides infrastructure for send.py)

## Two hard links:
# this file is used by the ~/Git/Club/Utils code base where it is found as
# Pymail/config.py
# and by the ~/Git/Lib code base where it is found as code/config.py.

"""
This file provides infrastructure for the accompanying file send.py
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


# Plan to rename 'config' to 'mta' ("--mta" command line option.)
# mta = dict(
config = dict(
    sonic= {
        "host": "smtp://akleider@mail.sonic.net",
        "port": "587",
        "protocol": "smtp",
        "auth": "on",
        "tls_starttls": "on",
        "user": "akleider@sonic.net",
        "from": "akleider@sonic.net",
        "password": getpw("sonic"),
        "tls": "on",
    },
    easy= {
        "host": "mailout.easydns.com",
        "tls_port": "587",
        "ssl_port": "465",  # SSL deprecated predecessor to TLS
#       "port": "2025",
        "port": "587",
        "protocol": "smtp",
        "auth": "on",
        "tls_starttls": "on",
        "user": "kleider.ca",
        "from": "alex@kleider.ca",
        "password": getpw("easy"),
        "tls": "on",
    },
    akg= {
        "host": "smtp.gmail.com",
        "port": "587",
        "tls_port": "587",
        "port": "587",
        "ssl_port": "465",
        "user": "alexkleider@gmail.com",
        "from": "alexkleider@gmail.com",
        "password": getpw("akg"),

    },
    clubg= {
        "host": "smtp.gmail.com",
        "port": "587",
        "tls_port": "587",
        "ssl_port": "465",
        "user": "rodandboatclub@gmail.com",
        "from": "rodandboatclub@gmail.com",
        "password": getpw("clubg"),

    },
)

if __name__ == '__main__':

    print("Redacted for security reasons!!")
    sys.exit()

    ### For testing only: comment out above two lines.
    pws = set()
    for key in config:
        pws.add(config[key]["password"])
    print("Passwords are:")
    print(repr(pws))

