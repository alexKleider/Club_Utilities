#!/usr/bin/env python3

# File: add_data.py

"""
This module takes data in the format (csv and text files)
I've been using for maintaining Club data and moves it
all into an sqlite3 data base. See the ## GLOBALS section:
these will need to be changed if/when going live with
our real data.
https://docs.python.org/3/library/sqlite3.html
"""

import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])
import csv
import sqlite3
import rbc
import member
import data
import helpers

## GLOBALS
db_file_name = "Sanitized/club.db"
sql_commands_file = 'create_tables.sql'  # table creating commands
membership_csv_file = "Sanitized/members.csv"
applicant_text_file = 'Sanitized/applicants.txt'
sponsor_text_file = 'Sanitized/sponsors.txt'
## END of GLOBALS

insert_template = """INSERT INTO {table} ({keys})
    VALUES({values});"""
pull_ID_query = """SELECT personID from People
WHERE People.first = "{first}" AND People.last = "{last}" """


def get_id_by_name(cur, con, first, last):
    """
    Returns People.personID for person with <first> <last> name
    """
    query = pull_ID_query.format(first=first, last=last)
#   _ = input(query)
    execute(cur, con, query)
    res = cur.fetchall()
    if not res:
        _ = input("No key for {} {}".format(first, last))
        return
    if len(res) > 1 or len(res[0]) > 1:
        print("too many values returned by get_id_by_name")
        sys.exit()
    return res[0][0]


def get_IDs_by_person(con, cur):
    ret = dict()
    query = """
        SELECT personID, first, last 
        From People; """
    execute(cur, con, query)
    for sequence in cur.fetchall():
        ret[f"{sequence[2]},{sequence[1]}"] = sequence[0]
    return ret


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
        command = []
        for line in in_stream:
            line = line.strip()
            if line.startswith('--'):
                continue
            command.append(line.strip())
            if line.endswith(';'):
                line = line[:-1]
                yield ' '.join(command)
                command = []


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


def shorten_rec(rec):
    ret = {}
    for key in rec.keys():
        ret[key] = rec[key]
        if key == 'email':
            break
    return ret


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


def execute(cursor, connection, command):
    try:
        cursor.execute(command)
    except (sqlite3.IntegrityError, sqlite3.OperationalError):
        print("Unable to execute following query:")
        print(command)
        raise
    connection.commit()


def populate_people(source, connection, cursor):
    """
    Adds all data from <source> into the "people" SQL table.
    Note: a suffix field is added to each record.
    """
    for rec in data_generator(source):
        ret = shorten_rec(rec)
        keys = ', '.join([key for key in ret.keys()])
        values = [value for value in ret.values()]
        values = ', '.join([f"'{value}'" for value in ret.values()])
        command = insert_template.format(
                    table='People', keys=keys, values=values)
#       _ = input(command)
        execute(cursor, connection, command)


def get_applicant_data(applicant_source, sponsor_source):
    """
    Parses the two files/parameters returning a dict.
    """
    club = rbc.Club()
    club.applicant_spot = applicant_source
    club.sponsors_spot = sponsor_source
    club.infile = 'Sanitized/members.csv'
    data.populate_sponsor_data(club)
    data.populate_applicant_data(club)
#   _ = input(club.applicant_data)
    return club.applicant_data


def one2two(name):
    n = name.find('_')
    suffix = name[n+1:]
    if n > -1 and len(suffix) == 2:
        return name[:-3], suffix
    else:
        return  name, ''


def change_name_key(name):
    last, first = name.split(',')
    last, suffix = one2two(last)
    return ','.join((last, first, suffix))


def change_name_field(name_field):
    first, last = name_field.split()
    last, suffix = one2two(last)
    return f"{first} {last} {suffix}"


def fix_applicant_data(data):
    """
    Changes records to include 'suffix' field and keys
    are name keys are changed from 'last,first' to
    'last,first,suffix'.
    """
    ret = {}
    for key in data.keys():
        new_key = change_name_key(key)
        ret[new_key] = {}
        for subkey in data[key].keys():
            if subkey == 'last':
                last, suffix = one2two(data[key][subkey])
                ret[new_key]['last'] = last
                ret[new_key]['suffix'] = suffix
                pass
            elif subkey in ('sponsor1', 'sponsor2'):
                if data[key][subkey]:
                    ret[new_key][subkey] = change_name_field(
                                        data[key][subkey])
                else:
                    ret[new_key][subkey] = data[key][subkey]
            else:
#               _ =  input(f"""{new_key} | {subkey} | {key} | {subkey}
#{data[key][subkey]}""")
                ret[new_key][subkey] = data[key][subkey]
    return ret


