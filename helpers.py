#!/usr/bin/env python3

# File: helpers.py

"""
Some helper functions needed by both formats.content and by utils
"""

import datetime

POSTAL_INDENT = 8
INDENTATION = " " * POSTAL_INDENT

format = "%b %d, %Y"
today = datetime.datetime.today()
month = today.month
s = today.strftime(format)
d = datetime.datetime.strptime(s, format)
date = d.strftime(format)
print("Setting the date to '{}'.".format(date))

def get_datestamp():
    """
    Returns a string depicting the current date (for postal letters.)
    """
    return date

def indent(text, indentation=INDENTATION):
    """
    Helper function providing indentation for postal content.
    """
    split_text = text.split("\n")
    indented = [indentation + line for line in split_text]
    return "\n".join(indented)

if __name__ == "__main__":
    print("The month is '{}'.".format(month))
    print("'helpers.get_datestamp() returns '{}'."
        .format(date))
