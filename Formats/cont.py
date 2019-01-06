#!/usr/bin/env  python3
# File: cont.py

"""
An experiment to see how imports can work in packages.
The import utils works only if this module is imported by
a module that can be found within PYTHONPATH.
In this experiment, it is ../run_cont.py
If this module is run directly it fails at the import utils line.
"""

import sys

print(sys.path)

import utils
#from ..Py import utils
print("Fomrats.cont imported utils OK")

