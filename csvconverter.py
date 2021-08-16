#!/usr/bin/env python3

# File: csvconverter.py

"""
Uses the Bolinas Rod and Boat Club applicant files,
specifically Data/applicants.txt 
and Data/sponsors.txt, and
converts the information into a csv file
(for the benefit of future excel loving officials.)
"""

import csv
import utils
import data
import rbc

club = rbc.Club()
sponsor_data = data.get_sponsor_data(club.SPONSORS_SPoT)
sponsor_keys = sorted(sponsor_data.keys())
applicant_data = data.get_applicant_data(
    club.APPLICANT_SPoT, all_dates=True)
applicant_keys = sorted(applicant_data.keys())
print("\nSponsor Data")
for key in sponsor_data.keys():
    print("{}: {}".format(key, sponsor_data[key]))
# print(sponsor_data)
print("\nApplicant Data")
for key in applicant_data.keys():
    print("{}: {}".format(key, applicant_data[key]))
# print(applicant_data)
applicant_data_lines = []
for key in applicant_keys:
    csv_line = []
    names = key.split(', ')
    csv_line.append(names[1])
    csv_line.append(names[0])
    csv_line.append(applicant_data[key]['status'])
#   print("possible keys are ", applicant_data[key].keys())
    if 'dates' in applicant_data[key].keys():
        for date in applicant_data[key]['dates']:
            csv_line.append(date)
    while len(csv_line) < 8:
        csv_line.append('')
    if key in sponsor_keys:
        csv_line.extend(list(sponsor_data[key]))
    applicant_data_lines.append(csv_line)

response = input(
        "Include all data? (vs only current applicants.) (Y/N)")

applicant_data_field_names = ("first", "last", "status", 
    "First", "Second", "Third", "ApprovalDate", "DateDuesPaid",
    "Sponsor1", "Sponsor2",)

with open(club.APPLICANT_CSV, 'w', newline='') as fileobj:
    writer = csv.writer(fileobj,
            dialect='unix', quoting=csv.QUOTE_NONE)
    writer.writerow(applicant_data_field_names)
    for line in applicant_data_lines:
        if response and response[0] in {'y', 'Y'}:
            writer.writerow(line)
        else:
            if line[2] != 'm':
                writer.writerow(line)
print("\nApplicant_data:")
print(applicant_data_field_names)
for line in applicant_data_lines:
    if response and response[0] in {'y', 'Y'}:
        print(line)
    else:
        if line[2] != 'm':
            print(line)

