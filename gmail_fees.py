#!/usr/bin/env python3

# File: gmail_fees.py

"""
Gets gmail contact data (so for only those with email!)
Dumps a json file:
    a list of dicts, each keyed by member name
    with values: an ordered list of what fees they pay.
Now challenge is to create a similar result based on 
membership data, subtract from it those without email
and see if the two correspond.
"""

import json
import helpers
import data
from rbc import Club


def get_fee_paying_contacts(club):
    """
    Assumes club attribute <groups_by_name> has already been
    assigned (by data.gather_contacts_data.)
    Creates a list of dicts keyed by contact name
    and each value is a list of fee categories.
    This list of dicts is returned after being assigned
    to the club attribute <fee_paying_contacts>.
    """
    collector = {}
    fee_groups = ["DockUsers", "Kayak", "Moorings"]
    fee_set = set(fee_groups)
    names = sorted(club.groups_by_name.keys())
    for name in names:
        intersect = club.groups_by_name[name].intersection(fee_set)
        if intersect:
            renamed_group = []
            for category in intersect:
                if category == 'DockUsers':
                    renamed_group.append('dock')
                if category == 'Kayak':
                    renamed_group.append('kayak')
                if category == 'Moorings':
                    renamed_group.append('mooring')
            if renamed_group:
                collector[name] = renamed_group
    club.fee_paying_contacts = collector
    return collector


if __name__ == "__main__":
    outfile = "gmail_fee_info.json"
    club = Club()
    club.quiet = True
    data.gather_contacts_data(club)
    collector = get_fee_paying_contacts(club)
    with open(outfile, 'w') as stream:
        json.dump(collector, stream)
    res = []
    for name in collector.keys():
        listing = ', '.join(collector[name])
        res.append(f'{name}: {listing}')
    print('\n'.join(helpers.tabulate(res, separator='   ',
        max_columns=2)))
