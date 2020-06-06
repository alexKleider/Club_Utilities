#!/usr/bin/env python3

# File: change_db.py

"""
A script being written to remove the 'email_only' field
from the Data/memlist.csv data base.
"""

import csv

#OLD_CSV = 'Tests/shortlist.csv'
OLD_CSV = 'Data/memlist.csv'
NEW_CSV = 'new_data.csv'
ERROR_FILE = '2check'

with open(OLD_CSV, 'r') as infile:
    dict_reader = csv.DictReader(infile)
    fieldnames = dict_reader.fieldnames
    print(fieldnames)
    new_keys = [key for key in fieldnames if not key=='email_only']
    with open(ERROR_FILE, 'w') as errors:
        with open(NEW_CSV, 'w') as outfile:
            dict_writer = csv.DictWriter(outfile, fieldnames=new_keys)
            print(new_keys)
            dict_writer.writeheader()

            for in_record in dict_reader:
                print(in_record)
                new_dict = {}
                for key in new_keys:
                    new_dict[key] = in_record[key]
                    print(
                        "key:'{}' old value: '{}' =>  new value: '{}'"
                        .format(key, in_record[key], new_dict[key]))
                dict_writer.writerow(new_dict)
#               print(new_dict, file=errors)
            fname = outfile.name
print("New data written to '{}'.".format(fname))
''' 
'''
