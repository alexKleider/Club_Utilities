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


@pytest.mark.parametrize("line, expected", [
("Jason Crichfield      | 210427 | 210427 | 210604 | 210702 |",
    ("Crichfield, Jason", ('a2', '210604', '210702'))),
("John Ford             | 171006 | 171006 | ?????? | ?????? | ?????? | ?????? | ?????? |",
    ("Ford, John", ('m', '??????', '??????', '??????'))),
("Elizabeth Vezzani     | 180105 | 180105 | 180105 | 180202 | 180302 | 180406 | ?????? |",
    ("Vezzani, Elizabeth", ('m', '180105', '180202', '180302'))),
("Melinda Stone         | 171201 | 171201 | Application expired. ",
    ("Stone, Melinda", ('zae',))),
("Tim Corriero          | 171201 | 171201 | 171201 | 180105 | Application expired.",
    ("Corriero, Tim", ('zae',))),
("Melinda Stone         | 180601 | 180601 | 180601 | 180706 | 180803 | 181005 | 1901?? |",
    ("Stone, Melinda", ('m', '180601', '180706', '180803'))),
("Joseph Nowicki        | 190705 | 190705 | 190705 | Application expired.",
    ("Nowicki, Joseph", ('zae',))),
("Bridget Bartholome    | 200103 | 200103 | 200103 | 200207 | 200306 | 200403 | 200415 |",
    ("Bartholome, Bridget", ('m', '200103', '200207', '200306'))),
("Herbert Tully         | 200214 | 200214 | 200306 | 201204 | Application withdrawn (Remick)",
    ("Tully, Herbert", ('zae',))),
("Andrew Kleinberg      | 200727 | 200727 | 201002 | 210205 | 210305 | 210305 |",
    ("Kleinberg, Andrew", ('ai', '201002', '210205', '210305'))),
("Marco Garcia          | 200804 | 200804 | 201002 | 201204 | 210205 | 210305 | 210315 |",
    ("Garcia, Marco", ('m', '201002', '201204', '210205'))),
("Jason Crichfield",
    ("Crichfield, Jason", ('zaa',))),
("Tony Onorato          | 210506 | 210506 | 210507 | 210604 | 210702 | 210806 |",
    ("Onorato, Tony", ('ai', '210507', '210604', '210702'))),
    ])
def test_parse_applicant_data_line(line, expected):
    assert data.parse_applicant_data_line(line) == expected


@pytest.mark.parametrize("line, expected", [
("Jason Crichfield      | 210427 | 210427 | 210604 | 210702 |",
    ("Crichfield, Jason", ('a2', '210427', '210427', '210604', '210702'))),
("John Ford             | 171006 | 171006 | ?????? | ?????? | ?????? | ?????? | ?????? |",
    ("Ford, John", ('m', '171006', '171006', '??????', '??????', '??????', '??????', '??????'))), 
("Elizabeth Vezzani     | 180105 | 180105 | 180105 | 180202 | 180302 | 180406 | ?????? |",
    ("Vezzani, Elizabeth", ('m', '180105', '180105', '180105', '180202', '180302', '180406', '??????'))),
("Melinda Stone         | 171201 | 171201 | Application expired. ",
    ("Stone, Melinda", ('zae',))),
("Tim Corriero          | 171201 | 171201 | 171201 | 180105 | Application expired.",
    ("Corriero, Tim", ('zae',))),
("Melinda Stone         | 180601 | 180601 | 180601 | 180706 | 180803 | 181005 | 1901?? |",
    ("Stone, Melinda", ('m', '180601', '180601', '180601', '180706', '180803', '181005', '1901??'))),
("Joseph Nowicki        | 190705 | 190705 | 190705 | Application expired.",
    ("Nowicki, Joseph", ('zae',))),
("Bridget Bartholome    | 200103 | 200103 | 200103 | 200207 | 200306 | 200403 | 200415 |",
    ("Bartholome, Bridget", ('m', '200103', '200103', '200103', '200207', '200306', '200403', '200415'))),
("Herbert Tully         | 200214 | 200214 | 200306 | 201204 | Application withdrawn (Remick)",
    ("Tully, Herbert", ('zae',))),
("Andrew Kleinberg      | 200727 | 200727 | 201002 | 210205 | 210305 | 210305 |",
    ("Kleinberg, Andrew", ('ai', '200727', '200727', '201002', '210205', '210305', '210305'))),
("Marco Garcia          | 200804 | 200804 | 201002 | 201204 | 210205 | 210305 | 210315 |",
    ("Garcia, Marco", ('m', '200804', '200804', '201002', '201204', '210205', '210305', '210315'))),
("Jason Crichfield",
    ("Crichfield, Jason", ('zaa',))),
("Tony Onorato          | 210506 | 210506 | 210507 | 210604 | 210702 | 210806 |",
    ("Onorato, Tony", ('ai', '210506', '210506', '210507', '210604', '210702', '210806'))),
    ])
def test_parse_applicant_data_line4all_dates(line, expected):
    assert data.parse_applicant_data_line(
            line, app_dates=True, last_dates=True) == expected


@pytest.mark.parametrize("line, expected", [
("Camille Porter        | 210402 | 210402 | 210402 | 210507 | 210604 | 210702 | 210722 |",
    {"first": "Camille", "last": "Porter", "status": 'm', 'app_rcvd': '210402', 'fee_rcvd': '210402',
    '1st': '210402', '2nd': '210507', '3rd': '210604', 'approved': '210702', 'dues_paid': '210722',
    'Sponsor1': '', 'Sponsor2': ''}),
#("Tony Onorato          | 210506 | 210506 | 210507 | 210604 | 210702 | 210806 |",
#("Gabriel Bider         | 210504 | 210504 | 210507 | 210702 | 210806 |",
#("Jason Crichfield      | 210427 | 210427 | 210604 | 210702 |",
#("Daniel Speirn         | 210702 | 210702 | 210702 |",
#("Sandy Monteko-Sherman | 210801 | 210801 |",
#("Joe Shmo              | 210801",
#("Herbert Tully         | 200214 | 200214 | 200306 | 201204 | Application withdrawn (Remick)",
#("Joseph Nowicki        | 190705 | 190705 | 190705 | Application expired.",
#("John Ford             | 171006 | 171006 | ?????? | ?????? | ?????? | ?????? | ?????? |",
("Wiki Newcomb          | 171006 | 171006 | ?????? | ?????? | ?????? | ?????? | ??????",
    {"first": "Wiki", 'last': 'Newcomb', 'status': 'm', 'app_rcvd': '171006', 'fee_rcvd': '171006',
     '1st': '??????', '2nd': '??????', '3rd': '??????', 'approved': '??????', 'dues_paid': '??????',
     'Sponsor1': '', 'Sponsor2': ''}),
])
def test_applicant_data_line2record(line, expected):
    assert data.applicant_data_line2record(line) == expected

