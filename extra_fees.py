#!/usr/bin/env python3

# File: extra_fees.py

"""
Accepts a text file in the format of Data/extra_fees.txt
and provides functionality to create 'dict's keyed by
category or by name and to send data to json files.

Usage:
  ./extra_fees.py [ --help | --version ]
  ./extra_fees.py [-i <infile> -c <by_category> -n <by_name>]

Options:
  -h --help  Print this docstring.
  --version  Print version.
  -i <infile>  Input file name. [default: Data/extra_fees.txt]
  -c <by_category>  By category json. This essentially presents the
          same information as the input file but in json format to
          the file named <by_category>.  [default: by_category.json]
  -n <by_name>  By name json. Keyed by member name (last, first) sent
          to the file named <by_name  [default: by_name.json]

Input file has the following format:

Members paying for a Mooring:
Michael Chadwick:  114
.....

Members paying for Dock privileges:
Rick Bettini:  75
Jeff McPhail:  75
.....

Members paying for Kayak storage:
Doug Barth:  70
Kathryn Cirincione-Coles:  70
Jeff McPhail:  70
.....
"""

import json
from docopt import docopt

args = docopt(__doc__, version="0.0")
by_name = {}
by_category = dict(  # json version of input file
    Kayak= [],
    Dock= [],
    Mooring= [],
    )
categories = [key for key in by_category.keys()]
# print(args)
# print(categories)

with open(args["-i"], 'r') as infile:
#   print("Opened {}."
#       .format(args["-i"]))
    line_number = 0
    category = ""
    for line in infile:
        line = line.strip()
        line_number += 1
        if not line:
            continue
        category_change = False
        if line[-1] == ':':  # category change
#           print("Should get a category change...")
            words = line[:-1].split()
            for word in words:
                if word in categories:
                    category = word
                    category_change = True
#                   print("Switching category to '{}'."
#                       .format(category))
                    continue
        else:  # Expect a name with fee for current category...
            parts = line.split(':')
#           print(parts)
            fee = int(parts[1])
            names = parts[0].split()
            first_name = names[0]
            last_name = names[1]
            name_key = "{}, {}".format(last_name, first_name)
            _ = by_name.setdefault(name_key,"")
            by_name[name_key] = by_name[name_key] + ("{} ${}; "
                    .format(category, fee))
            name = name_key  + ":"
            by_category[category].append("{:<27} {}".format(name, fee))

def ret_by_name():
    return by_name

def ret_by_category():
    return by_category

def create_by_name_json_file():
    with open(args["-n"], "w") as json_file_obj:
        json.dump(by_name, json_file_obj)
    print("by_category dumped to {}"
        .format(args["-n"]))

def create_by_category_json_file():
    with open(args["-c"], "w") as json_file_obj:
        json.dump(by_category, json_file_obj)
    print("by_category dumped to {}"
        .format(args["-c"]))

if __name__ == "__main__":
    create_by_name_json_file()
    create_by_category_json_file()
