#!/usr/bin/env python

# File: parse_applicants.py

in_file = "Data/applicants.txt"

expired = []
status_adjustment = 4

with open(in_file, 'r') as f_obj:
    for line in f_obj:
        line = line.strip()
        if line:
            parts = [part.strip() for part in line.split("|")]
            length = len(parts)
            if length > 2:
                status = length - status_adjustment
                name = parts[0]
                names = name.split()
                if len(names) == 2:
                    first = names[0]
                    last = names[1]
                    last_first = "{}, {}".format(last, first)
                    if parts[-1]:
                        print("parts[-1]: '{}'".format(parts[-1]))
                    if parts[-1] == "Application expired.":
                        expired.append(last_first)
                    else:
                        print("{}: length is {}; status is {}"
                            .format(last_first, length, status))
if expired:
    print("\nExpired applications:")
    for entry in expired:
        print(entry)
