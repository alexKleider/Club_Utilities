#!/usr/bin/env python3

# File: find_calls.py

"""
Get a listing of all function calls in each module.
Top level keys: tuple consisting of name of function being called
and the module in which it is declared;
next level keys: module where the call is being made
final value: list of line numbers where the call appears.
"""

import re
import sys
import pprint
import helpers

EXPR = r"def (\w+)\("
PAT = re.compile(EXPR)

# first get our list of source code files:
MODULE_NAMES = ("content",
                "data",
                "helpers",
                "member",
                "rbc",
                "utils",
                )


def call_found(func_name, line, refed):
    """
    Returns True is finc_name is called in line.
    Returns False if it is declared in line.
    Returns None if its name does not appear in the line.
    If func_name is neither defined or called but is referenced,
    it will be appended to refed if it is an empty list.
    """
    if func_name in line:
        index = line.find(func_name)
        if index > 3 and 'def' in line[index-4:index+len(func_name)]:
            return False
        elif "{}(".format(func_name) in line:
            return True
        elif refed == []:
            refed.append(func_name)


def cleanedup(d):
    new_d = {}
    modules = d.keys()
    for module in modules:
        funcs = d[module].keys()
        for func in funcs:
            if d[module][func]:
                _ = new_d.setdefault(module, {})
                new_d[module][func] = d[module][func]
    return new_d


def find_defs(module):
    """
    Returns the set of names of functions/methods defined in module.
    """
    ret = set()
    with open("{}.py".format(module), 'r') as fobj:
        for line in fobj:
            m = PAT.search(line)
            if m:
                if m.group(1).endswith('_'):
                    pass
                else:
                    ret.add(m.group(1))
    return ret


def yield_function_names(names_by_module):
    for module in names_by_module.keys():
        for function_name in names_by_module[module]:
            yield function_name

def main():
    """
    """
    res = {}
    refs = {}

    # Step 1:
    # Collect the name of each function or method declared
    # indexed by the module where the declaration appears:
    names_by_module = {}
    for f in MODULE_NAMES:
        names_by_module[f] = find_defs(f)
    helpers.output(pprint.pformat(names_by_module), 'defs')
    for module in names_by_module.keys():
        res[module] = {}
        refs[module] = {}
        for func in names_by_module[module]:
            res[module][func] = {}
            refs[module][func] = {}
#   pprint.pprint(res)
            
    # Step 2:
    # Iterate line for line through each module.
    # For each line, 
    #    Iterate through all declared functions for a call to it.
    for module_name in MODULE_NAMES:
        fname = '{}.py'.format(module_name)
        linenumber = 0
        with open(fname, 'r') as fobj:
            for line in fobj:
                linenumber += 1
                for module in MODULE_NAMES:
                    for funcname in names_by_module[module]:
                        collector = []
                        if call_found(funcname, line, collector):
                            _ = res[module][funcname].setdefault(
                                                module_name, [])
                            res[module][funcname][module_name
                                        ].append(linenumber)
                        if (module == 'content'
                            and funcname == 'prepare_email_template'
                            and linenumber == 1150
                            ):
                            print('{} {}: {}.{}'
                                  .format(module_name, linenumber,
                                  module, funcname))
                        if collector:
                            _ = refs[module][funcname].setdefault(
                                                module_name, [])
                            refs[module][funcname][module_name
                                        ].append(linenumber)
    helpers.output(pprint.pformat(res), 'calls')
    helpers.output(pprint.pformat(cleanedup(refs)), 'references')


if __name__ == '__main__':
    main()
