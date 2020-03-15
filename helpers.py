#!/usr/bin/env python3

# File: helpers.py

"""
Some helper functions needed by content and utils
and perhaps other modules in this folder.
"""

import datetime
import functools

date_template = "%b %d, %Y"
date_w_wk_day_template = "%a, %b %d, %Y"
today = datetime.datetime.today()
month = today.month
this_year = today.year
s = today.strftime(date_template)
d = datetime.datetime.strptime(s, date_template)
date = d.strftime(date_template)
n_friday = 4

def get_first_friday_of_month(date):
    year = date.year
    month = date.month
    for d in range(1, 8):  # range => 1..7 covering first week
#       print("checking day {}".format(d))
        first_friday =  datetime.date(year, month, d)
#       print("first_friday.weekday() => {}"
#               .format(first_friday.weekday()))
        if first_friday.weekday() == n_friday:
            return first_friday
    

def next_first_friday(today= datetime.date.today()):
    n_friday = 4
    year = today.year
    month = today.month
    date = get_first_friday_of_month(today)
    if not (date < today):
        return date.strftime(date_w_wk_day_template)
        # date.strftime(format)
    else:
#       print("Already had a friday this month")
        pass
    if month == 12:
        month = 1
        year = year + 1
#       print("Moved into next year")
    else:
        month = month + 1
    date = get_first_friday_of_month(datetime.date(year, month, 1))
    return date.strftime(date_w_wk_day_template)
    # date.strftime(format)
    print("ended with no return")


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


def add_header2list(header, list_,
        underline_char=None, extra_line=True):
    """
    Extends a list_ with a header preceded by an optional blank line
    and followed by an optional 'underline' composed of a specified
    character.
    """
    if extra_line: list_.append('')
    list_.append(header)
    if underline_char:
        list_.append(underline_char * len(header))


def show_dict(d, underline_char=None, extra_line=True):
    """
    Returns a list of strings representing a human readable version
    of a dictionary, the values of which are assumed to be lists
    of strings. If <underline_char> is specified, each key is
    an underlined header with corresponding values listed beneath;
    if not- each key is followed by its values all on one line.
    If <extra_line>, each key is preceded by an extra (blank) line.
    Keys and values are ordered/sorted.
    Typically one would specify either an underline_char or
    set extra_line to False.
    """
    ret = []
    for key in sorted([key for key in d.keys()]):
        if extra_line: ret.append('')
        if underline_char:
            ret.append(key)
            ret.append(underline_char * len(key))
            for val in sorted([val for val in d[key]]):
                ret.append(val)
        else:
            values = ", ".join(sorted(d[key]))
            ret.append("{}: {}".format(key, values))
    return ret


def create_json_file(json_data, json_file, verbose=True):
    with open(json_file, "w") as json_file_obj:
        if verbose:
            print('Dumping JSON to "{}".'
                .format(json_file_obj.name))
        json.dump(json_data, json_file_obj)


def longest(x, y):
    if len(x) > len(y):
        return x
    else:
        return y

def tabulate(data,
            display = None,  # a function
            alignment = '<', # left (<), right (>) or centered (^)
            down = True, #list by column (down) or by row (default)
            max_width = 75,
            max_columns = 0,
            separator = ' ', # minimum separation between columns
            force =0,
            usage=False,
            stats=False):
    """
    The single positional argument (<data>) must be an iterable, a
    representation of which will be returned as a list of strings
    which when '\\n'.join(ed) can be printed as a table.
    If <display> is provided it must be a function that, when
    provided with an element of data, returns a string
    representation.  If not provided, elements are assumed to have
    their own __repr__ and/or __str__ method(s).
    Possible values for <alignment> are '<', '^', and '>'
    for left, center, and right.
    <down> can be set to True if you want the elements to be listed
    down the columns rather than across each line.
    If <max_columns> is changed, it will be used as the upper limit
    of columns used. It is only effective if you specify fewer
    columns than would fit into <max_width> and any <force>
    specifiction will take precedence. (See next item.)
    <force> can be used to force groupings. If used, an attempt is
    made to keep items in groups of <force>, either vertically (if
    <down>) or horizontally (if not.)
    If both are specified, and if <force> is possible, <force> takes
    precedence over <max_columns>, otherwise <force> is ignored.
    If <usage> is set to True, the <data> parmeter is ignored and
    this document string is returned.
    If <stats> is set to True, output will show table layout but no table.
    """
    orig_max_col = max_columns
    if usage:
        print(tabulate.__doc__)
        return
    # Assign <display>:
    if not alignment in ('<', '^', '>'):
        return "Alignmemt specifier not valid: choose from '<', '^', '>'"
    if display: # Map to a representable format:
        _data = [display(x) for x in data]
    else:  # Eliminate side effects.
        _data = [x for x in data]
    # Establish length of longest element:
    max_len = len(functools.reduce(lambda x, y:
                            x if len(x)>len(y) else y, _data))
    # Establish how many can fit on a line:
    n_per_line = (
            (max_width + len(separator)) // (max_len + len(separator)))
    # Adjust for max_n_columns if necessary:
    # If <down> then <force> becomes irrelevant but otherwise,
    # force takes precedence over max_columns but within limits
    # of n_per_line.
#   print("max_columns ({}) < n_per_line ({})?"
#           .format(max_columns, n_per_line))
    if down:             # In down mode:
        if (max_columns > 0   # <force> is irelevant to n_per_line.
          and max_columns < n_per_line):
            n_per_line = max_columns
#           print("1. n_per_line is {}.".format(n_per_line))
    else:
        if max_columns < force and force <= n_per_line:
            max_columns = 0
        if force > 1 and n_per_line > force:
            _, remainder = divmod(n_per_line, force)
            n_per_line -= remainder
            forced = True
#           print("2. n_per_line is {}.".format(n_per_line))
        else:
            forced = False
        if max_columns > 0 and n_per_line > max_columns:
            if forced:
                temp_n = n_per_line
                while temp_n > max_columns:
                    temp_n -= force
                if temp_n > 0:
                    n_per_line = temp_n
            else:
                n_per_line = max_columns
#               print("3. n_per_line is {}.".format(n_per_line))
    if down:  # Tabulating downwards.
        column_data = []
        n_per_column, remainder = divmod(len(_data),n_per_line)
        if remainder:
            n_per_column += 1
        if force > 1:
            _, remainder = divmod(n_per_column, force)
            if remainder:
                n_per_column += force -remainder
        for j in range(n_per_column):
            for i in range(0, len(_data), n_per_column):
                try:
                    appendee = _data[i+j]
                except IndexError:
                    appendee = ''
                column_data.append(appendee)
        _data = column_data
    else:  # Tabulating accross so skip the above:
        pass
    if stats:
        return("Alignment={}, down={}, force={}, maxCol={}, n={}"
            .format(alignment, down, force, orig_max_col, n_per_line))

    new_data = []
    row = []
    for i in range(len(_data)):
        if not (i % n_per_line):
            new_data.append(separator.join(row))
            row = []
        try:
            appendee = ('{:{}{}}'
                .format(_data[i], alignment, max_len))
        except IndexError:
            appendee = ('{:{}{}}'
                .format('', alignment, max_len))
        row.append(appendee)
    if row:
            new_data.append(separator.join(row))
    while not new_data[0]:
        new_data = new_data[1:]
    new_data = [item.strip() for item in new_data]
    return new_data


def main():
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

def test_first_friday():
    print(next_first_friday())
    in_future = datetime.date(2010, 2, 20)
    print(next_first_friday(today= datetime.date(2010, 2, 20)))

if __name__ == "__main__":
    test_first_friday()


