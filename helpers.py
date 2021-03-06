#!/usr/bin/env python3

# File: helpers.py

"""
Helper functions developed for the Club/Utils repo.
This file also appears in ~/PyLib (by means of a hard link.)
"""

import os
import sys
import json
import datetime
import functools

date_template = "%b %d, %Y"
date_w_wk_day_template = "%a, %b %d, %Y"
date_year_template = "%y"
today = datetime.datetime.today()
month = today.month
this_year = today.year
s = today.strftime(date_template)
d = datetime.datetime.strptime(s, date_template)
date = d.strftime(date_template)
N_FRIDAY = 4  # ord of Friday: m, t, w, t, f, s, s
FORMFEED = chr(ord('L') - 64)  # '\x0c'


def script_location():
    return os.path.dirname(os.path.realpath(__file__))


def useful_lines(stream, comment=None):
    for line in stream:
        line = line.strip()
        if comment and line.startswith(comment):
            continue
        if line:
            yield line


def get_first_friday_of_month(date):
    """
    Returns a datetime.date object.
    """
    year = date.year
    month = date.month
    for d in range(1, 8):  # range => 1..7 covering first week
        day = datetime.date(year, month, d)
        if day.weekday() == N_FRIDAY:
            return day


def next_first_friday(today=datetime.date.today(),
                      exclude=False):
    """
    If <exclude> result will never be Jan 1
    Jan 8th will be returned.
    Returns a string (formated date.)
    """
    year = today.year
    month = today.month
    date = get_first_friday_of_month(today)
    if exclude:
        if date.month == 1 and date.day == 1:
            date = date + datetime.timedelta(days=7)
    if date < today:
        if month == 12:
            month = 1
            year = year + 1
        else:
            month = month + 1
        date = get_first_friday_of_month(
            datetime.date(year, month, 1))
        if exclude:
            if date.month == 1 and date.day == 1:
                date = date + datetime.timedelta(days=7)
    return date.strftime(date_w_wk_day_template)


# print("Setting the date to '{}'.".format(date))


def club_year(which='this', now=datetime.date.today()):
    if which == 'last':
        n = -1
    elif which == 'this':
        n = 0
    elif which == 'next':
        n = 1
    else:
        print("Invalid parameter given to helpers.club_year()")
        sys.exit()
    if now.month > 6:
        return "{}-{}".format(now.year + n, now.year + n+1)
    else:
        return "{}-{}".format(now.year + n -1, now.year + n)


def expand_date(date_string):
    if len(date_string) == 6:
        year = '20{}'.format(date_string[:2])
    elif len(date_string) == 8:
        year = date_string[:4]
    else:
        print("Error: len(date_string) must be 6 or 8.")
        return 'BAD DATE'
    return '{}-{}-{}'.format(year, date_string[-4:-2],
                             date_string[-2:])


def get_datestamp(date=None):
    """
    Returns a string depicting the current date (for postal letters.)
    If <date> is provided it must be type datetime.datetime or
    datetime.date.  If not provided, today's date is used.
    """
    if date:
        if (isinstance(date,datetime.date) 
            or isinstance(date, datetime.datetime)):
            d = date
        else:
            print("helpers.get_datestamp got a bad argument")
            sys.exit()
    else:
        d = datetime.date.today()
    return d.strftime(date_template)


def format_dollar_value(value):
    if value > 0:
        return "${:,.2f}".format(value)
    elif value == 0:
        return "$0.00"
    elif value < 0:
        return "-${:,.2f}".format(abs(value))
    else:
        assert False


def indent(text, n_spaces):
    """
    Helper function providing indentation for postal content.
    Can deal with either a list of strings ('lines')
    or one string ('lines' terminated by linefeeds.)
    In either case, returns a string.
    """
    assert type(n_spaces) == int
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


def expand_array(content, n):
    if len(content) > n:
        print("ERROR: too many lines in <content>")
        print("    parameter of content.expand()!")
        assert False
    a = [item for item in content]
    while n > len(a):
        if n - len(a) >= 2:
            a = [''] + a + ['']
        else:
            a.append('')
    return a


