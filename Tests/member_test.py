#!/usr/bin/env python3
# File: Tests/member_test.py

# Must first add the parent directory of the
# currently running script to the system path:
import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])

import pytest
import member

d1 = {'a': [1,2,3,4],
      'b': {1,2,3,4},
      'c': 'a string',
     }
expected = {'a': [1,2,3,4],
            'c': 'a string',
           }


def test_keys_removed():
    assert member.keys_removed(d1, 'b') == expected

