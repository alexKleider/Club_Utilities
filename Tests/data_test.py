#!/usr/bin/env python

# File: Tests/data_test.py

# Must first add the parent directory of the
# currently running script to the system path:
import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])
# print(sys.path)
# ... or alternatively set PYTHONPATH to project directory:
# export PYTHONPATH=/home/alex/Git/Club/Utils

import data
import rbc

def test_gather_sponsors():
    info = data.gather_sponsors(rbc.Club.SPONSORS_SPoT)
    collected = {}
    with open(rbc.Club.SPONSORS_SPoT, 'r') as f_obj:
        for line in f_obj:
            line = line.strip()
            if line:
                components = line.split(':')
                sponsored = components[0]
                first, last = sponsored.strip().split()
                sponsors = components[1].strip()
                collected["{}, {}".format(last, first)] = sponsors
    assert info == collected


