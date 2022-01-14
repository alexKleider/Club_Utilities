#!/usr/bin/env python3

# File: sys_globals.py  A place to keep system wide globals
# Typically: import sys_globals as glbs

# On rethinkiing: perhaps these globals should all be attributes of
# rbc.Club class.

VERSION = "1.1"

SEPARATOR = '|'  # Note: used by rbc and member modules.
## NOTE: When using this separator as part of a command line argument,
## the argument must be "quoted" to prevent the shell from treating it
## as a pipe!!!
MSMTP_ACCOUNT = "gmail"
MIN_TIME_TO_SLEEP = 1   # } Seconds between
MAX_TIME_TO_SLEEP = 5   # } email postings.

DEFAULT_ADDENDUM2REPORT_FILE = "Info/addendum2report.txt"
