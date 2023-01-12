#!/usr/bin/env python3

# File: add_data.py

"""
https://docs.python.org/3/library/sqlite3.html

Assume club.db has already been created as follows:
$ sqlite3 club.db
sqlite> .read specification.sql
sqlite> .quit
"""

import sys
import csv
import sqlite3


def check_read(rec):
        print(repr(rec))
        for key, value  in rec.items():
            print(f"{key}: {value}")


def return_name_suffix_tuple(name):
    """
    Returns a tuple or none.
    A tuple is returned if 3rd last character is '_':
    in which case two strings are returned:
    what comes before the '_' and what comes after.
    """
    n = name.find('_')
    suffix = name[n+1:]
    if n > -1 and len(suffix) == 2:
        return (name[:-3], suffix)
    else: return '', ''


def add_suffix_field(rec):
    """
    Returns a record with a 'suffix' field
    (which may be an empty string) based on
    the 'last' name field as processed by the
    <return_name_suffix_tuple>.
    """
    ret = {}
    ret['first'] = rec['first']
    ret['last'] = rec['last']
    ret['suffix'] = ''
    ret['phone'] = rec['phone']
    ret['address'] = rec['address']
    ret['town'] = rec['town']
    ret['state'] = rec['state']
    ret['postal_code'] = rec['postal_code']
    ret['country'] = rec['country']
    ret['email'] = rec['email']
    last, suffix = return_name_suffix_tuple(rec['last'])
    if suffix:
        ret['last'] = last
        ret['suffix'] = suffix
    return ret


def data_generator(filename):
    """
    Yield records from a csv data base.
    """
    with open(filename, 'r', newline='') as instream:
        reader = csv.DictReader(instream, restkey='extra')
        for rec in reader:
            yield(rec)


def populate_people(source, connection, cursor):
    """
    Adds all data from <source> into the "people" table.
    """
    for rec in data_generator(source):
        ret = add_suffix_field(rec)
        keys = ', '.join([key for key in ret.keys()])
        values = [value for value in ret.values()]
        values = ', '.join([f"'{value}'" for value in ret.values()])
        command = insert_template.format(
                    table='people', keys=keys, values=values)
        cursor.execute(command)
    connection.commit()


def get_table_names(cur):
    res = cur.execute("SELECT name FROM sqlite_master")
    # returns a list of tuples!
    # in this case: each one tuple is a table name
    tups = [tup[0] for tup in res.fetchall()]
    return ', '.join(tups)


insert_template = """INSERT INTO {table} ({keys})
    VALUES({values});"""

con = sqlite3.connect("club.db")
cur = con.cursor()
print(f"Table Names: {get_table_names(cur)}")
populate_people("eg_memlist.csv", con, cur)

cur.execute('SELECT * FROM people')
print("Data from 'people' table:")
for item in cur.fetchall():
    print('  ', item)

con.close()
