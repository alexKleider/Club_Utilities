#!/usr/bin/env python3

# File: readangies.py

import sys
import csv

fields2show = (
"First","Last","Deposit","Check Amount","Membership",
"Dock Fees","Mooring Fee","App  Fee","Kayak Storage",
"Derby Donation","Other","Notes","TOTAL ","22770")
if len(sys.argv) > 1:
    infile = sys.argv[1]
else:
    infile = "fromAngie.csv"

with open(infile, 'r', newline='') as instream:
    reader = csv.DictReader(instream)
    collector = []
    for rec in reader:
        keys = [key for key in rec.keys()]
        line = []
        for key in keys:
            if rec[key] and rec[key]!='None':
                line.append(f"{key}: {rec[key]}".strip())
        if line:
            collector.append(', '.join(line))
print("\n".join(collector))



