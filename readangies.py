#!/usr/bin/env python3

# File: readangies.py

import csv

with open("angies.csv", 'r', newline='') as instream:
    reader = csv.DictReader(instream)
    collector = []
    for rec in reader:
        keys = [key for key in rec.keys()]
        for key in keys:
            line = []
            if rec[key] and rec[key]!='None':
                entry = f"{key}: {rec[key]}".strip()
                if entry:
                    line.append(entry)
            line = [entry for entry in line if entry]
            collector.append(', '.join(line))
            collector = [line for line in collector if line]
    print("\n".join(collector))



