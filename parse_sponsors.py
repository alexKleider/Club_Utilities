#!/usr/bin/env python3

# File: parse_sponsors.py

"""
A work in progress: looking for a generalized way to parse files such
as: applicants.txt, sponsors.txt, etc
"""


def get_name_key(name):
    """
    Assumes <name> is a string consisting of two (a first and a last)
    names separated by at least one space.
    Returns a string in the format <last,first>.
    Returns None if fails.
    """
    name = name.strip().split()
    if not (len(names) == 2): return
    return '{1},{2}'.format(*names)


def parse_sponsors(line):
    """
    """
    line = line.strip()


def test_get_name_key(name_test_data):
    for item in name_test_data:
        if not get_name

 
test_data = (
        ('Kent Khtikian', 'Khtikian,Kent'),
        (' Kent Khtikian ','Khtikian,Kent'),
        (' Kent  Khtikian ','Khtikian,Kent'),
        )

if __name__ = "__main__":
    test
