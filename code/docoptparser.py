#!/usr/bin/env python3

# File: docoptparser.py

"""
Provides two utilities to parse a module's docstring 
assuming it's formatted to be parsed by the docopt module.
Both return dicts:
    One keyed by command name providing valid options for each
    the other keyed by option providing option descriptions.
"""

import os


FILENAME = os.path.expandvars("$CLUBU/utils.py")

def parse4opts_by_cmd(filename):
    """
    ## Should move the parsing functions into the utils module. ##
    Returns a dict keyed by command name.
    Each value is a listing of the possible options for that command.
    Gets its data by parsing the 'Usage:' part of <filename> which
    is expected to be "utils.py" (as a SPoL.)
    Second parameter not currently referenced but should perhaps store
    the result in <gbls> rather than returning it.
    Saved into gbls.opts_by_cmd
    """
    ret = {}
    cmd = ''
    opts = []
    parse = False
    with open(filename, 'r') as source:
        for line in source:
            line = line.strip()
            if line.startswith("Usage:"):
                parse = True
            elif parse:
                if not line:
                    break
                words = line.split()
                words = words[1:]  # get rid of "./utils.py"
                if (words[0] == '[-O]') or (
                    words[0].startswith('(label')):
                    # Simplify by ignoring these
                    continue
                key = words[0]
                opts = []
                for word in words[1:]:
                    if word.startswith(('[','(')):
                        word = word[1:]
                    if word.endswith((']',')')):
                        word = word[:-1]
                    if word.startswith('-'):
                        opts.append(word)
                ret[key] = opts
    return ret


def parse4opt_descriptors(filename):
    """
    ## Should move the parsing functions into the utils module. ##
    Returns a dict keyed by option. If both long and short options
    are provided they each have their (identical) entry.
    Each value is a list of strings describing the option.
    (These can be '\n\t'.joined.)
    Gets its data by parsing the 'Options:' part of <filename> which
    is expected to be "utils.py" (as a SPoL.)
    Second parameter not currently referenced but should perhaps store
    the result in <gbls> rather than returning it.
    """
    ret = {}
    short_long = []
    text = []
    parse = False
    with open(filename, 'r') as source:
        for line in source:
            line = line.strip()
            if line.startswith("Options:"):
                # begin parsing next line
                parse = True
            elif parse:
                if not line:  # No need to parse further
                    break     # after a blank line.
                if line.startswith('-'):
                    # begin parsing a new option...
                    # but 1st save any data already collected:
                    if short_long:  # False when dealing /w 1st option
                        for key in short_long:
                            # if both long and short options
                            # we make an entry for each:
                            ret[key] = text  # Data collection
                        short_long = []
                        text = []
                    words = []  # collector for non arg part of line
                    for word in line.split():
                        if word.startswith('-'):
                            short_long.append(word)
                        else:
                            words.append(word)
                    text.append(' '.join(words))
                else:
                    text.append(line)
    return ret

if __name__ == "__main__":
    cmd_opts = parse4opts_by_cmd(FILENAME)
    opt_descriptors = parse4opt_descriptors(FILENAME)

    options_header = "Commandline Options"
    descriptors_header = "Option Descriptions"
    print(options_header)
    print("=" * len(options_header))
    for key in sorted(cmd_opts.keys()):
        print("{}: {}".format(key, cmd_opts[key]))
    print()
    print(descriptors_header)
    print("=" * len(descriptors_header))
    for key in sorted(opt_descriptors.keys()):
        print("{}: {}".format(key,opt_descriptors[key][0]))
        for line in opt_descriptors[key][1:]:
            print("\t{}".format(line))

