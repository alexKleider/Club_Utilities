#!/usr/bin/env python3

# File: received_totals.py

import sys

input_file = sys.argv[1]
total = 0
subtotal = 0

with open(input_file, "r") as file_obj:
    for line in file_obj:
        line= line.rstrip()
        if line[24:27] == "---":
            print("SubTotal                --- ${}"
                .format(subtotal))
            subtotal = 0
        try:
            amount = int(line[24:27])
        except (ValueError, IndexError):
#           print("Invalid: '{}'".format(line))
            continue
#       print("Adding ${}.".format(amount))
        total += amount
        subtotal += amount
print("Grand Total to Date:    --- ---- ${}"
    .format(total))
