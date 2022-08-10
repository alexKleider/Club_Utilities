#!/usr/bin/env python3

# File: add_applicants.py

"""
When applicants come in, create a text file with field/value
names for each applicant and a blank line between applicants.
(See aug6_applicants.text as an example.)
# commented lines are ignored.

Then run this module with the name of that file as its parameter.

Fields must match those in the 'memlist.csv' file:
first,last,phone,address,town,state,postal_code,country,email,dues,dock,kayak,mooring,status

The file is read and a csv file is generated.

Next step to implement is to merge this csv file with the main club
data base csv file.  (Not yet implemented)
"""

FIELDS =(
'first,last,phone,address,town,state,postal_code,country,email,dues,dock,kayak,mooring,status'.split(','))

import sys
import csv

# default (intermediate) output file:
NEW_APPLICANT_CSV = 'new_applicants.csv'

# 'hard wired' file names:   (integrating above into below not yet
# implemented.
MEMBERSIP_FILE = '/home/alex/Git/Club/Data/memlist.csv'
NEW_MEMBERSHIP_FILE = '/home/alex/Git/Club/Data/new_memlist.csv'

membership_file = MEMBERSIP_FILE
new_membership_file = NEW_MEMBERSHIP_FILE
new_applicant_csv = NEW_APPLICANT_CSV

def collect_new_applicants(applicant_file): 
    print("begin 'collect_new_applicants' function")
    ret = []
    with open(applicant_file, 'r') as applicant_stream:
        print('Opening {}'.format(applicant_stream.name))
        new_record = {}
        for line in applicant_stream:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if line.startswith('first'):
                if new_record:
                    new_record['status'] = 'a'
                    ret.append(new_record)
                new_record = {}
            key, value = line.split(': ')
#           print("{}: {}".format(key, value))
            new_record[key] = value
        if new_record:
            new_record['status'] = 'a'
            ret.append(new_record)
    ret.sort(key=lambda d: d['last']+d['first'])
    return ret

def main():
    if len(sys.argv) < 2:
        print("Need to supply an input file!")
        sys.exit()
    if len(sys.argv) > 2:
        new_applicants_csv = sys.argv[2]
    else:
        new_applicant_csv = 
    applicant_file = sys.argv[1]
    new_records = collect_new_applicants(applicant_file)
#   for record in new_records:
#       for key, value in record.items():
#           print('{}: {}'.format(key, value))
    with open(applicant_csv, 'w', newline='') as stream:
        print("Opening {} for writing.".format(stream.name))
        dictwriter = csv.DictWriter(stream, fieldnames=FIELDS)
        dictwriter.writeheader()
        for record in new_records:
            dictwriter.writerow(record)

if __name__ == '__main__':
    main()
