#!/usr/bin/env python3

# File: query.py

import sqlite3
import add_data

db_file_name = "Sanitized/club.db"
sql1 = "query.sql"

def main():
    con = sqlite3.connect(db_file_name)
    cur = con.cursor()
    for command in add_data.get_commands(sql1):
        print(command)
        add_data.execute(cur, con, command)
        print(cur.fetchall())
        for sequence in cur.fetchall():
            print(sequence)



if __name__ == '__main__':
    main()
