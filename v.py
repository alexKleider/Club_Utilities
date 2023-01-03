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
    .v.py by_category fname categories [out_file]
                # report volunteers for specific categories,
                # 'all' for all categories.
    .v.py by_name fname names [out_file] # report jobs for which 
                    # listed (in <names>) members have volunteered,
                    # 'all' if to include everyone.

Both 'categories' and 'names' parameters (if specified)
must be a comma separated (no spaces) listing.
"""

import os
import sys
import json

ROOT_DIR = os.path.expandvars('$CLUB')
DATA_DIR = "Data"
DEFAULT_DATA_FILE_NAME = "vfile.json"
DEFAULT_DATA_FILE = os.path.join(
        ROOT_DIR, DATA_DIR, DEFAULT_DATA_FILE_NAME)
SEPARATOR = '.'
special_header = "SKILLS_ABILITIES_INTERESTS"

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
        EventStocking = [],
        ),
    KITCHEN = dict(
        SetUp = [],
        CleanUp = [],
        Serving = [],
        KitchenStocking = [],
        ),
    INFRASTRUCTURE = dict(
        DockDeckMaintenance = [],
        Decorating = [],
        ClubHouseMaintenance = [],
        ),
    COMMITTEE_SERVICE = dict(
        Docks_Yards = [],
        Entertainment = [],
        Membership = [],
        ByLaws = [],
        ExecutiveCommittee = [],
        Finance = [],
        Website = [],
        BuildingGrounds = [],
        ClubRentals = [],
        ),
    SKILLS_ABILITIES_INTERESTS = dict(
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


def add(args):
    """
    Adds args[3] (a name) to categories in data (args[2].
    """
    name = args[3]
    print(f"Adding name {name} into data file {args[2]}")
    no_entries = True
    with open(args[2], 'r') as instr:
        data = json.load(instr)
    special_header = "SKILLS_ABILITIES_INTERESTS"
    for header in [header for header in data.keys()]:
        if header == special_header:
            response = input(
            f"Are there any {special_header}? ")
            if response and response[0] in 'yY':
                no_entries = False
                _ = data[header].setdefault(name, [])
                while response:
                    response = input("Entry: ")
                    if response:
                        data[header][name].append(response)
        else:
            keys = [key for key in data[header].keys()]
            for key in keys:
                res = input(f"Add {name} to {header}: {key}? (y/n) ") 
                if res and res[0] in 'yY':
                    no_entries = False
                    data[header][key].append(name)
    if no_entries:
        _ = data[special_header].setdefault(name, [])
        data[special_header][name].append('NO ENTRIES')
    response = input("Input complete; OK to store? (y/n) ")
    if response and response[0] in 'yY':
        with open(args[2], 'w') as outstr:
            json.dump(data, outstr)


def by_category(args):
    """
    Display data by category (all or only those specified.)
    """
    categories = args[3]
    if categories != 'all':
        categories = set(args[3].split(','))
    if len(args) > 4:
        outf = args[4]
    else:
        outf = None
    res = []
    addendum = None
    with open(args[2], 'r') as instr:
        data = json.load(instr)
    headers = [header for header in data.keys()]
    for header in headers:
        if header == special_header:
            if data[header]:
                addendum = [header]
                addendum.extend([f"    {key}: {value}" for
                    key, value in data[header].items()])
            continue
        entries = []
        for category in data[header].keys():
            if categories == 'all' or category in categories:
                if data[header][category]:
                    entries.append(
                    f"    {category}: {repr(data[header][category])}")
        if entries:
            res.append(header)
            res.extend(entries)
    if addendum:
        res.extend(addendum)
    text = '\n'.join(res)
    if outf:
        print(f"writing to {outf}")
        with open(outf, 'w') as outstream:
            outstream.write(text)
    else:
        print(text)


def by_name(args):
    """
    Display data by name (all or only those specified.)
    """
    names2consider = args[3]
    if names2consider != 'all':
        names2consider = set(args[3].split(','))
    if len(args) > 4:
        outf = args[4]
    else:
        outf = None
    with open(args[2], 'r') as instream:
        data = json.load(instream)
    res = {}
    addendum = None
    for header in [key for key in data.keys()]:
        if header == special_header:
            names = [name for name in data[header].keys()]
            if names:
                _ = res.setdefault(header, {})
                for name in names:
                    _ = res[header].setdefault(name, [])
                    for item in data[header][name]:
                        res[header][name].append(item)
            continue
        for category in [key for key in data[header].keys()]:
            for name in data[header][category]:
                if names2consider == 'all' or name in names2consider:
                    _ = res.setdefault(name, [])
                    res[name].append(f"{header}:{category}")
#               else:
#                   _ = input(f"{name} not considered")
    with open('2check.json', 'w') as outstream:
        json.dump(res, outstream)
    # now need to convert data into text:
    ret = []
    for key in res.keys():
        ret.append(key)
        for val in res[key]:
            if key == special_header:
                # val is dict keyed by names (id)
                ids = res[special_header].keys()
                for id in ids:
                    if names == 'all' or id in names2consider:
#                       _ = input(
#                       f"id: {id} names2consider: {names2consider}")
                        listing = ', '.join(res[special_header][id])
#                       _ = input(f"appending '   {id}: {listing}'")
                        ret.append(f"    {id}: {listing}")
            else:
                ret.append(f"    {val}")
    text = '\n'.join(ret)
    if outf:
        print(f"writing to {outf}")
        with open(outf, 'w') as outstream:
            outstream.write(text)
    else:
        print(text)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd.startswith('?'):
        print(__doc__)
        sys.exit()
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



