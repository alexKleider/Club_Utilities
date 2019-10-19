#!/usr/bin/env python3

# File: extra_fees.py

"""
Input must be a text file in the format of Data/extra_fees.txt.
Functionality provided 'dict's keyed by category or by name.

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
Michael Cook:  114
.....

Members paying for Dock privileges:
Rick Butler:  75
Jeff McPhearson:  75
.....

Members paying for Kayak storage:
Doug Birch:  70
Kathryn Cook:  70
Jeff McPhearson:  70
.....
"""

import json
from docopt import docopt

NAME_KEY = "by_name"
CATEGORY_KEY = "by_category"

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


def gather_extra_fees_data(in_file):
    """
    Reads the in_file and returns a dict with keys:
        "by_category": each a list of (last_first, amount) tuples.
        "by_name": each a list of (category, amount) tuples.
    """
    by_name = {}
    by_category = dict(  # json version of input file
        Kayak= [],
        Dock= [],
        Mooring= [],
        )
    categories = [key for key in by_category.keys()]

    with open(in_file, 'r') as f_obj:
    #   print("Opened {}."
    #       .format(f_obj.name))
        line_number = 0
        category = ""
        for line in f_obj:
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
                _ = by_name.setdefault(name_key, [])
#               print("setdefault returns '{}' for '{}'"
#                       .format(_, name_key))
                by_name[name_key].append((category, fee))
#               print("Appending " + category + " " + str(fee) +
#                       " to " + name_key)
#               print(by_name[name_key])
                by_category[category].append((name_key, fee))
#   for key in by_name:
#       print(by_name[key])
    return {"by_name": by_name,
                # /ea value:= list of (category, amount) tuples
           "by_category": by_category,
                # /ea value:= list of (name, amount) tuples
            }


def present_by_name(json_version, raw=None):
    """
    Param would typically be the returned value of
    gather_extra_fees_data(infile)
    or its NAME_KEY value.
    Returns a text listing with header.
    """
    if NAME_KEY in json_version:
        jv = json_version[NAME_KEY]
    else:
        jv = json_version
    ret = []
    if not raw:
        ret.append("Extra fees by member:")
        ret.append("=====================")
    for key in jv:
        entry = key + ':'
        for value in jv[key]:
            entry = entry + " {} {}".format(value[0], value[1]) 
        ret.append(entry)
    return '\n'.join(ret)


def present_by_category(json_version, raw=None):
    """
    Param would typically be the returned value of
    gather_extra_fees_data(infile)
    or its CATEGORY_KEY value.
    Returns a text listing with header.
    """
    if CATEGORY_KEY in json_version:
        jv = json_version[CATEGORY_KEY]
    else:
        jv = json_version
    keys = sorted([key for key in jv])
    ret = []
    if not raw:
        ret.append("Extra fees by category:")
        ret.append("=======================")
    pass

 

def create_by_name_json_file(in_file):
    with open(args["-n"], "w") as json_file_obj:
        print('Dumping JSON to "{}".'.format(json_file_obj.name))
        json.dump(ret_by_name(in_file), json_file_obj)


def create_by_category_json_file(in_file):
    with open(args["-c"], "w") as json_file_obj:
        print('Dumping JSON to "{}".'.format(json_file_obj.name))
        json.dump(ret_by_category(in_file), json_file_obj)


if __name__ == "__main__":
    print(present_by_name(
        gather_extra_fees_data(args["-i"])[NAME_KEY]))
