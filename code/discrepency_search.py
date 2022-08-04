#!/usr/bin/env python3

# File: discrepency_search.py


"""
Usage:
    ./code/discrepency_search.py [infile [outfile]]
An optional input file parameter may be used to override the default
and an optional second parameter can specify an output file.
If want to specify an output param but keep the input as default:
    $ ./code/discrepency_search.py None output_file.

Reads MEMLIST = '/home/alex/Git/Club/Data/memlist.csv' and uses it to
check for data consistency.

Will generate a 'thankfile' called 'code/2thank.csv'.
"""

import os
import csv
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])
import helpers
import data
import rbc

INFILE = '/home/alex/Git/Club/Utils/code/receipts.txt'
OUTFILE = '/home/alex/Git/Club/Utils/code/checked-totals.txt'
THANKFILE = 'code/2thank.csv'

MEMLIST = '/home/alex/Git/Club/Data/memlist.csv'
infile = INFILE
outfile = OUTFILE
if len(sys.argv) > 1:
    if sys.argv[1] != 'None':
        infile = sys.argv[1]
if len(sys.argv) > 2:
    outfile = sys.argv[2]

club = data.club_with_payables_dict(MEMLIST)
owers = club.owing_dict.keys()

debug = """
print("Those Owing")
keys = sorted(club.owing_dict.keys())
for key in keys:
    print("{}: {}".format(key, club.owing_dict[key]))
answer = input("In & out put files set to {} & {}. Continue? "
        .format(infile, outfile))
if not (answer and (answer[0] in 'Yy')):
    sys.exit()
"""

collector = {}  # keys will be last,first names,
                # values will be what's been payed.
# First deal with the latest entries in Angie's list of receipts:
with open(infile, 'r') as instream:
    print("Reading from {}".format(instream.name))
    for line in helpers.useful_lines(instream):
        parts = line.split()
        collector['{},{}'.format(parts[1], parts[0])] = int(parts[2])
keys = sorted(collector.keys())

res = ['',
       'Money collected',
       '===============',
      ]
for key in keys:
    res.append("{}: {}".format(key, collector[key]))

payors = collector.keys()
payors_not_owing = set(payors).difference(owers)
if payors_not_owing:
    res.extend(['',
       "Paid but don't owe!",
       '===================',
      ])
    for payor in sorted(payors_not_owing):
        res.append(payor)
else:
    res.append("\nall payors are in owing")

with open(outfile, 'w') as outstream:
    print("writing to {}".format(outstream.name))
    for line in res:
        outstream.write(line + '\n')

# Create a csv file of members who have paid & need to be thanked:
with open(MEMLIST, 'r', newline='') as memliststream:
    print("Reading from {}".format(memliststream.name))
    dict_reader = csv.DictReader(memliststream, restkey='extra')
    fieldnames = dict_reader.fieldnames
    with open(THANKFILE, 'w') as thankstream:
        print("Writing to {}".format(thankstream.name))
        dict_writer = csv.DictWriter(thankstream,
                                    fieldnames,
                                    lineterminator='\n'
                                    )
        dict_writer.writeheader()
        for record in dict_reader:
            key = '{last},{first}'.format(**record)
            if key in payors:
                # For time being assume paid what's owed..
                dict_writer.writerow(record)

