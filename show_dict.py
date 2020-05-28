#!/usr/bin/env python3

# File: show_dict.py

"""
A 'work in progress' the goal of which is to write a general
function that will provide a human readable representation of
a json file.
"""

def show_dict(_dict):
    for key in _dict:
        print("\n" + key)
        print("=" * len(key))
        for val in _dict[key]:
            if type(val) == dict:
                print("a dict follows:")
                for k in val.keys():
                    print('\n' + k)
                    print('-' * len(k))
                    for item in val[k]:
                        print(item)
            else:
                print(val)
