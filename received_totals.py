#!/usr/bin/env python3

# File: received_totals.py

import sys

input_file = sys.argv[1]
total = 0
subtotal = 0

with open(input_file, "r") as file_obj:
    for line in file_obj:
        line= line.rstrip()
        if "LAST" in line:
            subtotal = 0
        try:
            amount = int(line[24:27])
        except (ValueError, IndexError):
            print("Invalid: '{}'".format(line))
            continue
        total += amount
        subtotal += amount
print("LAST amount collected:  ${}".format(subtotal))
print("Total amount collected: ${}".format(total))

