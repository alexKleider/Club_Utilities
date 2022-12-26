#!/usr/bin/env python3

# File: v.py

"""
Keep track of for what applicants have volunteered.
Must provide a minimum of 2 command line parameters as follows:
    1. a command
    2. a file name which can be 'default'.
Some commands allow or demand a third parameter specific
to the command.

Usage:
    .v.py cmd fname|default [options...]

    .v.py init fname
    .v.py add fname first_last
    .v.py by_category fname [category...]
    .v.py by_name fname [name...
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


def init_json_file(args):
    print(f"Writing to {args[2]}")
    with open(args[2], 'w') as outstr:
        json.dump(empty_data, outstr)


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


def populate_names(data, names, res, header=None):
    """
    """
    pass


def populate_categories(data, categories, res, header=None):
    """
    """
    keys = [key for key in data.keys()]
    for key in keys:
        if data[key]:
            res.append(f"\t{key}: {repr(data[key])}")


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
                    res.append(header)
                func(data[key], *params, header=header)
            else:
                header = ''
#               print("Independent items:")
                func(data, *params, header=header)
    return data  # only used by add command
            # other commands store data in one of the <params>

def add(args):
    """
    Adds args[3] (a name) to categories in data (args[2].
    """
    print(f"Adding name {args[3]} into data file {args[2]}")
    new_data = traverse_data(args,
                        populate_values,
                        (args[3],))
    with open(args[2], 'w') as outstr:
        json.dump(new_data, outstr)


def by_category(args):
    """
    Display data by category (all or only those specified.)
    """
    print(f"Reading data from {args[2]}...")
    if len(args) == 4:  # look at specific categories
        categories = args[3].split(SEPARATOR)  # now a tuple
    else:  # show all <categories> (which is an empty tuple.)
        categories = ()
    res = []
    traverse_data(args, populate_categories,
                        (categories, res), res)
    print('\n'.join(res))


def by_name(args):
    """
    Display data by name (all or only those specified.)
    """
    print(f"Readin data from {args[2]}")
    res = {}
    traverse_data(args, populate_names, (args[3], res))
    print(res)


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


if __name__ == "__main__":
    largs = len(sys.argv)
    cmd = sys.argv[1]
    if cmd == 'init':
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



