#!/usr/bin/env python

# File: mailings.py

"""
Provides a list of one dictionary ('mailings') to serve in
testing and as a template for real use.
"""

body_0 = """
This is a test using Reply-To: gmail.
Here's hoping it goes well.
Goog luck.
"""

mailings = [
    {
    'From': 'alex@kleider.ca',
    'reply-to': 'alexkleider@gmail.com',
    'To': ['akleider@sonic.net'],
    'Subject': 'TEST Reply-To',
    'attachments': ['notes',],
    'body': body_0,
    },
]
