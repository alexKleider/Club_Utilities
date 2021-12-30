#!/usr/bin/env python3

# File: setup.py

from setuptools import setup

setup(
    name='utils',
    entry_points={
        'console_scripts':[
            'utils = utils:main',
        ],
    }
)