def expand_string(content, n):
    a = content.split('\n')
    ret = expand_array(a, n)
    return '\n'.join(ret)


def expand(content, nlines):
    """
    Takes <content> which can be a list of strings or
    all one string with line feeds separating it into lines.
    Returns the same type (either string or list) but of <nlines>
    length, centered by blank strings/lines. If need an odd number
    of blanks, the odd one is at end (rather than the beginning.
    Fails if <content> has more than nlines.
    """
    if isinstance(content, str):
        return expand_string(content, nlines)
    else:
        return expand_array(content, nlines)


def add_header2list(header, list_, underline_char=None,
                    extra_line=True, indent=0):
    """
    Extends a list_ with a header preceded by an optional blank line
    and followed by an optional 'underline' composed of a specified
    character.
    Optional number of spaces to <indent>.
    """
    if extra_line:
        list_.append('')
    list_.append(" " * indent + header)
    if underline_char:
        list_.append(" " * indent + underline_char * len(header))


def add_sub_list(sub_header, sub_list, main_list,
                 underline_char="=", extra_line=True, indent=0):
    """
    Extends an existing <main_list> with a sorted version of
    <sub_list>.
    The added part is separated from the original by <separator> which
    must be a (possibly empty) list of strings- it defaults to a
    list of one empty string.
    """
    add_header2list(sub_header, main_list,
                    underline_char=underline_char,
                    extra_line=extra_line,
                    indent=indent)
    if indent:
        for item in sorted(sub_list):
            main_list.append(' ' * indent + item)
    else:
        main_list.extend(sorted(sub_list))


def prepend2file_name(word, file_name):
    head, tail = os.path.split(file_name)
    return os.path.join(head, ''.join((word, tail)))


def show_json(json, underlinechar=''):
    """
    Returns a human readable representation of json data
    as a list of lines (which can be '\n'.joined.)
    If underlinechar is specified, each key is underlined and
    preceeded by a blank line.
    """
    collector = []
    indent = 0

    def collect(json, indent=indent, collector=collector):
        if isinstance(json, dict):
            # if keys need to be sorted change code by replaceing the
            # next line with:
            # for key in sorted(json.keys()):
            for key in json:
                if underlinechar:
                    collector.extend(['', key, underlinechar*len(key)])
                else:
                    collector.append(key)
                collect(json[key], indent=indent+2)
        elif isinstance(json, list):
            for item in json:
                collect(item, indent, collector)
        else:
            collector.append(' '*indent+str(json))

    collect(json, indent=indent, collector=collector)
    return collector


def test_show_json():
    data = {"Chadwick, Michael": [["Mooring", 114]], "Churchman, Josh": [["Mooring", 114]], "Cowman, Tim": [["Mooring", 114]], "Differding, Gary": [["Mooring", 114]], "Ferraro, Joseph": [["Mooring", 138]], "Mann, Ed": [["Mooring", 114]], "Murch, Don": [["Mooring", 152]], "O'Connor, Daniel": [["Mooring", 138]], "O'Neil, Terry": [["Mooring", 132]], "Rodoni, Fred": [["Mooring", 114]], "Smith, Thornton": [["Mooring", 138]], "Swanson, Eric": [["Mooring", 126]], "Bettini, Rick": [["Dock", 75]], "Buckenmeyer, Robert": [["Dock", 75]], "Dixon, Rupert": [["Dock", 75]], "Ferlinghetti, Leonardo": [["Dock", 75]], "Finney, Scott": [["Dock", 75]], "Heffelfinger, Robert": [["Dock", 75]], "Krakauer, George": [["Dock", 75]], "Krieger, Nicholas": [["Dock", 75]], "Light, Mike": [["Dock", 75]], "MacDonald, Bob": [["Dock", 75]], "Martinelli, Chris": [["Dock", 75]], "McPhail, Jeff": [["Dock", 75], ["Kayak", 70]], "Norton, William": [["Dock", 75]], "O'Connor, Nick": [["Dock", 75]], "Smith, Peter": [["Dock", 75]], "Vantress, John": [["Dock", 75]], "Walker, Kirsten": [["Dock", 75]], "Barth, Doug": [["Kayak", 70]], "Cirincione-Coles, Kathryn": [["Kayak", 70]], "Griffith, Melinda": [["Kayak", 70]], "Martin, Monica": [["Kayak", 70]], "Mott, James": [["Kayak", 70]], "Pedemonte, Richard": [["Kayak", 70]], "Read, Don": [["Kayak", 70]], "Sawyer, Aenor": [["Kayak", 70]], "Straton, Joe": [["Kayak", 70]], "Thompson, Randall": [["Kayak", 70]], "Tremp, Dieter": [["Kayak", 70]]}
    print('\n'.join(show_json(data)))


