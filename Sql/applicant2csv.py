#!/usr/bin/env python3

# File: applicant2csv.py

import os
import sys
import csv
sys.path.insert(0, os.path.split(sys.path[0])[0])
#print(sys.path)
import helpers
import data
from rbc import Club


def line2record(line):
    """
    a modified version of what's in data.py
    """
    keys = (
        "first", "last",
        "app_rcvd", "fee_rcvd",   #} date (or empty
        "1st", "2nd", "3rd",      #} string if event
        "inducted", "dues_paid",  #} hasn't happened.
        "sponsor1", "sponsor2",   # empty strings if not available
        'status',
        )

    ret = {}
    for key in keys:
        ret[key] = ''
    parts = line.split('|')
    while not parts[-1]:  # lose trailing empty fields
        parts = parts[:-1]
    parts = [part.strip() for part in parts]
    names = parts[0].split()
    ret['first'] = names[0]
    ret['last'] = names[1]
    dates = parts[1:]
    l = len(dates)
    if parts[-1].startswith("Appl"):
        dates = dates[:-1]  # waste the text
        special_status = "zae"  # see members.STATUS_KEY_VALUES
        l -= 1
    elif parts[-1].startswith("w"):
        dates = dates[:-1]
        special_status = "aw"
        l -= 1
    else:
        special_status = ''
    if l == 0:       # Should never have an entry /w no dates.
        print("Entry for applicant {}{} is without any dates."
                .format(names[0], names[1]))
        sys.exit()
    elif l == 1:               # one date listed
        status = "a-"
    elif l == 2:
        status = "a0"
    elif l == 3:
        status = "a1"
    elif l == 4:
        status = "a2"
    elif l == 5:
        status = "a3"
    elif l == 6:
        status = "ad"
    elif l == 7:
        status = "m"
    else:
        print("Entry for {}{} has an invalid number of dates."
                .format(names[0], names[1]))
        sys.exit()
    data.move_date_listing_into_record(dates, ret)
    if special_status:
        ret['status'] = special_status
    else:
        ret['status'] = status
    return ret


infile = Club.APPLICANT_SPoT
outfile =  Club.APPLICANT_CSV
print(infile)
print(outfile)
club = Club()
data.populate_sponsor_data(club)
sponsored_applicant_keys = set(club.sponsors_by_applicant.keys())
with open(infile, 'r') as instream:
    for line in helpers.useful_lines(instream, comment='#'):
        rec = line2record(line)
        appl_key = "{last},{first}".format(**rec)
        if appl_key in sponsored_applicant_keys:
            rec['sponsor1'] = club.sponsors_by_applicant[
                    appl_key][0]
            rec['sponsor2'] = club.sponsors_by_applicant[
                    appl_key][1]
        print(repr(rec))

