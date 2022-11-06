#!/usr/bin/env python3

# File: sql.py

"""
https://docs.python.org/3/library/sqlite3.html

Usage:
    ./sql.py cmd [file_name]

The second (optional) <file_name> parameter only applies to the
add_data command in which case it over-rides the default csv file from
which data is obtained.

Commands:
    new_db
    table_names
    add_data
    display
"""

import sys
import csv
import sqlite3

csv_file = "eg_data.csv"
db_name = 'my.db'
file_name = ''
if len(sys.argv) > 1:
    cmd = sys.argv[1]
    if len(sys.argv) > 2:
        file_name = sys.argv[2]
else:
    print("Usage: ./sql.py cmd [file_name]")
    print("\nMust specify one of the following commands:")
    print("\tnew_db, table_names, add_data, display")
    sys.exit()

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

def new_db_cmd(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.execute("""CREATE TABLE people
            (id INTEGER NOT NULL PRIMARY KEY,
            first,last,phone,address,town,state,postal_code,country,
            email,dues,dock,kayak,mooring,status)""")
    cur.execute("SELECT name FROM sqlite_master")
    names = cur.fetchone()
    print(f"Tables now in existence: {names}")

def table_names_cmd(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    res = cur.execute("SELECT name FROM sqlite_master")
    # returns a tuple of table names...
    print("Table names: ", end='')
    table_names = res.fetchone()
    print(table_names)

    res = cur.execute(f"SELECT first FROM {table_names[0]}")
    res = cur.execute(f"SELECT first FROM people")
    print(res.fetchall())

def add_data_cmd(db_name):
    global csv_file
    if file_name:
        csv_file = file_name
    data = []
    for rec in data_generator(csv_file):
        values = [rec[key] for key in rec.keys()]
        data.append(tuple(values))
    #   print(repr(values))
    #   check_read(rec)
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    cur.executemany(
        '''INSERT INTO people VALUES(NULL,
        ?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        data)
    con.commit()

def display_cmd(db_name):
    con = sqlite3.connect(db_name)
    cur = con.cursor()
    res = cur.execute("SELECT id, first, last FROM people ORDER BY first")
    for name in res.fetchall():
        print(name)


if cmd == 'new_db':
    new_db_cmd(db_name)
elif cmd == 'table_names':
    table_names_cmd(db_name)
elif cmd == 'add_data':
    add_data_cmd(db_name)
elif cmd == 'display':
    display_cmd(db_name)

