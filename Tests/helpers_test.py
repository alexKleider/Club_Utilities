#!/usr/bin/env python3

# File: Tests/helpers_test.py

"""
import addparent
addparent.add2path()
import sys
print(sys.path)
"""
#import os
#import sys
#sys.path.insert(0, os.path.split(sys.path[0])[0])
#print(sys.path)

import pytest
import helpers
import datetime



s0 = ''
s1 = "alex@kleider.ca"
s2 = 'alexkleider@gmail.com,akleider@sonic.net,alexkleider@gmail.com,alex@kleider.ca'
s3 = 'alexkleider@protonmail.com'
s4 = 'sponsor'
res = "akleider@sonic.net,alex@kleider.ca,alexkleider@gmail.com,alexkleider@protonmail.com"

def test_join_email_listings():
    assert helpers.join_email_listings(s0, s1, s2, s3) == res


def test_script_location():
    assert helpers.script_location() == (
    "/home/alex/Git/Club/Utils"
    )


stream = [
    "The quick brown fox",
    "   jumped over the moon",
    "    "
    "# but of course this is rediculous!",
    " # as is this.",
    "        indented => unindented line",
    ]


def test_useful_lines():
    expected = [
    "The quick brown fox",
    "jumped over the moon",
    "# but of course this is rediculous!",
    "# as is this.",
    "indented => unindented line",
        ]
    assert [line for line in helpers.useful_lines(
            stream, comment='')] == expected


def test_useful_lines_without_comments():
    expected = [
    "The quick brown fox",
    "jumped over the moon",
    "indented => unindented line",
        ]
    assert [line for line in helpers.useful_lines(
            stream, comment='#')
            ] == expected


@pytest.mark.parametrize("date_object, expected", [
    (datetime.date(2021, 1, 1), datetime.date(2021, 1, 1)),
    (datetime.date(2019, 1, 6), datetime.date(2019, 1, 4)),
    (datetime.date(2019, 1, 9), datetime.date(2019, 1, 4)),
    (datetime.date(2019, 2, 28), datetime.date(2019, 2, 1)),
    (datetime.date(2019, 11, 11), datetime.date(2019, 11, 1)),
    (datetime.date(2019, 12, 31), datetime.date(2019, 12, 6)),
    (datetime.date(2021, 8, 8), datetime.date(2021, 8, 6)),
    (datetime.date(2021, 9, 9), datetime.date(2021, 9, 3)),
    (datetime.date(2021, 1, 10), datetime.date(2021, 1, 1)),
    (None, helpers.get_first_friday_of_month()),
    ])
def test_get_first_friday_of_month(date_object, expected):
    assert helpers.get_first_friday_of_month(date_object) == expected


@pytest.mark.parametrize("date_object, exclude, expected", [
    (datetime.date(2020, 12, 26), False,
            datetime.date(2021, 1, 1).strftime(
                helpers.date_w_wk_day_template)),
    (datetime.date(2020, 12, 26), True,
            datetime.date(2021, 1, 8).strftime(
                helpers.date_w_wk_day_template)),
    (datetime.date(2021, 1, 3), True,
            datetime.date(2021, 1, 8).strftime(
                helpers.date_w_wk_day_template)),
    (datetime.date(2021, 1, 8), True,
            datetime.date(2021, 1, 8).strftime(
                helpers.date_w_wk_day_template)),
    (datetime.date(2021, 1, 9), True,
            datetime.date(2021, 2, 5).strftime(
                helpers.date_w_wk_day_template)),
    (datetime.date(2021, 6, 20), True,
            datetime.date(2021, 7, 2).strftime(
                helpers.date_w_wk_day_template)),
    ])
def test_next_first_friday(date_object, exclude, expected):
    assert helpers.next_first_friday(
                today=date_object, exclude=exclude) == expected


