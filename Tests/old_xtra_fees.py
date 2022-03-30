#!/usr/bin/env python3

# File: Tests/old_xtra_fees.py

import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])
from rbc import Club
import helpers
from data import get_dict, gather_extra_fees_data, extra_fees_by_name


print("Running 'xtra_fees.py'.")
club = Club()
extra_fees = gather_extra_fees_data(Club.EXTRA_FEES_SPoTs)
by_name = extra_fees_by_name(extra_fees)
for key in extra_fees.keys():
    print('\n' + key.capitalize() + '\n' + '='*len(key))
    for k in sorted(extra_fees[key].keys()):
        print("{}: {}".format(k, extra_fees[key][k]))

print('\n=========\n')
for name in sorted(by_name.keys()):
    print("{}: {}".format(name, by_name[name]))

