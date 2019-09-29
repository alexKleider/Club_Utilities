#!/usr/bin/env python

# File: parse_applicants.py
# Expect to merge into ck_integrity.py &/or
# possibly merge both into utils.py

in_file = "Data/applicants.txt"

import member

status_adjustment = 4   # Depends on strict adhearance to
                        # formatting of input file

def gather_applicant_data(in_file):
    """
    Reads the in_file and returns a dict with keys:
        "expired": list of applicants who've let applications expire.
        "applicants": a dict- lists of applicants keyed by status.
            (Client will want to sort keys for presentation.)
    """
    expired_applications = []
    applicants = {}
    with open(in_file, 'r') as f_obj:
        for line in f_obj:
            line = line.strip()
            if line:
                parts = [part.strip() for part in line.split("|")]
                length = len(parts)
                if length > 2:
                    index = length - status_adjustment
                    try:
                        status = member.STATI[:5][index]
                    except IndexError:
                        continue
                    name = parts[0]
                    names = name.split()
                    if len(names) == 2:
                        first = names[0]
                        last = names[1]
                        last_first = "{}, {}".format(last, first)
                        last_segment = parts[-1]
#                       print("last_segment is '{}'"
#                           .format(last_segment))
                        if last_segment == "Application expired.":
                            expired_applications.append(last_first)
                        else:
                            _ = applicants.setdefault(status,[])
                            applicants[status].append(
                                "{}".format(last_first))
    return {"expired": expired_applications,  # just a list
            "applicants": applicants,  # lists keyed by status:
                        # client will want to sort the keys.
     # i.e. keys = sorted([key for key in data["applicants"]])
            }

if __name__ == "__main__":
    ret = []
    data = gather_applicant_data(in_file)
    keys = sorted([key for key in data["applicants"]])
    for key in keys:
        ret.append("{}:".format(key))
        for value in data["applicants"][key]:
            ret.append("{}".format(value))
    if data["expired"]:
        ret.append("\nExpired applications:")
    for entry in data["expired"]:
        ret.append(entry)
    print("\n".join(ret))
