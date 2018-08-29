#!/usr/bin/env python3

# File: helpers.py

"""
Some helper functions needed by both formats.content and by utils
"""


POSTAL_INDENT = 8
INDENTATION = " " * POSTAL_INDENT

def get_datestamp():
    """
    Returns a string depicting the current date (for postal letters.)
    """
    import datetime
    format = "%b %d, %Y"
    today = datetime.datetime.today()
    s = today.strftime(format)
    d = datetime.datetime.strptime(s, format)
    date = d.strftime(format)
    print("Setting the date to '{}'.".format(date))
    return date

def indent(text, indentation=INDENTATION):
    """
    Helper function providing indentation for postal content.
    """
    split_text = text.split("\n")
    indented = [indentation + line for line in split_text]
    return "\n".join(indented)
