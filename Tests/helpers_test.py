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


@pytest.mark.parametrize("test_input,expected", [
    (-50,             "-$50.00"),
    ( 48932.0451,      "$48,932.05"),
    (-93448932.0451,  "-$93,448,932.05"),
    ( 93448932.0451,   "$93,448,932.05"),
    ( -3,             "-$3.00"),
    ])
def test_format_dollar_value(test_input, expected):
    assert helpers.format_dollar_value(test_input) == expected


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
    ])
def test_expand_date(date_string, expected):
    assert helpers.expand_date(date_string) == expected


def test_get_datestamp_w_valid_dates():
    pass


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