@pytest.mark.parametrize("which, now, expected", [
    ("last", datetime.date(year=2020, month=4, day=3), "2018-2019"),
    ("this", datetime.date(year=2020, month=4, day=3), "2019-2020"),
    ("next", datetime.date(year=2020, month=4, day=3), "2020-2021"),
    ("last", datetime.date(year=2020, month=8, day=3), "2019-2020"),
    ("this", datetime.date(year=2020, month=8, day=3), "2020-2021"),
    ("next", datetime.date(year=2020, month=8, day=3), "2021-2022"),
    ])
def test_club_year(which, now, expected):
    assert helpers.club_year(which, now) == expected


@pytest.mark.parametrize("date_string, expected", [
    ("200606", "2020-06-06"),
    ("20200606", "2020-06-06"),
    ("210606", "2021-06-06"),
    ("20210606", "2021-06-06"),
    ("201206", "2020-12-06"),
    ("20201206", "2020-12-06"),
    ("210606", "2021-06-06"),
    ("20210606", "2021-06-06"),
    ('201225', '2020-12-25'),
    ('210703', '2021-07-03'),
    ('220101', '2022-01-01'),
    ])
def test_expand_date(date_string, expected):
    assert helpers.expand_date(date_string) == expected

@pytest.mark.parametrize("date_obj, expected", [
    (datetime.date(1945, 7, 3), 'Jul 03, 1945'),
    (datetime.date(1943, 7, 15), 'Jul 15, 1943'),
    ])
def test_get_datestamp_w_valid_datetime_params(date_obj, expected):
    assert helpers.get_datestamp(date_obj) == expected


def test_get_datestamp_fails_if_invalid_parameter_provided():
    try:
        helpers.get_datestamp("Jan 21, 2021")
    except SystemExit:
        assert True
    else:
        assert False


def test_get_datestamp_accepts_datetimedatetime():
    try:
        helpers.get_datestamp(datetime.datetime.today())
    except SystemExit:
        assert False
    else:
        assert True


def test_get_datestamp_accepts_datetimedate():
    try:
        helpers.get_datestamp(datetime.date.today())
    except SystemExit:
        assert False
    else:
        assert True


@pytest.mark.parametrize("test_input,expected", [
    (-50,             "-$50.00"),
    ( 48932.0451,      "$48,932.05"),
    (-93448932.0451,  "-$93,448,932.05"),
    ( 93448932.0451,   "$93,448,932.05"),
    ( -3,             "-$3.00"),
    ])
def test_format_dollar_value(test_input, expected):
    assert helpers.format_dollar_value(test_input) == expected


@pytest.mark.parametrize("text, n_spaces, expected", [
    ("Jane Doe\n101 First St.\nAnyTown, USA",5,
     "     Jane Doe\n     101 First St.\n     AnyTown, USA"),
    (["Jane Doe", "101 First St.", "AnyTown, USA"] ,5,
     "     Jane Doe\n     101 First St.\n     AnyTown, USA"),
    ])
def test_indent(text, n_spaces, expected):
    assert helpers.indent(text, n_spaces) == expected


@pytest.mark.parametrize("content, n, expected", [
    (["Jane Doe", "101 First St.", "AnyTown, USA"], 3,
     ["Jane Doe", "101 First St.", "AnyTown, USA"]),
    (["Jane Doe", "101 First St.", "AnyTown, USA"], 4,
     ["Jane Doe", "101 First St.", "AnyTown, USA", ""]),
    (["Jane Doe", "101 First St.", "AnyTown, USA"], 5,
     ["", "Jane Doe", "101 First St.", "AnyTown, USA", ""]),
    (["Jane Doe", "101 First St.", "AnyTown, USA"], 6,
     ["", "Jane Doe", "101 First St.", "AnyTown, USA", "", ""]),
    ])
def test_expand_array(content, n, expected):
    assert helpers.expand_array(content, n) == expected


