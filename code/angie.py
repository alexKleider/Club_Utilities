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

import os
import csv
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])
import helpers
import data
import rbc

MEMLIST = '/home/alex/Git/Club/Data/memlist.csv'
INFILE = '/home/alex/Git/Club/Data/angie220731.csv'
INFILE = '/home/alex/Git/Club/Utils/code/fromAngie.csv'
ERROR_FILE =  '/home/alex/Git/Club/Utils/code/errors.txt'

club = data.club_with_payables_dict(MEMLIST)
owers = club.owing_dict.keys()

FIRST = 'First'        # Can't get rid of the 'endian' prefix...
FIRST = '\ufeffFirst'  # ... which is contaminating header line.

money_keys = ( 'dues',
               'application',
               'dock',
               'kayak',
               'mooring',
               )

correspondence = (
        ('first', FIRST),
        ('last', 'Last'),
        ('dues', 'Membership'),
        ('dock', 'Dock Fees'),
        ('application', 'App  Fee'),  # note 2 spaces
        ('kayak', 'Kayak Storage'),
        ('mooring', 'Mooring Fee'),
        )


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


def parse_angies_csv(infile, owers=None, errors=None):
    """
    <infile> is an 'Angie generated' csv file.
    Returned is a dict:
        keys are last,first names
        values are dicts keyed by what's being paid
        i.e.  Last,First: {'dues': 100, 'dock': 75}
    If errors is a list, it'll be populated (side effect.)
    """
    collect_errors = False
    if isinstance(errors, list):
        collect_errors = True
    #  collect data from input file => collector
    collector = {}
    print("Reading {}".format(infile))
    with open(infile, 'r',
    #       encoding='utf-16',
            newline='') as stream:
        reader = csv.DictReader(stream, dialect='excel')
    #   print(reader.fieldnames)
        ck = 0
        for record in reader:
    #       print(record)
            total = 0
            if (not record[FIRST]
                or not record['Last']
                or record['Check Amount'] == record['Other']
                ):
                continue
            ret_rec = {}  # Note       vvvvvv   special char!
            for key1, key2 in correspondence:
                ret_rec[key1] = record[key2].strip()
            key = "{last},{first}".format(**ret_rec)
            if ck == 0:
                print(owers)
                ck += 1
            if owers and (not (key in owers)):
                errors.append("{} not in owers.".format(key))
            ret_rec.pop('first')
            ret_rec.pop('last')
            for money_key in money_keys:
                if ret_rec[money_key]:
                    try:
                        ret_rec[money_key] = int(
                                ret_rec[money_key])
                    except ValueError:
                        errors.append("{}: {}: {}\n"
                                .format(key, money_key,
                                        ret_rec[money_key]))
                        ret_rec[money_key] = 0
                    total += ret_rec[money_key]
                if not ret_rec[money_key]:
                    ret_rec.pop(money_key)
            ret_rec['total'] = total
            if not total:
                errors.append("{}: {}\n".format(key, repr(record)))
            collector[key] = ret_rec
    return collector

def key2name(key):
    names = key.split(',')
    return '{1} {0}'.format(*names) 


def text4receipts(receipts_dict):
    """
    <receipts_dict> is output from parse_angies_csv.
    Returns an array of lines to append to the receipts file.
    """
    ret = []
    for key, value in receipts_dict.items():
        entry =  "{:<27}{:>5}".format(key2name(key), value['total'])
        payments = ["{}: {}".format(k, v) for k, v in value.items()
                if k not in {'dues', 'total'}]
        addendum = ', '.join(payments)
        if addendum:
            entry = entry + '  (' + addendum + ')'
        ret.append(entry)
    return ret

def main():
    infile = INFILE
    # outfile = 'code/receipts'
    outfile = sys.stdout
    if len(sys.argv) > 1:
        if sys.argv[1] != 'None':
            infile = sys.argv[1]
    if len(sys.argv) > 2:
        outfile = sys.argv[2]

    answer = input("In & out put files set to {} & {}. Continue? "
            .format(infile, outfile))
    if not (answer and (answer[0] in 'Yy')):
        sys.exit()

    errors = []
    money_keys = ('dues', 'dock', 'application', 'kayak', 'mooring', )

    collector = parse_angies_csv(infile, owers=owers, errors=errors)
    print(repr(errors))
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

    #!!!!!!!!!!!!!!!! changed errors to a list
    error_keys = errors.keys()

    error_header = ['# INVALID LINES',
                    '# =============',
                    ]

    payments_header = ['# PAYMENTS',
                       '# ========',
                       ]

    writecode = 'w'

    if error_keys:
        print("writing to {}".format(outfile))
        with open(outfile, writecode) as outstream:
            if error_keys:
                display(dict2list(errors), '# INVALID LINES', outstream)
                display([], '', outstream)  # white space for separation
            writecode = 'a'
    if res:
        print("writing to {}".format(outfile))
        with open(outfile, writecode) as outstream:
            display(dict2list(res), '# PAYMENTS', outstream)

def dev():
    errors = []
    infile = INFILE
    error_file = ERROR_FILE
    res = parse_angies_csv(infile, owers=owers, errors=errors)
    outfile = 'code/receipts.txt'
    print("writing to {}".format(outfile))
    with open(outfile, 'w') as stream:
        for line in text4receipts(res):
            stream.write(line + '\n')
    if errors:
        print("Encountered error(s) sent to {}"
                .format(error_file))
        with open(error_file, 'w') as stream:
            for item in errors:
                stream.write(item + '\n')

if __name__ == '__main__':
    dev()
