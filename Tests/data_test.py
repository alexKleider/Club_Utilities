#!/usr/bin/env python3

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
    ('Khtikian,Kent', ('Siedman, Jack', 'Murch, Don'))),
('Andrew Kleinberg:  Rudi Ferris, Ralph Camiccia',
    ('Kleinberg,Andrew', ('Ferris, Rudi', 'Camiccia, Ralph'))),
('Jen Hatch:  Kimberly Goosherst, Shervin Kheradpir',
    ('Hatch,Jen', ('Goosherst, Kimberly', 'Kheradpir, Shervin'))),
('Hector Mora-Lopez: Ed Mann, Esra Connor',
    ('Mora-Lopez,Hector', ('Mann, Ed', 'Connor, Esra'))),
('July Guzman:  Kirsten Walker, William Norton',
    ('Guzman,July', ('Walker, Kirsten', 'Norton, William'))),
('Marco Garcia:  Kirsten Walker, Albert Foreman',
    ('Garcia,Marco', ('Walker, Kirsten', 'Foreman, Albert'))),
('Sam Schow:  Rudi Ferris, Joel Booth',
    ('Schow,Sam', ('Ferris, Rudi', 'Booth, Joel'))),
('Jason Crichfield: Joseph Ferraro, Ralph Camiccia',
    ('Crichfield,Jason', ('Ferraro, Joseph', 'Camiccia, Ralph'))),
('Matthew Lundy: Ralph Camiccia, Rudi Ferris',
    ('Lundy,Matthew', ('Camiccia, Ralph', 'Ferris, Rudi'))),
])
def test_parse_sponsor_data_line(line, expected):
    assert data.parse_sponsor_data_line(line) == expected


@pytest.mark.parametrize("line, expected", [
("Jason Crichfield      | 210427 | 210427 | 210604 | 210702 |",
    ( {"first": 'Jason', "last": 'Crichfield', "status": 'a2',
        "app_rcvd": "210427", "fee_rcvd": '210427', "1st": '210604',
        "2nd": '210702', "3rd": '', "inducted": '',
        "dues_paid": '', "sponsor1": '', "sponsor2": ''}),
    ),
("Elizabeth Vezzani     | 180105 | 180105 | 180105 | 180202 | 180302 | 180406 | 180618 |",
    ({'first': "Elizabeth", 'last': "Vezzani", 'status': 'm',
        'app_rcvd': '180105', 'fee_rcvd': '180105', '1st': '180105',
        '2nd': '180202', '3rd': '180302', 'inducted': '180406',
        'dues_paid': '180618',
        'sponsor1': '', 'sponsor2': ''}
    )),
("Melinda Stone         | 171201 | 171201 | Application expired. ",
    ({'first': "Melinda", 'last': "Stone", 'status': 'zae',
        'app_rcvd': '171201', 'fee_rcvd': '171201', '1st': '',
        '2nd': '', '3rd': '', 'inducted': '',
        'dues_paid': '',
        'sponsor1': '', 'sponsor2': ''}
    )),
("Tim Corriero          | 171201 | 171201 | 171201 | 180105 | Application expired.",
    ({'first': "Tim", 'last': "Corriero", 'status': 'zae',
        'app_rcvd': '171201', 'fee_rcvd': '171201', '1st': '171201',
        '2nd': '180105', '3rd': '', 'inducted': '',
        'dues_paid': '',
        'sponsor1': '', 'sponsor2': ''}
    )),
("Joseph Nowicki        | 190705 | 190705 | 190705 | Application expired.",
    ({'first': "Joseph", 'last': "Nowicki", 'status': 'zae',
        'app_rcvd': '190705', 'fee_rcvd': '190705', '1st': '190705',
        '2nd': '', '3rd': '', 'inducted': '',
        'dues_paid': '',
        'sponsor1': '', 'sponsor2': ''}
    )),
("Herbert Tully         | 200214 | 200214 | 200306 | 201204 | Application withdrawn (Remick)",
    ({'first': "Herbert", 'last': "Tully", 'status': 'zae',
        'app_rcvd': '200214', 'fee_rcvd': '200214', '1st': '200306',
        '2nd': '201204', '3rd': '', 'inducted': '',
        'dues_paid': '',
        'sponsor1': '', 'sponsor2': ''}
    )),
("Marco Garcia          | 200804 | 200804 | 201002 | 201204 | 210205 | 210305 | 210315 |",
    ({'first': "Marco", 'last': "Garcia", 'status': 'm',
        'app_rcvd': '200804', 'fee_rcvd': '200804', '1st': '201002',
        '2nd': '201204', '3rd': '210205', 'inducted': '210305',
        'dues_paid': '210315',
        'sponsor1': '', 'sponsor2': ''}
    )),
("Tony Onorato          | 210506 | 210506 | 210507 | 210604 | 210702 | 210806 |",
    ( {"first": 'Tony', "last": 'Onorato', "status": 'ad',
        "app_rcvd": "210506", "fee_rcvd": '210506', "1st": '210507',
        "2nd": '210604', "3rd": '210702', "inducted": '210806',
        "dues_paid": '', "sponsor1": '', "sponsor2": ''}),
    ),
("Wiki Newcomb          | 171006 | 171006 | ?????? | ?????? | ?????? | ?????? | ??????",
    {"first": "Wiki", 'last': 'Newcomb', 'status': 'm', 'app_rcvd': '171006', 'fee_rcvd': '171006',
     '1st': '??????', '2nd': '??????', '3rd': '??????', 'inducted': '??????', 'dues_paid': '??????',
     'sponsor1': '', 'sponsor2': ''}),
("Camille Porter        | 210402 | 210402 | 210402 | 210507 | 210604 | 210702 | 210722 |",
    {"first": "Camille", "last": "Porter", "status": 'm', 'app_rcvd': '210402', 'fee_rcvd': '210402',
    '1st': '210402', '2nd': '210507', '3rd': '210604', 'inducted': '210702', 'dues_paid': '210722',
    'sponsor1': '', 'sponsor2': ''}),
])
def test_applicant_data_line2record(line, expected):
    assert data.applicant_data_line2record(line) == expected