@pytest.mark.parametrize("content, n, expected", [
    ("Jane Doe\n101 First St.\nAnyTown, USA", 3,
     "Jane Doe\n101 First St.\nAnyTown, USA"),
    ("Jane Doe\n101 First St.\nAnyTown, USA\n", 4,
     "Jane Doe\n101 First St.\nAnyTown, USA\n"),
    ("Jane Doe\n101 First St.\nAnyTown, USA", 5,
     "\nJane Doe\n101 First St.\nAnyTown, USA\n"),
    ("Jane Doe\n101 First St.\nAnyTown, USA", 6,
     "\nJane Doe\n101 First St.\nAnyTown, USA\n\n"),
    ])
def test_expand_string(content, n, expected):
    assert helpers.expand_string(content, n) == expected


@pytest.mark.parametrize("content, n, expected", [
    (["Jane Doe", "101 First St.", "AnyTown, USA"], 3,
     ["Jane Doe", "101 First St.", "AnyTown, USA"]),
    (["Jane Doe", "101 First St.", "AnyTown, USA"], 4,
     ["Jane Doe", "101 First St.", "AnyTown, USA", ""]),
    (["Jane Doe", "101 First St.", "AnyTown, USA"], 5,
     ["", "Jane Doe", "101 First St.", "AnyTown, USA", ""]),
    (["Jane Doe", "101 First St.", "AnyTown, USA"], 6,
     ["", "Jane Doe", "101 First St.", "AnyTown, USA", "", ""]),
    ("Jane Doe\n101 First St.\nAnyTown, USA", 3,
     "Jane Doe\n101 First St.\nAnyTown, USA"),
    ("Jane Doe\n101 First St.\nAnyTown, USA\n", 4,
     "Jane Doe\n101 First St.\nAnyTown, USA\n"),
    ("Jane Doe\n101 First St.\nAnyTown, USA", 5,
     "\nJane Doe\n101 First St.\nAnyTown, USA\n"),
    ("Jane Doe\n101 First St.\nAnyTown, USA", 6,
     "\nJane Doe\n101 First St.\nAnyTown, USA\n\n"),
    ])
def test_expand(content, n, expected):
    assert helpers.expand(content, n) == expected


indented = "     Jane Doe\n     101 First St.\n     AnyTown, USA"
@pytest.mark.parametrize ("source, indent_n, expected", [
    ("Jane Doe\n101 First St.\nAnyTown, USA", 5,
        indented),
    (["Jane Doe", "101 First St.", "AnyTown, USA"] ,5,
        indented),
    ])
def test_indent(source, indent_n, expected):
    assert helpers.indent(source, indent_n) == expected


def test_get_datestamp():
    b_day = datetime.date(year=1945, month=7, day=3)
    stamp = helpers.get_datestamp(b_day)
    assert stamp == 'Jul 03, 1945'
    assert helpers.get_datestamp(
        datetime.date(1945, 7, 3)) == stamp

    date_obj = datetime.date(1945, 7, 3)
    expected = 'Jul 03, 1945'
    assert helpers.get_datestamp(date_obj) == expected


@pytest.mark.parametrize("source, expected", [
    ("sponsors", (True, [])),
    ('alex@kleider.ca,sponsors', (True, ['alex@kleider.ca'])),
    ('alex@kleider.ca,akleider@sonic.net',
        (False, ['alex@kleider.ca', 'akleider@sonic.net']))
    ])
def test_clarify__cc_wo_keyword(source, expected):
    assert helpers.clarify_cc(source) == expected


@pytest.mark.parametrize("source, keyword, expected", [
    ("sponsors", "sponsors", (True, [])),
    ('alex@kleider.ca,sponsors', "sponsors", (True, ['alex@kleider.ca'])),
    ('alex@kleider.ca,akleider@sonic.net', 'sponsors',
        (False, ['alex@kleider.ca', 'akleider@sonic.net']))
    ])
def test_clarify__cc_w_keyword(source, keyword, expected):
    assert helpers.clarify_cc(source, keyword) == expected


@pytest.mark.parametrize("source, expected", [
    ("Alex Kleider", "Kleider, Alex"),
    ("Kleider, Alex", "Alex Kleider"),
    ])
def test_tofro_first_last(source, expected):
    assert helpers.tofro_first_last(source) == expected


