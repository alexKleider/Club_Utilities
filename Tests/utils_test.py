#!/usr/bin/env python3

# File: Tests/utils_test.py

"""
Have so far written tests for:
    join2set
    replace_with_in
"""

# Must first add the parent directory of the
# currently running script to the system path:
import os
import sys
sys.path.insert(0, os.path.split(sys.path[0])[0])
# print(sys.path)
# ... or alternatively set PYTHONPATH to project directory:
# export PYTHONPATH=/home/alex/Git/Club/Utils

import utils
import pytest


redacted = '''
@pytest.mark.parametrize("params, expected", [
    (('a1|exec', 'sec', '', None), {'a1', 'exec', 'sec'}
        ),
    ])
def test_join2set(params, expected):
    assert utils.join2set(*params) == expected
'''

