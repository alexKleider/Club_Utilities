#!/usr/bin/env python3

# File: find_calls.py

"""
Get a listing of all function calls in each module.
Top level keys: name of function being called
next level keys: module where the call is being made
final value: list of line numbers where the call appears.
"""

import re
import sys
import pprint

EXPR= r"def (\w+)\("
PAT = re.compile(EXPR)

# first get our list of source code files:
source_files = ("content",
                "data",
                "helpers",
                "member",
                "rbc",
                "utils",
                )


def find_defs(fname):
    ret = []
    with open("{}.py".format(fname), 'r') as fobj:
        for line in fobj:
            m = PAT.search(line)
            if m:
                if m.group(1).endswith('_'):
                    pass
                else:
                    ret.append(m.group(1))
    return ret


def yield_function_names(names_by_file_name):
    for file_name in names_by_file_name.keys():
        for function_name in names_by_file_name[file_name]:
            yield function_name


# Collect names of all the functions/methods indexed by file name:
names_by_file_name = {}
for f in source_files:
    names_by_file_name[f] = find_defs(f)

# Look for calls to these functions/methods in each of the files:
res = {}
for f in source_files:
    res[f] = {}

'''
    d[word][f] = []
    with open(f, 'r') as fobj:
        line_number = 0
        for line in fobj:
            line_number += 1
            for word in words:
                if line.count(word):
                    d[word][f].append(line_number)
'''

pprint.pprint(f_defs)
