#!/usr/bin/env python3

# File: ck_underscore_dash.py

"""
Quick script written to check for consistency in use of 
dash vs underscore.
Using dashes, not underscores for double barreled names.
Underscores are used where one would use a space (but can't
because it would stymie the parsing.)
"""
import os
import csv

with open(os.path.expandvars("$CLUB/Data/memlist.csv"), 'r',
        newline='') as stream:
    reader = csv.DictReader(stream)
    for rec in reader:
        for separator in '-_':
            for key in ('first', 'last'):
                if separator in rec[key]:
                    print(rec[key])

