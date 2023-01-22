#!/usr/bin/env python3

# File: merge2csv.py

"""
Usage:
    ./merge2csv.py fieldnames csv1 csv2 new_csv

Args:
    fieldnames: a >=1 line file containing a comma
        separated listing of all field names needed.
    csv1:  }  two csv files to
    csv2:  }  combine into ...
    new_csv

We assume that 1. keys "first" and "last" appear in ...
and 2. fields specified in <fieldnames> includes 
all field names of ...             both csv1 and csv2.
<new_csv> will contain records of both csv1 and csv2
with added keys as necessary so that all keys specified
by <fieldnames> are included.
NOTE: The order in which the two csv files are specified matters!
The content of the second takes precedence.
"""

import sys
import csv

args = sys.argv

if len(args) != 5:
    print(__doc__)
    sys.exit()


def get_new_keys(key_file):
    """
    Returns a listing of the comma separated values
    found in a file called <key_file>.
    """
    collector = []
    with open(key_file, 'r') as instream:
        for line in instream:
            line = line.strip()
            line = line.split(',')
            line = [item for item in line if item]
            collector.extend(line)
    return collector



def collect_dict(csv_file, new_keys):
    """
    Returns a dict keyed by last,first with values
    which are records (dicts) with all new_keys populated
    using empty strings if csv_file doesn't contain the key.
    """
    collector = dict()
    with open(csv_file, 'r', newline='') as instream:
        reader = csv.DictReader(instream)
        keys_in_row = reader.fieldnames
        for row in reader:
            name_key = f"{row['last']},{row['first']}"
            values = dict()
            for key in new_keys:
                if key in keys_in_row:
                    values[key] = row[key]
                else:
                    values[key] = ''
            collector[name_key] = values
    return collector


def populate_csv_file(file_name, fieldnames, dict_of_records):
    with open(file_name, 'w', newline='') as outstream:
        writer = csv.DictWriter(outstream,
                fieldnames=fieldnames)
        writer.writeheader()
        for key in dict_of_records.keys():
            print(key)
            writer.writerow(dict_of_records[key])


def main():
    new_keys = get_new_keys(args[1])
#   print(new_keys)
    csv1 = args[2]
    csv2 = args[3]
    new_csv = args[4]
    for file_name in (csv1, csv2, new_csv, ):
#       print(file_name)
        pass
    d1 = collect_dict(csv1, new_keys)
    d2 = collect_dict(csv2, new_keys)
    new_dict = dict()
    for key in d1.keys():
        new_dict[key] = d1[key]
    for key in d2.keys():
        new_dict[key] = d2[key]
    populate_csv_file(new_csv, new_keys, new_dict)


if __name__ == '__main__':
    main()
