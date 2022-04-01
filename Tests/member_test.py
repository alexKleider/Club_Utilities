#!/usr/bin/env python3
# File: Tests/member_test.py

# Must first add the parent directory of the
# currently running script to the system path:
import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])

import pytest
import helpers
import member

d1 = {'a': [1,2,3,4],
      'b': {1,2,3,4},
      'c': 'a string',
     }
expected = {'a': [1,2,3,4],
            'c': 'a string',
           }


@pytest.mark.parametrize("s, rl, l, expected", [
    ('exec', ('pres', 'vp', 'treas', 'sec', 'b1'),
        ('executive', 'a1'),
        ['a1', 'b1', 'pres', 'sec', 'treas', 'vp']),
    ])
def test_replace_with_in(s, rl, l, expected):
    assert member.replace_with_in(s, rl, l) == expected

def test_keys_removed():
    assert helpers.keys_removed(d1, 'b') == expected


def test_names_reversed():
    name = 'James (Kirk) Kirkham'
    assert member.names_reversed(member.names_reversed(name)) == name


@pytest.mark.parametrize("record, expected", [
#({'first': 'Rick', 'last': 'Addicks', 'phone': '883-0365', 'address': '185 Caribe Isle', 'town': 'Novato', 'state': 'CA', 'postal_code': '94949', 'country': 'USA', 'email': 'mail@rickaddicks.com', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'Val', 'last': 'Agnoli', 'phone': '868-0553', 'address': 'PO Box 417', 'town': 'Stinson Beach', 'state': 'CA', 'postal_code': '94970', 'country': 'USA', 'email': 'val@agnoli.com', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'Christine', 'last': 'Airey', 'phone': '868-0512', 'address': 'PO Box 453', 'town': 'Stinson Beach', 'state': 'CA', 'postal_code': '94970', 'country': 'USA', 'email': '', 'dues': '-100', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
({'first': 'Chuck', 'last': 'Alexander', 'phone': '868-0428', 'address': 'PO Box 101', 'town': 'Bolinas', 'state': 'CA', 'postal_code': '94924', 'country': 'USA', 'email': 'chas-c@sbcglobal.net', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
    "Chuck Alexander  PO Box 101, Bolinas, CA 94924"),
#({'first': 'Thomas', 'last': 'Allen', 'phone': '415/990-0240', 'address': '1703 Madrona Ave.', 'town': 'St. Helena', 'state': 'CA', 'postal_code': '94574', 'country': 'USA', 'email': 'tallen@northbaymgt.com', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'John', 'last': 'Archibald', 'phone': '415/250-7915', 'address': 'PO Box 132', 'town': 'Stinson Beach', 'state': 'CA', 'postal_code': '9497', 'country': 'USA', 'email': 'jl_archibald@yahoo.com', 'dues': '100', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'Raymond', 'last': 'Bagley', 'phone': '415/522-2908', 'address': '211 Paloma Ave.', 'town': 'San Rafael', 'state': 'CA', 'postal_code': '94901', 'country': 'USA', 'email': '', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''}, 
#    ),
    ])
def test_fstrings_first_last_w_address_only(record, expected):
    assert member.fstrings[
            'first_last_w_address_only'].format(**record) ==expected


@pytest.mark.parametrize("record, expected", [
({'first': 'Chuck', 'last': 'Alexander', 'phone': '868-0428', 'address': 'PO Box 101', 'town': 'Bolinas', 'state': 'CA', 'postal_code': '94924', 'country': 'USA', 'email': 'chas-c@sbcglobal.net', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
    "Chuck Alexander [868-0428] PO Box 101, Bolinas, CA 94924 [chas-c@sbcglobal.net]"),
    ])
def test_fstrings_first_last_w_all_data(record, expected):
    assert member.fstrings[
            'first_last_w_all_data'].format(**record) == expected

            
@pytest.mark.parametrize("record, expected", [
#({'first': 'Rick', 'last': 'Addicks', 'phone': '883-0365', 'address': '185 Caribe Isle', 'town': 'Novato', 'state': 'CA', 'postal_code': '94949', 'country': 'USA', 'email': 'mail@rickaddicks.com', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'Val', 'last': 'Agnoli', 'phone': '868-0553', 'address': 'PO Box 417', 'town': 'Stinson Beach', 'state': 'CA', 'postal_code': '94970', 'country': 'USA', 'email': 'val@agnoli.com', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'Christine', 'last': 'Airey', 'phone': '868-0512', 'address': 'PO Box 453', 'town': 'Stinson Beach', 'state': 'CA', 'postal_code': '94970', 'country': 'USA', 'email': '', 'dues': '-100', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
({'first': 'Chuck', 'last': 'Alexander', 'phone': '868-0428', 'address': 'PO Box 101', 'town': 'Bolinas', 'state': 'CA', 'postal_code': '94924', 'country': 'USA', 'email': 'chas-c@sbcglobal.net', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
    "Alexander, Chuck  PO Box 101, Bolinas, CA 94924"),
#({'first': 'Thomas', 'last': 'Allen', 'phone': '415/990-0240', 'address': '1703 Madrona Ave.', 'town': 'St. Helena', 'state': 'CA', 'postal_code': '94574', 'country': 'USA', 'email': 'tallen@northbaymgt.com', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'John', 'last': 'Archibald', 'phone': '415/250-7915', 'address': 'PO Box 132', 'town': 'Stinson Beach', 'state': 'CA', 'postal_code': '9497', 'country': 'USA', 'email': 'jl_archibald@yahoo.com', 'dues': '100', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'Raymond', 'last': 'Bagley', 'phone': '415/522-2908', 'address': '211 Paloma Ave.', 'town': 'San Rafael', 'state': 'CA', 'postal_code': '94901', 'country': 'USA', 'email': '', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''}, 
#    ),
    ])
def test_fstrings_last_first_w_address_only(record, expected):
    assert member.fstrings[
            'last_first_w_address_only'].format(**record) ==expected


@pytest.mark.parametrize("record, expected", [
#({'first': 'Rick', 'last': 'Addicks', 'phone': '883-0365', 'address': '185 Caribe Isle', 'town': 'Novato', 'state': 'CA', 'postal_code': '94949', 'country': 'USA', 'email': 'mail@rickaddicks.com', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'Val', 'last': 'Agnoli', 'phone': '868-0553', 'address': 'PO Box 417', 'town': 'Stinson Beach', 'state': 'CA', 'postal_code': '94970', 'country': 'USA', 'email': 'val@agnoli.com', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'Christine', 'last': 'Airey', 'phone': '868-0512', 'address': 'PO Box 453', 'town': 'Stinson Beach', 'state': 'CA', 'postal_code': '94970', 'country': 'USA', 'email': '', 'dues': '-100', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
({'first': 'Chuck', 'last': 'Alexander', 'phone': '868-0428', 'address': 'PO Box 101', 'town': 'Bolinas', 'state': 'CA', 'postal_code': '94924', 'country': 'USA', 'email': 'chas-c@sbcglobal.net', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
    "Alexander, Chuck [868-0428] PO Box 101, Bolinas, CA 94924 [chas-c@sbcglobal.net]"),
#({'first': 'Thomas', 'last': 'Allen', 'phone': '415/990-0240', 'address': '1703 Madrona Ave.', 'town': 'St. Helena', 'state': 'CA', 'postal_code': '94574', 'country': 'USA', 'email': 'tallen@northbaymgt.com', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'John', 'last': 'Archibald', 'phone': '415/250-7915', 'address': 'PO Box 132', 'town': 'Stinson Beach', 'state': 'CA', 'postal_code': '9497', 'country': 'USA', 'email': 'jl_archibald@yahoo.com', 'dues': '100', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'Raymond', 'last': 'Bagley', 'phone': '415/522-2908', 'address': '211 Paloma Ave.', 'town': 'San Rafael', 'state': 'CA', 'postal_code': '94901', 'country': 'USA', 'email': '', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''}, 
#    ),
    ])
def test_fstrings_last_first_w_all_data(record, expected):
    assert member.fstrings[
            'last_first_w_all_data'].format(**record) ==expected


redacted = '''
#({'first': 'Rick', 'last': 'Addicks', 'phone': '883-0365', 'address': '185 Caribe Isle', 'town': 'Novato', 'state': 'CA', 'postal_code': '94949', 'country': 'USA', 'email': 'mail@rickaddicks.com', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'Val', 'last': 'Agnoli', 'phone': '868-0553', 'address': 'PO Box 417', 'town': 'Stinson Beach', 'state': 'CA', 'postal_code': '94970', 'country': 'USA', 'email': 'val@agnoli.com', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'Christine', 'last': 'Airey', 'phone': '868-0512', 'address': 'PO Box 453', 'town': 'Stinson Beach', 'state': 'CA', 'postal_code': '94970', 'country': 'USA', 'email': '', 'dues': '-100', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'Thomas', 'last': 'Allen', 'phone': '415/990-0240', 'address': '1703 Madrona Ave.', 'town': 'St. Helena', 'state': 'CA', 'postal_code': '94574', 'country': 'USA', 'email': 'tallen@northbaymgt.com', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'John', 'last': 'Archibald', 'phone': '415/250-7915', 'address': 'PO Box 132', 'town': 'Stinson Beach', 'state': 'CA', 'postal_code': '9497', 'country': 'USA', 'email': 'jl_archibald@yahoo.com', 'dues': '100', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''},
#    ),
#({'first': 'Raymond', 'last': 'Bagley', 'phone': '415/522-2908', 'address': '211 Paloma Ave.', 'town': 'San Rafael', 'state': 'CA', 'postal_code': '94901', 'country': 'USA', 'email': '', 'dues': '0', 'dock': '', 'kayak': '', 'mooring': '', 'status': ''}, 
#    ),
'''
