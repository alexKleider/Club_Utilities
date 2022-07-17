#!/usr/bin/env python3

# File: angie.py

"""
The csv file Angie sends me must be subjected to the 'fromdos'
command, then have the first line deleted. After that it becomes
a csv file that this utility can process.
Lines that don't make proper sense (i.e. text in what should be
numeric fields) are printed first followed by a listing of
payments she is reporting.
All output is printed to the screen so typical usage would be
    $ ./code/angie.py [input-file-name]  >  angie-data.txt
.. and then study 'angie-data.txt' and
move new parts to $CLUB/Data/receipts*
An optional input file parameter may be used to override the default
and an optional second parameter can specify an output file.
If want to specify an output param but keep the input as default:
    $ ./code/angie.py None output_file.
"""

notes = """
Angie's keys: 
\ufeffFirst,Last,Deposit,Check Amount,Membership,Dock Fees,Mooring Fee,App  Fee,Kayak Storage,Derby Donation,Other,Notes
My keys:
first,last,phone,address,town,state,postal_code,country,email,dues,dock,kayak,mooring,status
The '\ufeff' declares 'endian' and I haven't figured out how to get
rid of it!  I've just accepted it as part of the key name.
"""

INFILE = 'loose1st.csv'
INFILE = '/home/alex/Git/Club/Data/fromAngie.csv'
INFILE = '/home/alex/Git/Club/Data/angieslist.csv'
FIRST = 'First'
FIRST = '\ufeffFirst'

import csv
import sys

infile = INFILE
outfile = sys.stdout
out_stream = False
if len(sys.argv) > 1:
    if sys.argv[1] != 'None':
        infile = sys.argv[1]
if len(sys.argv) > 2:
    outfile = sys.argv[2]
    out_stream = True

answer = input("In & out put files set to {} & {}. Continue? "
        .format(infile, outfile))
if not (answer and (answer[0] in 'Yy')):
    sys.exit()
collector = {}
errors = {}
money_keys = ('dues', 'dock', 'application', 'kayak', 'mooring', )

#with open(infile, 'r', newline='') as stream:
with open(infile, 'r',
#       encoding='utf-16',
        newline='') as stream:
    reader = csv.DictReader(stream, dialect='excel')
#   print(reader.fieldnames)
    for record in reader:
#       print(record)
        ret_rec = {}  # Note       vvvvvv   special char!
        ret_rec['first'] = record[FIRST]
        ret_rec['last'] = record['Last']
        ret_rec['dues'] = record['Membership']
        ret_rec['dock'] = record['Dock Fees']
        ret_rec['application'] = record['App  Fee']
        ret_rec['kayak'] = record['Kayak Storage']
        ret_rec['mooring'] = record['Mooring Fee']
        key = "{first} {last}".format(**ret_rec)
        for money_key in money_keys:
            if ret_rec[money_key]:
                try:
                    ret_rec[money_key] = int(ret_rec[money_key])
                except ValueError:
                    errors[key] = ("{}: {}".format(money_key,
                                                ret_rec[money_key]))
                    ret_rec[money_key] = ''
        collector[key] = ret_rec

res = []
for name_key in collector.keys():
    entry = ''
    total_paid = 0
    for money_key in money_keys:
        val = collector[name_key][money_key]
        if val:
            total_paid += int(val)
            entry = (entry + ' ' + '{}: {}'
                    .format(money_key, val))
    if entry:
        text = ("{:<24}{:>3d}".format(name_key, total_paid)
                + "  (" + entry + ")")
        shorter_text = text.replace("( dues: 100", '(')
        if shorter_text.endswith('  ()'):
#           print("found ' ( )'")
            shorter_text = shorter_text[:-4]
#       shorter_text = text
#       if shorter_text != text: print("no change")
        res.append(shorter_text)

error_keys = errors.keys()

def display(stream=sys.stdout):
    if error_keys:
        print("\nERRORS", file=stream)
        print("\n======", file=stream)
        for key in error_keys:
            print("{}  {}".format(key,errors[key]), file=stream)
    if res:
        print("\nPAYMENTS", file=stream)
        print("\n========", file=stream)
    for item in res:
        print(item, file=stream)

if out_stream:
    with open(outfile, 'w') as out_stream:
        display(out_stream)
else: display()
