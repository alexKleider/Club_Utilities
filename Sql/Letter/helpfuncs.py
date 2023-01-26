#!/usr/bin/env python3

# File: helpfuncs.py

"""
A slimmed down version of helpers.py
"""

import os
import datetime
import functools

date_template = "%b %d, %Y"
date_w_wk_day_template = "%a, %b %d, %Y"
date_year_template = "%y"
today = datetime.datetime.today()
month = today.month
this_year = today.year
fall_back = '''
s = today.strftime(date_template)
d = d
date = d.strftime(date_template)
'''
date = datetime.datetime.strptime(
        today.strftime(date_template),
        date_template
            ).strftime(date_template)
N_FRIDAY = 4  # ord of Friday: m, t, w, t, f, s, s
              # should instead use rbc.Club.N_FRIDAY???
FORMFEED = chr(ord('L') - 64)  # '\x0c'

CURRENT_CENTURY = '20'


def get_os_release():
    with open('/etc/os-release', 'r') as info:
        assignments = info.read()
    return assignments.split('\n')[0].split('=')[1][1:-1]


def verify(notice, report=None):
    """
    Print notice and call sys.exit() if response does not begin with
    'y' or 'Y'.
    If report is set, it is printed before sys.exit() is called.
    Returns True if sys.exit() is not called.
    """
    response = input(notice)
    if not (response and response[0] in 'yY'):
        if report:
            print(report)
        sys.exit()
    else: return True


def get_attributes(r):
    """
    # Not used but might be helpful.
    """
    return sorted([attribute for attribute in dir(r)
            if not attribute.startswith('__')])


def check_before_deletion(file_names):
    """
    Parameter <file_names> may be one name or a sequence of names.
    For each- check with user if ok to delete or overwrite.
    Aborts program execution if permission is not granted.
    Does not itself do any deletion.
    """
    if isinstance(file_names, str):
        file_names = (file_names, )
    for f in file_names:
        if os.path.exists(f):
            response = input(
                    "'{}' exists! Over write &/or delete it?(y/n) "
                    .format(f))
            if not(response and response[0] in 'yY'):
                print('Aborting program execution.')
                sys.exit()


def expand_date(date_string):
    """
    # Not used but might be helpful.
    Assumes date_string is in form yymmdd or yyyymmdd;
    Returns date in 'yyyy-mm-dd' format
    or "BAD DATE" if len(date_string) != 6 or 8.
    """
    if len(date_string) == 6:
        year = '{}{}'.format(CURRENT_CENTURY, date_string[:2])
    elif len(date_string) == 8:
        year = date_string[:4]
    else:
        print("Error: len(date_string) must be 6 or 8.")
        return 'BAD DATE'
    return '{}-{}-{}'.format(year, date_string[-4:-2],
                             date_string[-2:])


def get_datestamp(date=None):
    """
    Returns a string (for postal letters,) in the format 'Jul 03, 1945'.
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


def print_args(args, argument):
    """
    If args[argument] is True: print all the argument values.
    This works well with docopt when trying to debug.
    Screen width (number of columns) and height (number of rows) are
    assumed to be 80 and 24 unless defined by args['-w'] and/or
    args['r'] all respectively.
    """
#   print("Entering helpers.print_args")
    if args[argument]:
#       print(
#       "helpers.print_args' 2nd param evaluates 'True'")
        if '-w' in args.keys(): max_width = int(args['-w'])
        else: max_width = 80
        if '-r' in args.keys(): max_height = int(args['-r'])
        else: max_height = 24
        res = sorted(["{}: {}".format(key, args[key]) for key in args])
#       print(res)
        ret = tabulate(res, max_width=max_width, separator='   ')
        row_number = 0
        for row in ret:
            row_number += 1
            if row_number > max_height:
                row_number = 1
                _ = input("..any key to continue: ")
            print(row)
#       print("Got to here!!")
        response = input("...end of ## arguments. Continue? ")
        if not (response and response[0] in 'yY'):
            sys.exit()
    else:
#       print(
#       "helpers.print_args' 2nd param evaluates 'False'")
        pass  # no nothing if args['argument'] ==> False.


class Rec(dict):
    """
    Each instance is a (deep!) copy of the dict type parameter and is
    callable (with a formatting string as a parameter) returning the
    populated formatting string. Suitable for displaying the record
    &/or when one wants to have the record modified without changing
    the original record (as when passed by reference!!)
    """
    def __init__(self, rec):
#       self = {key:value for (key,value) in rec.items()}
        for key, value in rec.items():
            self[key] = value

    def __call__(self, fstr):
        return fstr.format(**self)


def useful_lines(stream, comment="#"):
    """
    A generator which accepts a stream of lines (strings.)
    Blank lines are ignored.
    If <comment> resolves to true, lines beginning with <comment>
    (after being stripped of leading spaces) are also ignored.
    <comment> can be set to <None> if don't want this functionality.
    Other lines are returned ("yield"ed) stripped of leading and
    trailing white space.
    """
    for line in stream:
        line = line.strip()
        if comment and line.startswith(comment):
            continue
        if line:
            yield line


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


if __name__ == "__main__":
    print(get_os_release())

