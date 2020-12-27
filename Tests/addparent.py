#!/usr/bin/env python

# File: Tests/addparent.py

"""
To be able to import modules for testing it is necessary to have
the project directory in sys.path. One way to achieve this is
to run <add2path> provided here.
Unfortunately, this doesn't work when using pytest.
If using pytest do the following at the command line before hand:
$ export PYTHONPATH=/home/alex/Git/Club/Utils
This always works pretty much obviating the need for this script.
"""

import os
import sys

def add2path():
    sys.path.insert(0, os.path.split(sys.path[0])[0])
