#!/usr/bin/env python3

# File: v.py

"""
Applicant Volunteerism
======================
Unless using the '?' option, the user must
provide a minimum of 2 command line parameters as follows:
    1. a command
    2. a file name (which can be 'default'.)
Some commands may allow or demand one (or possibly several)
more parameter(s) specific to the command in question.

Usage:
    .v.py (? | (cmd fname|default [options...]))

    .v.py ?   # print this docstring
    .v.py init fname  # initialize an empty data base
    .v.py add fname first_last  # add data pertaining to ..
    .v.py by_category fname [categories]  # report volunteers for
                # specific categories, for all if not specified.
    .v.py by_name fname [names]  # report jobs for which 
                    # listed members have volunteered,
                    # all if names is not specified.

Both 'categories' and 'names' parameters (if specified)
must be a comma separated (no spaces) listing.
"""

import sys
import json

DEFAULT_DATA_FILE = "vfile.json"
SEPARATOR = '.'

empty_data = dict(
    EVENTS = dict(
        StPatricksDay = [],
        SummerBBQ = [],
        FishingDerby = [],
        PancakeBreakfast = [],
        Oktoberfest = [],
        ChristmasParty = [],
        OtherDinnerEvents = [],
        Bartending = [],
        Stocking = [],
        ),
    KITCHEN = dict(
        SetUp = [],
        CleanUp = [],
        Serving = [],
        Stocking = [],
        ),
    INFRASTRUCTURE = dict(
        DockDeckMaintenance = [],
        Decorating = [],
        ClubHouseMaintenance = [],
        ),
    SKILLS_ABILITIES_INTERESTS = dict(
        ),
    COMMITTEE_SERVICE = dict(
        Docks_Yards = [],
        Entertainment = [],
        Membership = [],
        ByLaws = [],
        ExecutiveCommittee = [],
        Finance = [],
        Website = [],
        Maintenance = [],
        BuildingGrounds = [],
        ClubRentals = [],
        ),
    )

special_data = {}


def confirm_file(fname):
    if fname == 'default':
        fname = DEFAULT_DATA_FILE
    if fname == DEFAULT_DATA_FILE:
        print(f"Dealing with data file called {fname}")
        return fname
    else:
        response = input(
            f"Use file '{fname}' (rather than '{DEFAULT_DATA_FILE}'? (y/n): ")
        if response and response[0] in ('yY'):
            return fname


def traverse_data(args, func, params, res):
    """
    Apply the <function> using provided <params>
    to each element in data (derived from args.)
    Retuns the (possibly modified) data retrieved 
    from file defined by <args[2]>.
    """
    print(f"Traversing data...")
    header = ''
    with open(args[2], 'r') as instr:
        data = json.load(instr)
    keys = [key for key in data.keys()]
    for key in keys:
#           print(f"Under header '{key}':")
            header = key
            if isinstance(data[key], dict):
                if isinstance(res, dict):
                    pass
                else:
                    if isinstance(res, list):
                        res.append(header)
                func(data[key], *params, header=header)
            else:
                header = ''
#               print("Independent items:")
                func(data, *params, header=header)
    return data  # only used by add command
            # other commands store data in one of the <params>


def wrapper(args):
    """
    <args> is expected to be sys.argsv. args[1]==cmd.
    Replaces the command name with the command function
    which is then executed.
    """
    f = confirm_file(args[2])
    if f:
        args[2] = f
        args[1](args)
    else:
        print(f"Aborting (Not authorized to use file {args[2]})")


def init_json_file(args):
    """
    Initialize an empty data base.
    """
    print(f"Writing to {args[2]}")
    with open(args[2], 'w') as outstr:
        json.dump(empty_data, outstr)


def dump_data(args, data):
    """
    Dump data (presumably after it's been read from the data
    base and then modified) back into the data base.
    """
    print(f"Writing to {args[2]}")
    with open(args[2], 'w') as outstr:
        json.dump(data, outstr)


def populate_values(data, name, header=None):
    """
    Assumes <data> is a dict of lists.
    For each key within <data>, provides option to
    add <name> to its list value.
    """
    keys = [key for key in data.keys()]
    for key in keys:
        res = input(f"Add {name} to {key}? (y/n) ") 
        if res and res[0] in 'yY':
            data[key].append(name)


def add(args):
    """
    Adds args[3] (a name) to categories in data (args[2].
    """
    print(f"Adding name {args[3]} into data file {args[2]}")
    new_data = traverse_data(args,
                        populate_values,
                        (args[3],), res=None)
    with open(args[2], 'w') as outstr:
        json.dump(new_data, outstr)


def populate_categories(data, categories, res, header=None):
    """
    """
    keys = [key for key in data.keys()]
    for key in keys:
        if categories == 'all' or key in categories:
            if data[key]:
                res.append(f"\t{key}: {repr(data[key])}")


def by_category(args):
    """
    Display data by category (all or only those specified.)
    """
    print(f"Reading data from {args[2]}...")
    if len(args) > 3:
        categories = set(args[3].split(','))
    else: categories = 'all'
    res = []
    traverse_data(args, populate_categories,
                        (categories, res), res)
    print('\n'.join(res))


def by_name(args):
    """
    Display data by name (all or only those specified.)
    """
    print(f"Readin data from {args[2]}")
    with open(args[2], 'r') as instr:
        data = json.load(instr)
    if len(args) > 3:
        names = set(args[3].split(','))
    else: names = 'all'
    res = {}
    for header in [key for key in data.keys()]:
        for category in [key for key in data[header].keys()]:
            for name in data[header][category]:
                if names == 'all' or name in names:
                    _ = res.setdefault(name, [])
                    res[name].append(f"{header}:{category}")
    ret = []
    for key in res.keys():
        ret.append(key)
        for val in res[key]:
            ret.append(f"\t{val}")
    print('\n'.join(ret))


if __name__ == "__main__":
    largs = len(sys.argv)
    cmd = sys.argv[1]
    if cmd.startswith('?'):
        print(__doc__)
    elif cmd == 'init':
        sys.argv[1] = init_json_file
        wrapper(sys.argv)
    elif cmd == 'add':
        sys.argv[1] = add
        wrapper(sys.argv)
    elif cmd == 'by_category':
        sys.argv[1] = by_category
        wrapper(sys.argv)
    elif cmd == 'by_name':
        sys.argv[1] = by_name
        wrapper(sys.argv)
    else:
        print("No action taken.")



