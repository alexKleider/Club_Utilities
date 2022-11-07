#!/usr/bin/env python3

# Ref File://home/alex/WebSites/Python/python-sqlite-module

import csv
import sqlite3

# need to explicitly close the connection so use context manager

db_name = ':memory:'
schema_file = 'schema.sql'
csv_file = "eg_data.csv"

def data_generator(filename):
    with open(filename, 'r', newline='') as instream:
        reader = csv.DictReader(instream, restkey='extra')
        for rec in reader:
#           check_read(rec)
            yield(rec)

with open(schema_file, 'r') as rf:
    schema = rf.read()

data = []
for rec in data_generator(csv_file):
    values = [rec[key] for key in rec.keys()]
    data.append(tuple(values))

with sqlite3.connect(db_name) as conn:
    # create connection object (exists or not!)
    print("Created connection.")
    cur = conn.cursor()  # create cursor into data base
    # Create a schema (how db is to be organized- a db table.)
    # For each column we want an identifier, a type and a description.
    # ...then can execute queries using cursor.execute('SQL_QUERY')
    # SQL query to create schema:
    cur.executescript(schema)
    print("Created the Table! Now inserting")
    cur.executemany(
        '''INSERT INTO people VALUES(NULL,
        ?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        data)
    print('Inserted values into the table.')
    conn.commit()
    res = cur.execute("SELECT id, first, last, phone FROM people ORDER BY first")
    for name in res.fetchall():
        print(name)
    

print("Closed the connection.")


