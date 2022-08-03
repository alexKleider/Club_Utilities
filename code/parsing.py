#!/usr/bin/env python3

# File: parsing.py

import sys
import os

sys.path.insert(0, os.path.split(sys.path[0])[0])

import rbc
import helpers

def parse_receipts(infile=rbc.Club.RECEIPTS_FILE, errors=None):
    this_year = repr(helpers.this_year)
    res = {}
    report_errors = False
    if not errors == None:
        report_errors = True
    with open(infile, 'r') as stream:
        for line in helpers.useful_lines(stream):
            parts = line.split()
            if parts[0] in {this_year,
                            'Date:',
                            'SubTotal',
                            'Grand',
                            } or line.startswith("="):
                continue
            if len(parts)<3 and report_errors:
                errors.append(line)
            else:
                res["{},{}".format(parts[1],parts[0])] = parts[2]
    return res


if __name__ == '__main__':
    errors = []
    for key, value in sorted(parse_receipts(errors=errors).items()):
        print("{0}: {1}".format(key, value))
    if errors:
        print('\nErrors')
        print(  '======')
        for error in errors:
            print(error)
