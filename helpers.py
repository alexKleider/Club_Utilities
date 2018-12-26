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

def expand(address, nlines):
    """
    Takes an address which can be a list of strings/lines
    or all one string (with line feeds separating lines,)
    and returns the same type (either string or list) but
    containing nlines.
    Fails if address already has more than nlines.
    """
    isstring = False
    if isinstance(address, str):
        isstring = True
        address = address.split("\n")
    if len(address) > nlines:
        print("Error: too many lines in an address!")
        assert False
    while nlines > len(address):
        if nlines - len(address) >= 2:
            address = [''] + address + ['']
        else:
            address.append('')
    if isstring:
        return '\n'.join(address)
    else:
        return address


if __name__ == "__main__":
    print("The month is '{}'.".format(month))
    print("'helpers.get_datestamp() returns '{}'."
        .format(date))

    addr1 = "Alex Kleider\nPO Box 277\nBolinas, CA 94924"
    addr2 = """Alex Kleider
PO Box 277
Bolians, CA 94924"""
    addr3 = ["Alex Kleider", "PO Box 277", "Bolinas, CA 94924"]

    for addr in (addr1, addr2, addr3):
        print()
        print(expand(addr, 7))

