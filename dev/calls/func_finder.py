#!/usr/bin/env python3

# File: func_finder.py


import sys
import re


DEF_EXPR = r"def (\w+)\("
DEF_PAT = re.compile(DEF_EXPR)

CALL_EXPR = r"(\w+)\("
CALL_PAT = re.compile(CALL_EXPR)

REF_EXPR = r"\b[a-zA-Z]\w*\b(?![(])"
REF_PAT = re.compile(REF_EXPR)

module_names = (
            "content",
            "data",
            "helpers",
            "interface",
            "member",
            "rbc",
            "sys_globals",
            "utils",
        )


def target_path(module_name):
    return  "/home/alex/Git/Club/Utils/{}.py".format(module_name)

def find_defs(module_name):
    ret = []
    line_n = 0
    with open(target_path(module_name), 'r') as stream:
        for line in stream:
            line_n += 1
            m = DEF_PAT.search(line)
            if m:
                ret.append("{}.{} @ {}"
                        .format(module_name,
                                m.group(1),
                                line_n))
    return ret


def find_calls(module_name):
    ret = []
    line_n = 0
    with open(target_path(module_name), 'r') as stream:
        for line in stream:
            line_n += 1
            # could be more than one call in a line...
            iterator = CALL_PAT.finditer(line)
            for c in iterator:
                call = c.group(1)
                d = line.find('def ')
                m = line.find(call)
                if ((d > -1) and ((m - d) == 4)):
                    continue
                ret.append("{}.{} @ {}"
                        .format(module_name,
                                call,
                                line_n))
    return ret


def find_refs(names, module_name):
    ret = []
    line_n = 0
    with open(target_path(module_name), 'r') as stream:
        for line in stream:
            line_n += 1
            words = [match.group() for match in
                    REF_PAT.finditer(line)]
            for name in names:
                if name in words:
                    ret.append("{}.{} @ {}"
                            .format(module_name,
                                    name,
                                    line_n))
    return ret


def extract_name(entry):
    """
    Return just the name as in the underscored part..
    'member.set_kayak_fee @ 671'
            ^^^^^^^^^^^^^
    .. devoid of module name and '@ line#'.
    """
    parts = entry.split('.')
    bits = parts[1].split('@')
    return bits[0].strip()


def names_only(listing):
    return [extract_name(entry) for entry in listing]


if __name__ == "__main__":
    defs = []
    for name in sorted(module_names):
        l = find_defs(name)
        defs.extend(l)

    calls = []
    for name in sorted(module_names):
        l = find_calls(name)
        calls.extend(l)

    uncalled = []
    call_set = set(extract_name(call) for call in calls)
    uncalled = [d for d in defs if
                extract_name(d) not in call_set]
    
    refs = []
    for module_name in module_names:
        refs.extend(find_refs(names_only(uncalled), module_name))

#   print("\nrefs")
#   for item in sorted(refs):
#       print(item)

    reffed_names = set(names_only(refs))
    uncalled_names = set(names_only(uncalled))
    unused_set = uncalled_names - reffed_names
    unused_listing = []
    for item in defs:
        if extract_name(item) in unused_set:
            unused_listing.append(item)

    print("\nunused:")
    for item in unused_listing:
        print(item) 