def dump2json_file(data, json_file, verbose=True):
    with open(json_file, "w") as json_file_obj:
        if verbose:
            print('Dumping (json) data to "{}".'.format(
                  json_file_obj.name))
        json.dump(data, json_file_obj)


def get_json(file_name, report=False):
    """
    Reads 'file_name' and returns a dict.
    Provides optional reporting.
    """
    with open(file_name, 'r') as f_obj:
        if report:
            print('Reading JSON file "{}".'.format(f_obj.name))
        return json.load(f_obj)


def longest(x, y):
    if len(x) > len(y):
        return x
    else:
        return y


def tabulate(data,
             display=None,   # a function
             alignment='<',  # left (<), right (>) or centered (^)
             down=True,  # list by column (down) or by row (default)
             max_width=145,
             max_columns=0,
             separator=' | ',  # minimum separation between columns
             force=0,
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
    if alignment not in ('<', '^', '>'):
        return "Alignmemt specifier not valid: choose from '<', '^', '>'"
    if display:  # Map to a representable format:
        _data = [display(x) for x in data]
    else:  # Eliminate side effects.
        _data = [x for x in data]
    # Establish length of longest element:
    max_len = len(functools.reduce(
                  lambda x, y: x if len(x) > len(y) else y, _data))
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
        # <force> is irelevant to n_per_line.
        if (max_columns > 0) and (max_columns < n_per_line):
            n_per_line = max_columns
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
        n_per_column, remainder = divmod(len(_data), n_per_line)
        if remainder:
            n_per_column += 1
        if force > 1:
            _, remainder = divmod(n_per_column, force)
            if remainder:
                n_per_column += force - remainder
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
               .format(
                   alignment, down, force, orig_max_col, n_per_line))

    new_data = []
    row = []
    for i in range(len(_data)):
        if not (i % n_per_line):
            new_data.append(separator.join(row))
            row = []
        try:
            appendee = ('{:{}{}}'.format(_data[i],
                                         alignment, max_len))
        except IndexError:
            appendee = ('{:{}{}}'.format('', alignment, max_len))
        row.append(appendee)
    if row:
        new_data.append(separator.join(row))
    while not new_data[0]:
        new_data = new_data[1:]
    new_data = [item.strip() for item in new_data]
    return new_data


def output(data, destination=None, announce=True):
    """
    Sends data (text) to (a file called) <destination>
    (which defaults to stdout.)
    """
    if destination is None:
        print(data)
    else:
        with open(destination, "w") as fileobj:
            fileobj.write(data)
            if announce:
                print('Data written to "{}".'.format(fileobj.name))


def main():
    print("The month is '{}'.".format(month))
    print("'helpers.get_datestamp() returns '{}'."
          .format(date))

    print("'this_club_year()' returns '{}'."
          .format(this_club_year()))

    addresses = [
        "Alex Kleider\nPO Box 277\nBolinas, CA 94924",
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
    print(next_first_friday(today=datetime.date(2010, 2, 20)))


if __name__ == "__main__":
    #   test_first_friday()
    print("This year is {}.".format(this_year))
    main()
