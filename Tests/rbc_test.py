#!/usr/bin/env python3

# File: Tests/utils.py


import pytest
import rbc

def test_club_init():
    club = rbc.Club()
    with pytest.raises(NotImplementedError):
        club1 = rbc.Club()

