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
import utils
import data
import rbc

EXCLUDED_STATI = {'m', 'zae'}

club = rbc.Club()
applicant_data = data.get_applicant_data(club.APPLICANT_SPoT,
                                         club.SPONSORS_SPoT)
applicant_keys = sorted(applicant_data.keys())
#print("\nApplicant Data")
#for key in applicant_data.keys():
#    print("{}: {}\n".format(key, applicant_data[key]))
#sys.exit()


with open(club.APPLICANT_CSV, 'w', newline='') as fileobj:
    dict_writer = csv.DictWriter(fileobj,
                                 rbc.Club.APPLICANT_DATA_FIELD_NAMES, 
                                 dialect='unix',
                                 quoting=csv.QUOTE_MINIMAL)
    dict_writer.writeheader()
    for key in applicant_keys:
        if not applicant_data[key]['status'] in EXCLUDED_STATI:
            dict_writer.writerow(applicant_data[key])

