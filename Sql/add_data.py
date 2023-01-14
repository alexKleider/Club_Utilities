#!/usr/bin/env python3

# File: add_data.py

"""
https://docs.python.org/3/library/sqlite3.html

Assume club.db has already been created as follows:
$ sqlite3 club.db
sqlite> .read specification.sql
sqlite> .quit
"""

import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])
import csv
import sqlite3
import rbc
import data
import helpers

insert_template = """INSERT INTO {table} ({keys})
    VALUES({values});"""

sql_commands_file =  'create_tables.sql'


def get_commands(in_file):
    """
    Assumes <in_file> contains valid SQL commands.
    i.e. could be read by sqlite3 > .read <in_file>
    Yeilds the commands one at a time.
    """
    with open(in_file, 'r') as in_stream:
        command = ''
        for line in in_stream:
            line = line.strip()
            if line.startswith('--'):
                continue
            command = command + line.strip()
            if line.endswith(';'):
                yield command[:-1]
                command = ''


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


def get_applicant_data(applicant_source, sponsor_source):
    """
    """
    club = rbc.Club()
    club.applicant_spot = applicant_source
    club.sponsors_spot = sponsor_source
    club.infile = 'Sanitized/members.csv'
    data.populate_sponsor_data(club)
    data.populate_applicant_data(club)
    return club.applicant_data


def populate_applicant_data(applicant_data, valid_names,
                                con, cur):
    """
    """
    names = set()
    for key in applicant_data.keys():
        names.add(key)
        sponsors = set()
        for name in ('sponsor1', 'sponsor2'):
            if name:
                sponsors.add(helpers.tofro_first_last(
                    applicant_data[key][name]))
        names.update(sponsors)
    if not set(valid_names).issuperset(names):
        _ = input(names.difference(set(valid_names)))
    else:
        print("so far so good")


def get_table_names(cur):
    res = cur.execute("SELECT name FROM sqlite_master")
    # returns a list of tuples!
    # in this case: each one tuple is a table name
    tups = [tup[0] for tup in res.fetchall()]
    return ', '.join(tups)


def main():
    con = sqlite3.connect("club.db")
    cur = con.cursor()
    # set up the tables (first deleting any that exist)
    for command in get_commands(sql_commands_file):
        cur.execute(command)
#   _ = input(f"Table Names: {get_table_names(cur)}")
    populate_people("Sanitized/members.csv", con, cur)
    # collect a set of valid name keys (people_keys)
    cur.execute('SELECT first, last FROM people')
#   print("First and last names from 'people' table:")
    people = cur.fetchall()
    people_keys = [f"{names[1]},{names[0]}" for names in people]

    applicant_data = get_applicant_data(
            'Sanitized/applicants.txt',
            'Sanitized/sponsors.txt')
    populate_applicant_data(applicant_data, people_keys, con, cur)
    con.close()

if __name__ == '__main__':
    main()
