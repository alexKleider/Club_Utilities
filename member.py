#!/usr/bin/env python3

# File: member.py

"""
Many methods of Membership class are essentially
independant of Membership but pertain to each record.
Hence makes sense to separate them out.
"""

STATUS_SEPARATOR = ':'
WAIVED = "w"
status_key_values = {
    "a0": "Application received.",
    "a1": "Attended one meeting.",
    "a2": "Attended two meetings.",
    "a3": "Attended three (or more) meetings.",
    "ai": "Inducted, membership fee pending.",
    "m": "Member in good standing.",
    WAIVED: "Fees being waived.",
    "be": "Email on record doesn't work.",
    }
STATI = sorted([key for key in status_key_values.keys()])
NON_MEMBER_STATI = STATI[:5]
APPLICANT_SET = set(STATI[:5])

def is_applicant(self, record):
    stati = record['status'].split(STATUS_SEPARATOR)
    for status in stati:
        if status in APPLICANT_SET: 
            return True
    return False

def is_member(record):
    """
    Tries to determine if record is that of a member (based on
    status field.)
    If there is a problem, will either append notice to
    self.errors if it exists, or cause program to fail.
    """
    stati = record['status'].split(STATUS_SEPARATOR)
    for status in NON_MEMBER_STATI:
        if status in stati:
            return False
    if (
        stati == [''] or  # blank for most members
        "m" in stati or  # member
        stati == ['be'] or  # bad email
        #    Notice the '==', not '"be" in ..'
        "w" in stati   # fees waved
        ):
        return True
    error = ("Problem in 'is_member' with {}."
        .format("{last}, {first}".format(**record)))
    print(error)


#   def is_member(self, record):
#       """
#       Anyone who is not an applicant.
#       """
#       return not self.is_applicant(record)

def is_fee_paying_member(self, record):
    """
    """
    if WAIVED in record['status'].split(STATUS_SEPARATOR):
        return False
    if self.is_member(record):
        return True

def add2stati_by_status(self, record):
    """
    Prerequisite: self.stati_dict
    Populates self.stati_dict (which must be set up by
    client) with lists of member names (last, first) keyed
    by status.
    """
    stati = record["status"].split(STATUS_SEPARATOR)
    for status in stati:
        _ = self.stati_dict.setdefault(status, [])
        self.stati_dict[status].append(
                    "{last}, {first}".format(**record))
