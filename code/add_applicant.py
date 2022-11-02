#!/usr/bin/env python3

# File: eg_applicant.py

"""
Usage:
    ./eg_applicant.py [filename]


Positional argument <filename>, if provided,
must have one field value per line in the correct order.

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
print(','.join(values))
