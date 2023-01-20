#!/usr/bin/env python3

# File: main.py

"""
Manage data base for a letter writing app.
"""

import sys
import sqlite3

menu = '''I)initiate A)dd F)ind Q)uit..'''


def initiate_db():
    print("Initiating the data base.")


def find_contact():
    contact = input("Which contact(s) to display?")
    print(f"Displaying {contact}'s info:")


def add_contact():
    print('Adding a contact.')


def main():
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
            else:
                print("Choose a valid entry!")


if __name__ == '__main__':
    main()

