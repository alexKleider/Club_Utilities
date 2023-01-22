#!/usr/bin/env python3

# File: main.py

"""
Manage data base for a letter writing app.
"""

import os
import sys
import csv
import sqlite3
d, f = os.path.split(sys.path[0])
d, f = os.path.split(d)
sys.path.insert(0, d)
# print(sys.path)
import content

db_file_name = 'Data/contacts.sqldb'
source_csv = 'Data/my.csv'
creation_script = 'creation_script.sql'

insert_template = """INSERT INTO {table} ({keys})
    VALUES({values});"""


def get_commands(sql_file):
    """
    Assumes <in_file> contains valid SQL commands.
    i.e. could be read by sqlite> .read <in_file>
    Yeilds the commands one at a time.
    Usage:
        con = sqlite3.connect("sql.db")
        cur = con.cursor()
        for command in get_commands(sql_commands_file):
            cur.execute(command)
    """
    with open(sql_file, 'r') as in_stream:
        command = ''
        for line in in_stream:
            line = line.strip()
            if line.startswith('--'):
                continue
            command = command + line.strip()
            if line.endswith(';'):
                yield command[:-1]
                command = ''


def data_generator(filename):
    """
    Yield records from a csv data base.
    """
    with open(filename, 'r', newline='') as instream:
        reader = csv.DictReader(instream, restkey='extra')
        for rec in reader:
            yield(rec)


def get_field_names(csv_file):
    with open(csv_file, 'r', newline='') as instream:
        reader = csv.DictReader(instream)
        return(reader.fieldnames)

def get_insert_query(record, table):
    keys = ', '.join([key for key in record.keys()])
    values = [value for value in record.values()]
    values = ', '.join([f"'{value}'" for
                    value in record.values()])
    query = insert_template.format(
            table=table, keys=keys, values=values)
#       _ = input(query)
    return query


def execute(cursor, connection, command):
    try:
        cursor.execute(command)
    except (sqlite3.IntegrityError, sqlite3.OperationalError):
        print("Unable to execute following query:")
        print(command)
        raise
    connection.commit()


def initiate_db():
    print("Initiating the data base.")
    if os.path.exists(db_file_name):
        os.remove(db_file_name)
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    ## set up the tables (first deleting any that exist)
    for command in get_commands(creation_script):
#       print(command)
        execute(cur, con, command)
#   _ = input(f"Table Names: {get_table_names(cur)}")
    yes_no = input(
            "Populate table with data from Data/my.csv? ")
    if yes_no and yes_no[0] in 'yY':
        for record in data_generator(source_csv):
            query = get_insert_query(record, 'People')
    #       _ = input(query)
            execute(cur, con, query)


def add_contact():
    print('Adding a contact.')
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    record = dict()
    for key in get_field_names(source_csv): 
        record[key] = input(f"{key}: ")
    query = get_insert_query(record, 'People')
    execute(cur, con, query)


def get_keys():
    print('Collecting keys:')
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    query = """Select personID, first, last 
                    FROM People;"""
    execute(cur, con, query)
    res = cur.fetchall()
    print(" ID  First  Last")
    print(' --  -----  ----')
    for item in res:
        print("{:3}: {} {}".format(*item))
    return [item[0] for item in res]


def find_contact():
    keys = get_keys()
    while True:
        peopleID = input("Which contact to display? ")
        if not peopleID:
            return
        if int(peopleID) in keys:
            break
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    query = "SELECT * FROM People WHERE personID = {}"
    execute(cur, con, query.format(peopleID))
    res = cur.fetchall()
    print('|'.join([item for item in res[0][1:]]))


def generate_letter(text_file, recipient, printer="X6505_e9"):
    with open(text_file, 'r') as instream:
        letter = instream.read()
    print(letter)


def generate_letter(text_file, recipientID, printer):
    with open(text_file, 'r') as instream:
        letter = instream.read()
    print(letter)


def prepare_letter():
    text_file = input("File containing letter text: ")
    recipientID = str(input("Recipient ID #: "))
    printer = "X6505_e9"
    response = input(f"Change printer from {printer} to .. ")
    if response:
        printer = response
    generate_letter(text_file, recipientID, printer)


def main():
    menu = '\nI)initiate A)dd F)ind K)eys L)etter Q)uit..'
    while True:
        response = input(menu) 
        if response:
            if response[0] in 'qQ':
                sys.exit()
            elif response[0] in 'iI':
                initiate_db()
            elif response[0] in 'fF':
                find_contact()
            elif response[0] in 'aA':
                add_contact()
            elif response[0] in 'kK':
                get_keys()
            elif response[0] in 'lL':
                prepare_letter()
            else:
                print("Choose a valid entry!")


if __name__ == '__main__':
#   print(get_field_names(source_csv))
    main()

