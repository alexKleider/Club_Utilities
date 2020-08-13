#!/usr/bin/env python

# File: Tests/t.py

import unittest

import os
import sys

sys.path.insert(0, os.path.split(sys.path[0])[0])

import data
import rbc

info = data.gather_sponsors(rbc.Club.SPONSORS_SPoT)
for key in info.keys():
    print("{}: {}".format(key, info[key]))

