#!/usr/bin/env python3

# File: main.py

"""
Manage data base for a letter writing app.

Can initiate data from any csv file that does not have any
field names not contained in the <creation_script> file.

Note: access to original source
"""

import os
import sys
import csv
import sqlite3
d, f = os.path.split(sys.path[0])
d, f = os.path.split(d)
sys.path.insert(0, d)
# print(sys.path)

import letters
import content

db_file_name = 'Data/contacts.sqldb'
source_csv = 'Data/new.csv'
source_csv = 'Data/my-old.csv'
creation_script = 'creation_script.sql'
test_letter = 'Data/test_letter.txt'

insert_template = """INSERT INTO {table} ({keys})
    VALUES ({values});"""


def get_sql(sql_file):
    """
    Reads what are assumed to be valid SQL queries
    from <sql_file> 'yield'ing them one at a time.
    Usage:
        con = sqlite3.connect("sql.db")
        cur = con.cursor()
        for query in get_sql(sql_commands_file):
            cur.execute(query)
    """
    with open(sql_file, 'r') as in_stream:
        query = ''
        for line in in_stream:
            line = line.strip()
            if line.startswith('--'):
                continue
            query = query + line.strip()
            if line.endswith(';'):
                yield query[:-1]
                query = ''


def csv_data_generator(filename):
    """
    Yield records from a csv data base.
    Used to populate the data base from a csv file.
    """
    with open(filename, 'r', newline='') as instream:
#       reader = csv.DictReader(instream)
        reader = csv.DictReader(instream, restkey='extra')
        for rec in reader:
            yield(rec)


def get_csv_field_names(csv_file):
    """
    Not used.  See get_fieldnames()
    We get field names from the data base instead
    """
    with open(csv_file, 'r', newline='') as instream:
        reader = csv.DictReader(instream)
        return(reader.fieldnames)


def get_insert_query(record, table):
    """
    Returns valid sql syntax to populate <table>
    with all of <record>'s non empty fields.
    """
    keys_w_values = []
    values = []
    for key in [key for key in record.keys()]:
        if key == 'extra':
            continue
        value = record[key]
        if value:
            keys_w_values.append(key)
            if not isinstance(value, str):
                _ = input(f"{key}: {value}")
            value = '"{}"'.format(value)
            values.append(value)
    keys = ', '.join(keys_w_values)
    values = ', '.join(values)
    query = insert_template.format(
            table=table, keys=keys, values=values)
#       _ = input(query)
    return query


def execute(cursor, connection, query):
    """
    Wrapper to provide debugging
    information should a query fail.
    """
    try:
        cursor.execute(query)
    except (sqlite3.IntegrityError, sqlite3.OperationalError):
        print("Unable to execute following query:")
        print(query)
        raise
    connection.commit()


def initiate_db_cmd():
    """
    Re-initializes the data base as per content of files
    declared as globals: db_file_name, creation_script;
    with option to populate with data from source_csv
    """
    print("Initiating the data base.")
    if os.path.exists(db_file_name):
        os.remove(db_file_name)
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    ## set up the tables (first deleting any that exist)
    for query in get_sql(creation_script):
#       print(query)
        execute(cur, con, query)
#   _ = input(f"Table Names: {get_table_names(cur)}")
    yes_no = input(
            "Populate table with data from {}? "
            .format(source_csv))
    if yes_no and yes_no[0] in 'yY':
        for record in csv_data_generator(source_csv):
            query = get_insert_query(record, 'People')
    #       _ = input(query)
            execute(cur, con, query)


def get_fieldnames(includeID=False):
    """
    Returns an iterable of the fieldnames 
    (in the only/People table.)
    Option allows inclusion of the primary key
    (which is left out by default.)
    """
    con = sqlite3.connect(db_file_name)
    cur = con.execute("SELECT * FROM People")
    res = ([item[0] for item in cur.description])
    if not includeID:
        res = res[1:]
    return res


def update():
    show_index()
    idkey = input("Key of record to modify: ")
    display_row(idkey, display=True)
    response = input(
        'Continue with modification of above record? (y/n)')
    if not response or not response in 'yY':
        return
    update_query_template = """UPDATE {table}
        SET {clauses}
        WHERE personID = {personID}
    """
    fieldnames = get_fieldnames()