def populate_applicant_data(applicant_data, valid_names,
                                con, cur):
    """
    <applicant_data> is a dict collected by get_applicant_data
    <valid_names> provided to ensure that all applicants and
    sponsors are already in the 'People' table of the db.
    Murchant_Mr,Jacob
        first: Jacob
        last: Murchant_Mr
        status: a3
        app_rcvd: 220315
        fee_rcvd: 220315
        1st: 220506
        2nd: 220701
        3rd: 221007
        inducted: 
        dues_paid: 
        sponsor1: Al Forest
        sponsor2: George Krugger
    """
    # first check validity of names (both applicant and sponsors)
    names = set()  # set of names we will want to check
    for key in applicant_data.keys():
        names.add(key)  # add applicants to the names to check
        sponsors = set()  # collect sponsor names (in key format)
        for sponsor in ('sponsor1', 'sponsor2'):
            if applicant_data[key][sponsor]:
                sponsors.add(helpers.tofro_first_last(
                    applicant_data[key][sponsor]))
        names.update(sponsors)  # adding sponsors
    if not set(valid_names).issuperset(names):
        print("Invalid names found...")
#       _ = input(names.difference(set(valid_names)))
    else:
        pass
#       print(names)

    # must get <personID>s for applicants and sponsors
    ids_by_name = {}
    for name in names:   # names of applicants & sponsors
        last, first = name.split(',')
        query = f"""SELECT personID from People
WHERE People.first = "{first}" AND People.last = "{last}" """
        execute(cur, con, query)
        query_result = cur.fetchall()
        ids_by_name[name] = query_result[0][0]
#   print(ids_by_name)

    # now ready to populate tables
    applicant_insertion_template = """INSERT INTO
                    Applicants (
                    personID,
                    app_rcvd, fee_rcvd,
                    meeting1, meeting2, meeting3,
                    inducted, dues_paid
                    )
                    VALUES (
                    {personID},
                    {app_rcvd},
                    {fee_rcvd},
                    {1st},
                    {2nd},
                    {3rd},
                    {inducted},
                    {dues_paid}
                    );"""
    sponsor_insertion_template =  """INSERT INTO
                    Sponsors
                    (personID, sponsorID)
                    VALUES ({}, {});"""
    for applicant in applicant_data.keys():
        personID = ids_by_name[applicant]
        data = applicant_data[applicant]
        for sponsor in ('sponsor1', 'sponsor2',):
            sponsor_name = data[sponsor]
            if sponsor_name:
                name_key = helpers.tofro_first_last(sponsor_name)
                sponsorID = ids_by_name[name_key]
                query = sponsor_insertion_template.format(
                        int(personID), int(sponsorID))
#               _ = input(query)
                execute(cur, con, query)
        data['personID'] = personID
        for key in data.keys():
            if not data[key]:
                data[key] = 'NULL'
#       _ = input(data)
        query = applicant_insertion_template.format(**data)
#       print("query is ..")
#       _ = input(query)
        execute(cur, con, query)


def get_table_names(cur):
    res = execute(cur, con, "SELECT name FROM sqlite_master")
    # returns a list of tuples!
    # in this case: each one tuple is a table name
    tups = [tup[0] for tup in res.fetchall()]
    return ', '.join(tups)


def get_people_keys(con, cur):
    execute(cur, con, 'SELECT first, last FROM people')
    people = cur.fetchall()
    return set([f"{names[1]},{names[0]}" for names in people])


def populate_Stati_table(con, cur):
    """
    """
    stati_insertion_template = """INSERT INTO
                    Stati
                    (key, text)
                    VALUES ("{}", "{}");"""
    for key, value in member.STATUS_KEY_VALUES.items():
        query = stati_insertion_template.format(key, value)
        execute(cur, con, query)


def get_statusIDs_by_key(con, cur):
    query = "SELECT statusID, key FROM Stati;"
    execute(cur, con, query)
    ret = dict()
    for tup in cur.fetchall():
        ret[tup[1]] = tup[0]
    return ret


def retrieve_personID(con, cur, last_first_key):
    pass


def populate_Person_Status_table(con, cur,
        IDs_by_person, statusIDs_by_key):
    status_insertion_template = """INSERT INTO
                    Person_Status
                    (personID, statusID)
                    VALUES ("{}", "{}");"""
    with open(membership_csv_file, 'r', newline='') as instream:
        reader = csv.DictReader(instream)
        for record in reader:
            first = record['first']
            last = record['last']
            stati = member.get_status_set(record)
            if member.is_member(record):
                stati.add('m')
            personID = IDs_by_person[
                f"{last},{first}"]
            for status in stati:
                statusID = statusIDs_by_key[status]
                execute(cur, con,
                    status_insertion_template.format(
                    personID, statusID))


def main():
    if os.path.exists(db_file_name):
        os.remove(db_file_name)
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    ## set up the tables (first deleting any that exist)
    for command in get_commands(sql_commands_file):
#       print(command)
        cur.execute(command)
#   _ = input(f"Table Names: {get_table_names(cur)}")
    populate_people(membership_csv_file, con, cur)
    # collect a set of valid name keys (people_keys)
#   key = get_id_by_name(cur, con, 'Bill', 'Smithers')
#   sys.exit()
    IDs_by_person = get_IDs_by_person(con, cur)
    people_keys = IDs_by_person.keys()

    applicant_data = get_applicant_data(applicant_text_file,
                                sponsor_text_file)
#   _ = input(applicant_data)
    populate_applicant_data(
            applicant_data, people_keys, con, cur)
    populate_Stati_table(con, cur)
    populate_Person_Status_table(con, cur,
            IDs_by_person, get_statusIDs_by_key(con, cur))
    con.close()

if __name__ == '__main__':
    main()
