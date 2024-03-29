#!/usr/bin/env python3

# File: find_calls.py

"""
Study function definitions, calls and assignments.

Definitions, Calls, & Assignments are sent to 
output files named below ("# output file names...")
"""

import re
import sys
import pprint
import helpers

# output file names...
DEFS = '2ck_defs'
CALLS = '2ck_calls'
CALLSf = '2ck_calls_formatted'
UNUSED = '2ck_unused'


EXPR = r"def (\w+)\("
PAT = re.compile(EXPR)

# first get our list of source code files:
MODULE_NAMES = ("archive",
                "content",
                "data",
#               "docoptparser",
                "dot_files",
                "find_calls",
                "helpers",
                "interface",
#               "json_as_txt",
                "member",
#               "parse_sponsors",
                "rbc",
#               "restore",
                "setup",
                "sys_globals",
                "utils",
                )

def call_found(func_name, line, refed=None):
    """
    Returns True if finc_name is called in line.
    Returns False if it is declared in line.
    Returns None if its name does not appear in the line.
    If <refed> is an empty list: functions that are referenced but
    neither defined nor called will be added.
    """
    if func_name in line:
        index = line.find(func_name)
        if index > 3 and 'def' in line[index-4:index+len(func_name)]:
            return False
        elif "{}(".format(func_name) in line:
            return True
        elif refed == []:
            refed.append(func_name)


def all_defs():
    """
    Returns a listing of the names of all functions/methods defined.
    Prints a warning if there are duplicates.
    """
    result = []
    for module in MODULE_NAMES:
        ret = []
        with open("{}.py".format(module), 'r') as fobj:
            line_n = 0
            for line in fobj:
                line_n += 1
                m = PAT.search(line)
                if m:
                    if m.group(1).endswith('_'):
                        # not sure about need to eliminate trailing
                        # underscore???
                        pass
                    else:
                        ret.append("{}.{} @ {}"
                                   .format(module,
                                           m.group(1),
                                           line_n))
        result.extend(ret)
        if len(ret) != len(set(ret)):
            n = len(ret) - len(set(ret))
            print("Warning! {} duplicate(s) in {}.py"
                  .format(n, module))
    return result


def split_datum(datum):
    module_name, func_name_w_line_n = datum.split('.')
    func_name, line_n = func_name_w_line_n.split('@')
    return module_name, func_name, line_n


def pformat(data):
    res = []
    current_module = ''
    for key in sorted(data.keys()):
        module, func, line_n = split_datum(key)
        if module != current_module:
            current_module = module
            if res:
                res.append('\f')
            res.append(module)
            res.append('=' * len(module))
#       res.append(func_w_line_n)
        res.append(key)
        if 'calls' in data[key]:
            res.append('  CALLS:')
            for entry in data[key]['calls']:
                res.append('    {}'.format(entry))
        if 'references' in data[key]:
            res.append('  REFS:')
            for entry in data[key]['references']:
                res.append('    {}'.format(entry))
    return res


def main():
    """
    """
    res = {}
    defs = all_defs()
    n_defs = len(defs)
    n_calls = 0
    n_refs = 0
    called_or_refed = set()
    helpers.output('\n'.join(defs), DEFS)
    print("Listing of functions (& methods) defined sent to '{}'"
            .format(DEFS))
    for mod_name in MODULE_NAMES:
        with open("{}.py".format(mod_name), 'r') as module:
            line_n = 0
            for line in module:
                line_n += 1
                for def_ in defs:
                    # searching for funtion def_
                    mod, func_w_n = def_.split('.')
                    func, n = func_w_n.split('@')
                    refed = []
                    if call_found(func, line, refed):
                        n_calls += 1
                        called_or_refed.add(def_)
                        _ = res.setdefault(def_, {})
                        _ = res[def_].setdefault("calls", [])
                        res[def_]["calls"].append(
                            "{} @ {}" .format(mod_name, line_n))
                    if refed:
                        n_refs += 1
                        called_or_refed.add(def_)
                        _ = res.setdefault(def_, {})
                        _ = res[def_].setdefault("references", [])
                        res[def_]["references"].append(
                            "{} @ {}".format(mod_name, line_n))

    n_no_refs = len(defs) - len(called_or_refed)
    no_refs = set(defs) - called_or_refed
    helpers.output('\n'.join(pformat(res)), CALLS)
    print("Listing of function (& method) calls sent to '{}'"
          .format(CALLS))
    helpers.output(pprint.pformat(res, compact=True, width=70),
                   CALLSf)
    print("Formatted listing of function (& method) calls sent to '{}'"
          .format(CALLSf))
    helpers.output('\n'.join(sorted(no_refs)), UNUSED)
    print("Listing of unused functions (& methods) sent to '{}'"
          .format(UNUSED))
    print("Found {} defs, {} calls, {} refs & {} with out either"
          .format(n_defs, n_calls, n_refs, n_no_refs))


if __name__ == '__main__':
    main()
