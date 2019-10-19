#!/usr/bin/env python

# File: rewrite_db.py

"""
Traverses a csv file and applies one or more functions tranforming
it into another csv file. Two file names must be specified- an in
and an out put file.
Used Sept 28th, 2019 to reinstall the dues/fees owed for the upcoming
year and at the same time put the extra fees categories into
alphabetical order.
(Data/memlist.csv was backed up and then replaced with new
version.)
"""

import csv
import utils
import member
import extra_fees

in_file = "Temp/in.csv"
out_file = "Temp/out.csv"

new_fieldnames = [  # BE CAREFUL WHEN CHANGING FIELD NAMES
    # Move extra fees into sorted order.
    # Used in conjunction with move_fields2new_record()
    "first", "last", "phone", "address", "town",
    "state", "postal_code", "country", "email", "email_only",
    "dues", "dock", "kayak", "mooring", "status"]


def move_fields2new_record(record, new_record, **kwargs):
    """
    Must preceed all the other functions that can be called
    by rewrite() if data is to be preserved.
    """
    for key in record:
        new_record[key] = record[key]


def restore_dues_and_fees(record, new_record, **kwargs):
    """
    The **kwargs is the by_name dict part of what is returned
    by extra_fees.gather_extra_fees_data(infile).
    Must be preceded by move_fields2new_record.
    """
    if not member.is_fee_paying_member(record):
        return
    # first deal with dues:
    if not record["dues"]:
        new_record["dues"] = utils.Membership.YEARLY_DUES
    else:
        new_record["dues"] = (int(record["dues"]) +
                        utils.Membership.YEARLY_DUES)
    # now deal with fee:
    name_key = "{last}, {first}".format(**record)
    if name_key in kwargs:
#       print("Found {}".format(name_key))
        for value in kwargs[name_key]:
            key = value[0].lower()
            new_record[key] = value[1]
#           print(key, value[1])



def rewrite(in_file, out_file, methods,
                    args={}, new_fieldnames=None):
    with open(in_file, 'r') as ifile:
        dict_reader = csv.DictReader(ifile)
        if not new_fieldnames:
            new_fieldnames = dict_reader.fieldnames
        with open(out_file, 'w', newline='') as ofile:
            dict_writer = csv.DictWriter(ofile, fieldnames=new_fieldnames)
            dict_writer.writeheader()
            for record in dict_reader:
                new_record = {}
                for method in methods:
                    method(record, new_record, **args)
                dict_writer.writerow(new_record)


if __name__ == "__main__":
    extra_fees_file = "Data/extra_fees.txt"
    args = extra_fees.gather_extra_fees_data(extra_fees_file)[
            "by_name"]
    methods = [move_fields2new_record, restore_dues_and_fees, ]
    rewrite(in_file, out_file, methods, 
        args=args,
        new_fieldnames=new_fieldnames)

