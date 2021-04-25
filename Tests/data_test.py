#!/usr/bin/env python

# File: Tests/data_test.py

"""
Have so far written tests for:
    parse_applicant_data_line
    parse_sponsor_data_line
"""

# Must first add the parent directory of the
# currently running script to the system path:
import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])
# print(sys.path)
# ... or alternatively set PYTHONPATH to project directory:
# export PYTHONPATH=/home/alex/Git/Club/Utils

import data
import rbc
import sys_globals as glbs
import pytest

@pytest.mark.parametrize("line, expected", [
("John Ford             | 171006 | 171006 | ?????? | ?????? | ?????? | ?????? | ?????? |",
    ("Ford, John", ('m'))),
("Elizabeth Vezzani     | 180105 | 180105 | 180105 | 180202 | 180302 | 180406 | ?????? |",
    ("Vezzani, Elizabeth", ('m'))),
("Melinda Stone         | 171201 | 171201 | Application expired. ",
    ("Stone, Melinda", ('zae'))),
("Tim Corriero          | 171201 | 171201 | 171201 | 180105 | Application expired.",
    ("Corriero, Tim", ('zae'))),
("Melinda Stone         | 180601 | 180601 | 180601 | 180706 | 180803 | 181005 | 1901?? |",
    ("Stone, Melinda", ('m'))),
("Joseph Nowicki        | 190705 | 190705 | 190705 | Application expired.",
    ("Nowicki, Joseph", ('zae'))),
("Bridget Bartholome    | 200103 | 200103 | 200103 | 200207 | 200306 | 200403 | 200415 |",
    ("Bartholome, Bridget", ('m'))),
("Herbert Tully         | 200214 | 200214 | 200306 | 201204 | Application withdrawn (Remick)",
    ("Tully, Herbert", ('zae'))),
("Andrew Kleinberg      | 200727 | 200727 | 201002 | 210205 | 210305 | 210305 |",
    ("Kleinberg, Andrew", ('ai', '201002', '210205', '210305'))),
("Marco Garcia          | 200804 | 200804 | 201002 | 201204 | 210205 | 210305 | 210315 |",
    ("Garcia, Marco", ('m'))),
("Jason Crichfield",
    ("Crichfield, Jason", ('zaa'))),
    ])
def test_parse_applicant_data_line(line, expected):
    assert data.parse_applicant_data_line(line) == expected


@pytest.mark.parametrize("line, expected", [
('Kent Khtikian: Jack Siedman, Don Murch',
    ('Khtikian, Kent', ('Jack Siedman', 'Don Murch'))),
('Andrew Kleinberg:  Rudi Ferris, Ralph Camiccia',
    ('Kleinberg, Andrew', ('Rudi Ferris', 'Ralph Camiccia'))),
('Jen Hatch:  Kimberly Goosherst, Shervin Kheradpir',
    ('Hatch, Jen', ('Kimberly Goosherst', 'Shervin Kheradpir'))),
('Hector Mora-Lopez: Ed Mann, Esra Connor',
    ('Mora-Lopez, Hector', ('Ed Mann', 'Esra Connor'))),
('July Guzman:  Kirsten Walker, William Norton',
    ('Guzman, July', ('Kirsten Walker', 'William Norton'))),
('Marco Garcia:  Kirsten Walker, Albert Foreman',
    ('Garcia, Marco', ('Kirsten Walker', 'Albert Foreman'))),
('Sam Schow:  Rudi Ferris, Joel Booth',
    ('Schow, Sam', ('Rudi Ferris', 'Joel Booth'))),
('Jason Crichfield: Joseph Ferraro, Ralph Camiccia',
    ('Crichfield, Jason', ('Joseph Ferraro', 'Ralph Camiccia'))),
('Matthew Lundy: Ralph Camiccia, Rudi Ferris',
    ('Lundy, Matthew', ('Ralph Camiccia', 'Rudi Ferris'))),
])
def test_parse_sponsor_data_line(line, expected):
    assert data.parse_sponsor_data_line(line) == expected
