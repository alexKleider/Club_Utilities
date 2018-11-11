#!/usr/bin/env python3

# File: print_letters.py

"""
Prints all the files found in the directory named by the
first (and only) parameter.

Usage:
    print_letters.py target_dir

"""

import os
import sys
import subprocess

target_dir = sys.argv[1]
print(target_dir)

for letter_name in os.listdir(target_dir):
    path_name = os.path.join(target_dir, letter_name)
    completed = subprocess.run(["lpr", path_name])
    print("{}: {}".format(path_name, completed))



