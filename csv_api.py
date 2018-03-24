#!/usr/bin/env python3

# File: csv_api.py

import csv
from utils import Membership as M

"""
# Membership (M) indeces:
    i_first= 0
    i_last = 1
    i_address = 2
    i_town = 3
    i_state = 4
    i_zip = 5
    i_email = 6
    i_email_only = 7
    i_dues = 8
    i_mooring = 9
    i_dock = 10
    i_kayak = 11

    n_fields_per_record = 12

    membership_dues = 100
"""

infile = "memlist.csv"
outfile = "newlist.csv"

def get_csv(file_name):
    working_list = []
    with open(infile, 'r', newline='') as f_obj:
        reader = csv.reader(f_obj, dialect='excel')
        for row in reader:
            working_list.append(row)
    return working_list

def change_data(csv_data, func):
    new_data = []
    for row in csv_data:
        new_data.append(func(row))
    return new_data

def put_csv(data, file_name):
    with open(file_name, 'w', newline='') as f_obj:
        writer = csv.writer(f_obj, dialect='excel')
        for row in data:
            print(row)
            writer.writerow(row)

# Define 'funcs' here:

# def add_membership_fee(csv_row):
     """
     Don't run this one again- not idempotent!!!
     """
#     return csv_row[:8] + ["100"] + csv_row[8:]

if __name__ == "__main__":
    working_list = get_csv(infile)
    new_data = change_data(working_list, add_membership_fee)
    put_csv(new_data, outfile)

