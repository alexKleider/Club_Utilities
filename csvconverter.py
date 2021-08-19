#!/usr/bin/env python3

# File: csvconverter.py

"""
Uses the Bolinas Rod and Boat Club applicant files,
specifically Data/applicants.txt 
and Data/sponsors.txt, and
converts the information into a csv file
(for the benefit of future excel loving officials.)
"""

import sys
import csv
import helpers
import data
import rbc

EXCLUDED_STATI = {'m', 'zae'}


def filtered_data(a_dict_w_dict_values,
               test_key, excluded):
    for key in a_dict_w_dict_values.keys():
        if not a_dict_w_dict_values[key][test_key] in excluded:
            yield a_dict_w_dict_values[key]


club = rbc.Club()
applicant_data = data.get_applicant_data(club.APPLICANT_SPoT,
                                         club.SPONSORS_SPoT)
applicant_keys = sorted(applicant_data.keys())

helpers.save_db(filtered_data(applicant_data,
                              'status',
                              EXCLUDED_STATI,
                              ),
                club.APPLICANT_CSV,
                club. APPLICANT_DATA_FIELD_NAMES,  #
                report='applicants in csv format')

