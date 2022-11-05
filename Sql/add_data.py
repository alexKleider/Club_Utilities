#!/usr/bin/env python3

# File: add_data.py

"""
https://docs.python.org/3/library/sqlite3.html
"""

import sys
import csv
import sqlite3

con = sqlite3.connect("my.db")
cur = con.cursor()
# the following already done:
# cur.execute("CREATE TABLE people (first,last,phone,address,town,state,postal_code,country,email,dues,dock,kayak,mooring,status)")

def check_read(rec):
        print(repr(rec))
        for key, value  in rec.items():
            print(f"{key}: {value}")
        _ = input("")

def data_generator(filename):
    with open(filename, 'r', newline='') as instream:
        reader = csv.DictReader(instream, restkey='extra')
        for rec in reader:
#           check_read(rec)
            yield(rec)

res = cur.execute("SELECT name FROM sqlite_master")
# returns a tuple of table names...
print("Table names: ", end='')
print(res.fetchone())

collector = []
for rec in data_generator("eg_data.csv"):
    values = [rec[key] for key in rec.keys()]
    collector.append(tuple(values))
#   print(repr(values))
#   check_read(rec)
command_lines = []
command_lines.append('INSERT INTO people VALUES')
for item in collector:
    command_lines.append(repr(item) + ',')
command = '\n'.join(command_lines)
command = command[:-1]
cur.execute(command)
con.commit()

