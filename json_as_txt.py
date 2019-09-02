#!/usr/bin/env python3

# File: json_as_txt.py

"""
json files are hard for humans to read.
This tries to solve this problem.
Difficulty is how to account for every possible version of a json
file.  So far only two forms work.
This utility may be retired in the future in favour of a custom script
for each category of json file used.
"""

import json
import sys

if len(sys.argv) < 2 :
    print("No argument(s) provided!")
    sys.exit()

for f in sys.argv[1:]:
    collector = []
    components = f.split(".")
    if ((len(components) != 2)
    or (components[1] != 'json')):
        print("Argument(s) malformed- must be ____.json")
        sys.exit()
    out_file = ".".join((components[0], 'txt'))
    with open(f, 'r') as f_obj:
        data = json.load(f_obj)
    keys = [key for key in data.keys()]
    _keys = keys.sort()
    for key in keys:
        if isinstance(data[key], str):
            value = data[key]
            collector.append("{:<27} {}"
                .format(key, value))
        else:
            collector.append(key)
            for s in data[key]:
                collector.append("\t{};".format(s))
    with open(out_file, 'w') as f_obj:
        f_obj.write("\n".join(collector))
