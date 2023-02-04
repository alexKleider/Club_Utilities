#!/usr/bin/env python3

# File: query1.py

import sqlite3
import add_data

db_file_name = "Sanitized/club.db"
query_file = "query1.sql"


def main():
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    for command in add_data.get_commands(query_file):
        print(command)
        print()
        add_data.execute(cur, con, command)
#       print(cur.fetchall())
        for sequence in cur.fetchall():
            print(sequence)
            if sequence[-1] == 'aw':
                print('\t{}'.format(sequence))



if __name__ == '__main__':
    main()
