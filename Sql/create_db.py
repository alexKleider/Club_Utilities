#!/usr/bin/env python3

# File: Sql/create_db.py

# Ref File://home/alex/WebSites/Python/python-sqlite-module

"""
Currently db in created only in memory.

Code: "use_sanitized = True/False"
must be changed depending on whether we are serious or testing.
Default is True
"""

import os
import sys
import csv
import sqlite3
sys.path.insert(0, os.path.split(sys.path[0])[0])
from rbc import Club

# need to explicitly close the connection so use context manager

db_name = ':memory:'
memlist_schema = 'memlist.schema'
applicant_schema = 'applicant.schema'

use_sanitized = True
if use_sanitized:
    mem_csv = "Sanitized/members.csv"
    applicant_csv = 'Sanitized/applicant.csv'
else:
    mem_csv = Club.MEMBERSHIP.SPoT
    applicant_csv = Club.APPLICANT_CSV

def data_generator(filename):
    """
    Assumes <filename> is a csv file.
    Yields one record at a time.
    """
    with open(filename, 'r', newline='') as instream:
        reader = csv.DictReader(instream, restkey='extra')
        for rec in reader:
#           check_read(rec)
            yield(rec)

member_data = []
# collect membership data
for rec in data_generator(mem_csv):
    values = [rec[key] for key in rec.keys()]
    member_data.append(tuple(values))
applicant_data = []
# collect applicant data
for rec in data_generator(applicant_csv):
    values = [rec[key] for key in rec.keys()]
    applicant_data.append(tuple(values))

with sqlite3.connect(db_name) as conn:
    # create connection object (exists or not!)
    print("Created connection.")
    cur = conn.cursor()  # create cursor into data base
    # Create a schema (how db is to be organized- a db table.)
    # For each column we want an identifier, a type and a description.
    # ...then can execute queries using cursor.execute('SQL_QUERY')
    # SQL query to create schema:
    with open(memlist_schema, 'r') as rf:
        schema = rf.read()
    cur.executescript(schema)
    print("Created the Member Table! Now inserting")
    cur.executemany(
        '''INSERT INTO people VALUES(NULL,
        ?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        member_data)
    print('Inserted values into member table.')
    with open(applicant_schema, 'r') as rf:
        schema = rf.read()
    cur.executescript(schema)
    print("Created the Applicant Table! Now inserting")
    cur.executemany(
        '''INSERT INTO applicants VALUES(NULL,
        ?,?,?,?,?,?,?,?,?,?,?,?)''',
        applicant_data)
    print('Inserted values into applicant table.')
    conn.commit()
    res = cur.execute("SELECT id, first, last, phone FROM people ORDER BY first")
    print("From people table:")
    for name in res.fetchall():
        print(name)
    
    res = cur.execute("""SELECT id, first, last, fee_rcvd, sponsor1,
            sponsor2, status FROM applicants ORDER BY last""")
    print("\nFrom applicants table:")
    for name in res.fetchall():
        print(name)

print("Closed the connection.")


