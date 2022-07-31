#!/usr/bin/env python3

# File: angie.py

"""
Usage:
    ./angie.py [input file (None if default)] [output file: default is
    stdout]

Options:
    infile defaults to 'code/fromAngie.csv', 'None' > default.
    outfile defaults to stdout. Suggest 'code/receipts.txt'

The csv file Angie sends me must be subjected to the 'fromdos'
command, then have the first line deleted. After that it becomes
a csv file that this utility can process.
Use it as input to this utility. Default is code/fromAngie.csv

Lines that don't make proper sense (i.e. text in what should be
numeric fields) are printed first. The rest of the output is
a listing of payments she is reporting.

If an output file is not specified (as a second parameter:)
output is printed to the screen so typical usage would be
    $ ./code/angie.py [input-file-name]  >  receipts.txt.txt

The output file should be examined for errors; Note that names may
not match club data base- pass what's been collected since last run
into an input file for code/discrepency_search.py. 
Once clean up has been done, can then move relevant parts (payments
that came in since last reported) to $CLUB/Data/receipts*

An optional input file parameter may be used to override the default
and an optional second parameter can specify an output file.
If want to specify an output file but use the default input file
use 'None' as a first parameter as follows:
    $ ./code/angie.py None code/receipts.txt
"""

notes = """
Angie's keys: 
\ufeffFirst,Last,Deposit,Check Amount,Membership,Dock Fees,Mooring Fee,App  Fee,Kayak Storage,Derby Donation,Other,Notes
My keys:
first,last,phone,address,town,state,postal_code,country,email,dues,dock,kayak,mooring,status
The '\ufeff' declares 'endian' and I haven't figured out how to get
rid of it!  I've just accepted it as part of the key name.
"""

INFILE = '/home/alex/Git/Club/Utils/code/fromAngie.csv'

FIRST = 'First'        # Can't get rid of the 'endian' prefix...
FIRST = '\ufeffFirst'  # ... which is contaminating header line.

import csv
import sys

infile = INFILE
outfile = sys.stdout
# outfile = 'code/receipts'
if len(sys.argv) > 1:
    if sys.argv[1] != 'None':
        infile = sys.argv[1]
if len(sys.argv) > 2:
    outfile = sys.argv[2]

answer = input("In & out put files set to {} & {}. Continue? "
        .format(infile, outfile))
if not (answer and (answer[0] in 'Yy')):
    sys.exit()


def dict2list(dic, formatter='{:<24}{}'):
    """
    """
    return [ formatter.format(key, value) for key, value in
            dic.items()]


def display(listing, header, stream):
        print("\n" + header, file=stream)
        print(  "=" * len(header), file=stream)
        for item in listing:
            print(item, file=stream)


collector = {}
errors = {}
money_keys = ('dues', 'dock', 'application', 'kayak', 'mooring', )

#  collect data from input file => collector
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


# convert what's been collected into useful format
res = {}
for name_key in collector.keys():
    entry = ''
    addendum = []
    total_paid = 0
    for money_key in money_keys:
        val = collector[name_key][money_key]
        if val:
            total_paid += int(val)
            entry = (entry + ' ' + '{}: {}'
                    .format(money_key, val))
    if entry:
        # {:<24}
        text = ("{:>3d}".format(total_paid)
                + "  (" + entry + ")")
        shorter_text = text.replace("( dues: 100", '(')
        if shorter_text.endswith('  ()'):
#           print("found ' ( )'")
            shorter_text = shorter_text[:-4]
#       shorter_text = text
#       if shorter_text != text: print("no change")
        res[name_key] = shorter_text

error_keys = errors.keys()

error_header = ['# INVALID LINES',
                '# =============',
                ]

payments_header = ['# PAYMENTS',
                   '# ========',
                   ]

writecode = 'w'

if error_keys:
    with open(outfile, writecode) as outstream:
        if error_keys:
            display(dict2list(errors), '# INVALID LINES', outstream)
            display([], '', outstream)  # white space for separation
        writecode = 'a'
if res:
    with open(outfile, writecode) as outstream:
        display(dict2list(res), '# PAYMENTS', outstream)