#   _ = input(fieldnames)
    rec = get_record(idkey)
#   _ = input(rec)
    updates = []
    print("Change fields:")
    print("\t* don't change")
    print("\t$ leave remaining")
    print("\t^ leave blank")
    for key in rec.keys():
        entry = input(f'{key}: {rec[key]}  change to ..  ')
        if entry:
            if entry == '*':  # don't change field
                continue
            if entry == '$':  # leave remaining fields
                break
            if entry == '^':  # blank out
                updates.append((key, '',))
                continue
            updates.append((key, entry,))
#   _ = input(f"updates: {updates}")
    clauses = []
    for key, entry in updates:
        clauses.append(f"{key} = '{entry}'")
    if not clauses:
        print("No update performed.")
        return
    clauses = ', '.join(clauses)
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    execute(cur, con,
        update_query_template.format(table='People',
                                    clauses=clauses,
                                    personID=idkey))


def add_new_contact():
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    record = dict()
    for key in get_fieldnames(): 
        record[key] = input(f"{key}: ")
    query = get_insert_query(record, 'People')
    execute(cur, con, query)


def add_cmd():
    while True:
        response = input(
        'N)ew, U)pdate, Q)uit .. ')
        if response:
            if response[0] in 'uU':
                update()
            elif response[0] in 'nN':
                add_new_contact()
            elif response[0] in 'qQ':
                return


def get_IDs_w_names():
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    query = """Select personID, first, last 
                    FROM People;"""
    execute(cur, con, query)
    return cur.fetchall()


def show_index():
    print('Collecting keys:')
    res = get_IDs_w_names()
    print(" ID  First  Last")
    print(' --  -----  ----')
    for item in res:
        print("{:3}: {} {}".format(*item))


def get_values(peopleID):
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    query = "SELECT * FROM People WHERE personID = {}"
    execute(cur, con, query.format(peopleID))
    res = cur.fetchall()
    return [item for item in res[0][1:]]


def get_record(peopleID):
    values = get_values(peopleID)
    keys = get_fieldnames()
#   _ = input(f'keys: {keys}')
#   _ = input(f'values: {values}')
    ret = dict()
    for key, value in zip(keys, values):
        ret[key] = value
    return ret


def display_row(id=None, display=False):
    keys = [item[0] for item in get_IDs_w_names()]
    if id:
        peopleID = id
    else:
        while True:
            peopleID = input("Which contact to display? ")
            if not peopleID:
                return
            if int(peopleID) in keys:
                break
    values = get_values(peopleID)
    ret = '|'.join(values)
    if display:
        print(ret)


def get_record_id(prompt):
    id_number = input("Id of {}: ".format(prompt))
    return id_number


def get_letter_content(default=None):
    if default:
        file_name = default
    else: 
        file_name = input("File with letter content: ")
    with open(file_name, 'r') as instream:
        content = instream.read()
    return content


def prepare_letter_cmd():
    """
    pick letter
    pick sender
    pick recipient
    set optional re: field
    show_index()
    sender = get_record(get_record_id("Sender Id: "))
    recipient = get_record(get_record_id("Recipient Id: "))
    """
    sender = get_record(2)
    recipient = get_record(7)
    content = get_letter_content(default='Data/test_letter.txt')
    printer = letters.printers["X6505_e9"]
    sink = 'Data/generated_letter.txt'
#   response = input(f"Change printer from {printer} to .. ")
#   if response:
#       printer = response
    letter = letters.letter_text(content, recipient,
            sender, printer, formality=0)
    with open(sink, 'w') as outstream:
        outstream.write(letter)
    print(letter)


def main():
    menu = '\nI)initiate K)eys D)isplay A)dd L)etter Q)uit..'
    while True:
        response = input(menu) 
        if response:
            if response[0] in 'iI':
                initiate_db_cmd()
            elif response[0] in 'kK':
                show_index()
            elif response[0] in 'dD':
                display_row(display=True)
            elif response[0] in 'aA':
                add_cmd()
            elif response[0] in 'lL':
                prepare_letter_cmd()
            elif response[0] in 'qQ':
                sys.exit()
            else:
                print("Choose a valid entry!")


if __name__ == '__main__':
    main()

