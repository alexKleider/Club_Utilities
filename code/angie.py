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
$ ./angie.py > 2check
and then study '2check' and move new parts to $CLUB/Data/receipts*
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

collector = {}
errors = {}
money_keys = ('dues', 'dock', 'application', 'kayak', 'mooring', )

#with open(INFILE, 'r', newline='') as stream:
with open(INFILE, 'r',
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
if error_keys:
    print("\nERRORS")
    print("\n======")
    for key in error_keys:
        print("{}  {}".format(key,errors[key]))
if res:
    print("\nPAYMENTS")
    print("\n========")
for item in res:
    print(item)

