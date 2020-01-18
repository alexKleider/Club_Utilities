#!/usr/bin/env python3

# File: helpers.py

"""
Some helper functions needed by both formats.content and by utils
"""

import datetime

format = "%b %d, %Y"
today = datetime.datetime.today()
month = today.month
this_year = today.year
s = today.strftime(format)
d = datetime.datetime.strptime(s, format)
date = d.strftime(format)

# print("Setting the date to '{}'.".format(date))

def this_club_year():
    if month > 6:
        return ("{}-{}".format(this_year, this_year + 1))
    else:
        return  ("{}-{}".format(this_year - 1, this_year))

def last_club_year():
    if month > 6:
        return ("{}-{}".format(this_year -1, this_year))
    else:
        return  ("{}-{}".format(this_year - 2, this_year - 1))

def next_club_year():
    if month > 6:
        return ("{}-{}".format(this_year + 1, this_year + 2))
    else:
        return  ("{}-{}".format(this_year, this_year + 1))

def get_datestamp():
    """
    Returns a string depicting the current date (for postal letters.)
    """
    return date


def indent(text, n_spaces):
    """
    Helper function providing indentation for postal content.
    Can deal with either a list of strings ('lines')
    or one string ('lines' terminated by linefeeds.)
    In either case, returns a string.
    """
#   print("Entering function 'indent'.")
    indentation = ' ' * n_spaces
    if isinstance(text, str):
        return (indentation + text.replace(
                            '\n', '\n' + indentation))
    elif isinstance(text, list):
        print("Encountering a list...")
        return '\n'.join([indentation + line for line in text])
    else:
        print("Should NOT get here!")
        assert(False)


def expand(text, nlines):
    """
    A helper function to expand addresses to requisite
    number of lines:
    Takes text which can be a list of strings/lines
    or all one string (with line feeds separating lines,)
    and returns the same type (either string or list) but
    containing nlines.
    Fails if address already has more than nlines.
    """
    isstring = False
    if isinstance(text, str):
        isstring = True
        text = text.split("\n")
    if len(text) > nlines:
        print("Error: too many lines in an address!")
        assert False
    while nlines > len(text):
        if nlines - len(text) >= 2:
            text = [''] + text + ['']
        else:
            text.append('')
    if isstring:
        return '\n'.join(text)
    else:
        return text


def show_dict(d, underline_char=None, extra_line=True):
    """
    Returns a list of strings representing a human readable version
    of a dictionary. If an underline_char is povided, each key is
    an underlined header with corresponding values listed beneath;
    if not- each key is followed by its values all on one line.
    Keys and values are ordered/sorted.
    """
    ret = []
    for key in sorted([key for key in d.keys()]):
        if underline_char:
            ret.append('')
            ret.append(key)
            ret.append(underline_char * len(key))
            for val in sorted([val for val in d[key]]):
                ret.append(val)
        else:
            line = ", ".join(sorted([val for val in d[key]]))
            ret.append("{}: {}".format(key, line))
    return ret


def create_json_file(json_data, json_file, verbose=True):
    with open(json_file, "w") as json_file_obj:
        if verbose:
            print('Dumping JSON to "{}".'
                .format(json_file_obj.name))
        json.dump(json_data, json_file_obj)


if __name__ == "__main__":
    print("The month is '{}'.".format(month))
    print("'helpers.get_datestamp() returns '{}'."
        .format(date))

    print("'this_club_year()' returns '{}'."
        .format(this_club_year()))

    addresses = ["Alex Kleider\nPO Box 277\nBolinas, CA 94924",
           """Alex Kleider
PO Box 277
Bolinas, CA 94924""",
    ["Alex Kleider", "PO Box 277", "Bolinas, CA 94924"]]

    expanded = [expand(addr, 7) for addr in addresses]
    indented = [indent(addr, 4) for addr in addresses]

    for addr in expanded:
        print("--")
        print(addr)
    print("--")
    debugging_code = """
    print("--")
    for addr in indented:
        print("--")
        print(addr)
        print(repr(addr))
    print("--")
    for n in range(len(indented)-1):
        for i in range(len(indented[n])):
            if indented[n][i] != indented[n+1][i]:
                print("{} == {}".format(indented[n][i], indented[n+1][i]))
            else:
                print("{} == {}".format(indented[n][i], indented[n+1][i]))
        if len(indented[n]) != len(indented[n+1]):
            print("lengths are not equal")
        if indented[n] != indented[n+1]:
            print("The following are not equal:")
            print(repr(indented[n]))
            print("----")
            print(repr(indented[n+1]))
            print("----")
    """
    assert(indented[0] == indented[1])
    assert(indented[1] == indented[2])



