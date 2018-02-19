#!/home/alex/.virtualenvs/djbk/bin/python

# File: columnar.py

"""
Usage:
    columnar.py [-c <n> |-w <m>] [FILE]
    columnar.py (-h|--help)
    columnar.py --version

Options:
    -h --help   Show this screen.
    --version   Show version
    -c <n>, --columns=<n>   number of columns.
    -w <m>, --char_width=<m>  page width in chars.

If a source FILE is not specified, input is expected from stdin.
Output goes to stdout and thus can be redirected to a file.
The following NOT yet implemented:
Any lines beginning with a '#' are reproduced as is and the
collimating process is begun (again.)
Blank lines are ignored.
"""

import sys
import docopt
args = docopt.docopt(__doc__, version='v0.0.0')
#                     see: https://semver.org/
print(args)
print(args['FILE'])
_ = input("Enter to continue, 'a' to abort.. ")
if _ and _[0] == 'a':
    sys.exit()

comments = []
data = []
res = []
longest = 0

last_was_data = False

def columns(iterable,
            horizontal_limit=70,
            minimum_separation=2,
            n_columns=None,
            downwards=True,
            empty_content=''):
    """
    Returns a columnar version of the iterable as a list of lines.
    Default is to choose a column width to allow for the longest
    entry and this in turn will determine the number of columns.
    If n_columns is set to an integer, horizontal_limit is ignored.
    The default is for order of presentation to be downwards (down
    columns sequentially.)
    If <downwards> is set to 'False', order of presentation will be
    horizontal (along rows.)
    By default unused cells are left empty.
    If <empty_content> is set to a single character, that character
    is used to fill the cell, if more than one character, the string
    is used.
    """
    res = []
    empty_content_length = len(empty_content)
    n_entries = len(iterable)
    if not n_entries:
        return res
    max_length = 0
    for entry in iterable:
        entry_length = len(entry)
        if entry_length > max_length:
            max_length = entry_length
    if empty_content_length > max_length:
        max_length = empty_content_length
    if len(empty_content) == 1:
        empty_content = empty_content * max_length
    print("h_limit: {}, min_sep: {}, max_l: {}, min_sep: {}"
        .format(horizontal_limit, minimum_separation,
            max_length, minimum_separation))
    if not n_columns:
        n_columns = ((horizontal_limit + minimum_separation)
            // (max_length + minimum_separation))
    formatting_string = "{{:<{}}}".format(str(n_columns-1))
    print("n_columns: {}, f_string: {}"
        .format(n_columns, formatting_string))
    for n in range(1, n_columns):
        formatting_string = (formatting_string
            + " "* minimum_separation
            + formatting_string)
    modulo = n_entries % n_columns
    if modulo:
        for i in range(n_columns - modulo):
            iterable.append(empty_content)
            n_entries += 1
    if downwards:
        fraction_of_n = n_entries//n_columns
        terminator = fraction_of_n
        i = 0
        while i < terminator:
            tup = (iterable[i], )
            for j in range(1, n_columns):
                tup = (*tup, iterable[i + fraction_of_n * j])
            print(formatting_string)
            print(*tup)
            res.append(formatting_string.format(*tup))
            i += 1
    else:
        # use 'yield' here?
        pass
    return res

def process_file(iterable):
    for line in iterable:
        line = line.strip()
        if line:
            if line[0]=='#':
                columate_data(data)
                res.append(line)
            else:
                data.append(line)
                longest = len(line)

if __name__ == "__main__":
    iterable = []
    try:
        with open(args["FILE"], 'r') as fileobj:
            for line in fileobj:
                if line:
                    iterable.append(line.strip())
            print("\n".join(columns(iterable)))
    except NameError:
        print("File not declared; use stdin:")
        data = []
        while True:
            datum = input("> ")
            if datum:
                data.append(datum)
            else:
                break
        print(columns(data))
    except FileNotFoundError:
        print("Specified file doesn't exist.")

