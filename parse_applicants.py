#!/usr/bin/env python

# File: parse_applicants.py
# Expect to merge into ck_integrity.py &/or
# possibly merge both into utils.py

APPLICANT_SPoT = "Data/applicants.txt"
# SPoT == Single Point of Truth (DRY by another name)
# DRY == Do not Repeat Yourself
# This is the file used to keep track of applicants' data
# that is not reflected in the club's master list of members
# (which does include applicants.  ck_integrity compares
# these two soruces of information for consistency.

import member

status_adjustment = 4   # Depends on strict adhearance to
                        # formatting of input file

def gather_applicant_data(in_file):
    """
    Reads the in_file (assumed to be the APPLICANT_SPoT)
    and returns a dict with keys:
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


def present_expired(list_of_expired_applications, raw=False):
    """
    It's expected that the parameter will be the the following:
    gather_applicant_data(APPLICANT_SPoT)["expired"]
    which is just a list of last_first names.
    """
    if raw:
        ret = []
    else:
        ret = ["Applicants whos applications have expired:",
               "=========================================="]
    for name in sorted(list_of_expired_applications):
        ret.append(name)
    return "\n".join(ret)

def present_applicants(applicants_keyed_by_status, raw=False):
    """
    It's expected that the parameter will be the the following:
    gather_applicant_data(APPLICANT_SPoT)["applicants"]
    which is a dict keyed by status /w each value => list
    of last_first names.
    """
    if raw:
        ret = []
    else:
        ret = ["Applicants by status:",
               "====================="]
    keys = sorted([key for key in applicants_keyed_by_status])
    for key in keys:
        if not raw:
            ret.append("")
        ret.append("{}:".format(key))
        for value in sorted(data["applicants"][key]):
            ret.append("{}".format(value))
    return "\n".join(ret)


if __name__ == "__main__":
    ret = []
    data = gather_applicant_data(APPLICANT_SPoT)
    print(present_applicants(data["applicants"]))
    print("\n\n")
    print(present_expired(data["expired"]))

