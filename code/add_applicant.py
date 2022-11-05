#!/usr/bin/env python3

# File: eg_applicant.py

"""
Usage:
    ./eg_applicant.py [infilename [outfilename]]

Prints a line of comma separated values which can
be redirected into (>) or appended to (>>) a file.

Positional argument <infilename>, if provided,
must have one field value per line in the correct order.
If used then <outfilename> may also be provided for output.
Data is appended (so as not to overwrite if file exists.)

A work in progress...

"""
import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])
# print(sys.path)
import helpers
from rbc import Club

applicant = dict(
    first= '',
    last= '',
    phone= '',
    address= '',
    town= '',
    state= '',
    postal_code= '',
    country= '',
    email= '',
    sponsor1= '',
    sponsor2= '',
    date= '',
    )
keys = applicant.keys()


if len(sys.argv) > 1:
    # read data from a file...
    with open(sys.argv[1], 'r') as instream:
        values = helpers.useful_lines(instream)
        for key in keys:
            applicant[key] = next(values)
#           print(f"{key}: {applicant[key]}")
else:
    for key in keys:
        applicant[key] = input(f"\t{key}: ")

values = [applicant[key] for key in applicant.keys()]
ret = ','.join(values)
if len(sys.argv) == 3:
    with open(sys.argv[2], 'a') as outstream:
        outstream.write(ret)
else:
    print(ret)
