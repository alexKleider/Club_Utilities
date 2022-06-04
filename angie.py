#!/usr/bin/env python4

# File: angie.py

"""
Angie's keys: 
First,Last,Deposit,Check Amount,Membership,Dock Fees,Mooring Fee,App  Fee,Kayak Storage,Derby Donation,Other,Notes
My keys:
first,last,phone,address,town,state,postal_code,country,email,dues,dock,kayak,mooring,status
"""

INFILE = '/home/alex/Git/Club/Data/fromAngie.csv'
INFILE = 'loose1st.csv'

import csv

collector = {}
errors = {}
money_keys = ('dues', 'dock', 'application', 'kayak', 'mooring', )

#with open(INFILE, 'r', newline='') as stream:
with open(INFILE, 'r',newline='') as stream:
    reader = csv.DictReader(stream, dialect='excel')
#   print(reader.fieldnames)
    for record in reader:
#       print(record)
        ret_rec = {}  # Note       vvvvvv   special char!
        ret_rec['first'] = record['\ufeffFirst']
        ret_rec['last'] = record['Last']
        ret_rec['dues'] = record['Membership']
        ret_rec['dock'] = record['Dock Fees']
        ret_rec['application'] = record['App  Fee']
        ret_rec['kayak'] = record['Kayak Storage']
        ret_rec['mooring'] = record['Mooring Fee']
        key = "{first} {last}: ".format(**ret_rec)
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
    for money_key in money_keys:
        val = collector[name_key][money_key]
        if val:
            entry = (entry + ' ' + '{}: {}'
                    .format(money_key, val))
    if entry:
        res.append(name_key + entry)

for key in errors.keys():
    print("{}  {}".format(key,errors[key]))
for item in res:
    print(item)

