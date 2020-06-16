#!/usr/bin/env python3

# File: change_db.py

"""
A script being written to remove the 'email_only' field
from the Data/memlist.csv data base.
It could be modified to make other changes to the database
if/when the need arises.

Usage:
    ./change_db.py [in_file [out_file]]

Options:
    Both <infile> and <out_file> have defaults set.
    (See constants declared below.)
"""

import sys
import csv

#OLD_CSV = 'Tests/shortlist.csv'
OLD_CSV = 'Data/memlist.csv'
NEW_CSV = 'new_data.csv'
ERROR_FILE = '2check'

if len(sys.argv) > 1:
    OLD_CSV = sys.argv[1]
if len(sys.argv) > 2:
    NEW_CSV = sys.argv[2]

response = input(""""Input coming from {}.
Output going to {}.
OK to proceed? """.format(OLD_CSV, NEW_CSV))

if response and response[0] in 'yY':
    pass
else:
    sys.exit()

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
                new_dict = {}
                for key in new_keys:
                    new_dict[key] = in_record[key]
                dict_writer.writerow(new_dict)
#               print(new_dict, file=errors)
            fname = outfile.name
print("New data has been written to '{}'.".format(fname))

