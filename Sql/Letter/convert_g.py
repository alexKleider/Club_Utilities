#!/usr/bin/env python3

# File: convert_g.py

"""
Convert a google contacts csv file into my csv format.
"""

import csv

output_csv = "Data/my_google.csv"
google_csv = 'Data/google.csv'

my_fields = ("prefix","first","initial","last","suffix","company",
            "phone","address","address1","town","state",
            "postal_code","country","email","extra",)

corresponding_fields = (
    ('Given Name',              'first'),
    ('Additional Name',         'middle'),
    ('Family Name',             'last'),
    ('Name Prefix',             'prefix'),
    ('Name Suffix',             'suffix'),

    ('Address 1 - Street',      'address'),
    ('Address 1 - City',        'town'),
    ('Address 1 - PO Box',      'address1'),
    ('Address 1 - Region',      'state'),
    ('Address 1 - Postal Code', 'postal_code'),
    ('Address 1 - Country',     'country'),

    ('Organization 1 - Name',   'company'),
    )
phone_fields = (
    'Phone 1 - Value', 'Phone 1 - Type',
    'Phone 2 - Value', 'Phone 2 - Type',
    'Phone 3 - Value', 'Phone 3 - Type',
    )
email_fields = ('E-mail 1 - Value', 'E-mail 2 - Value') 


def complete_record(collected_fields):
    ret = {}
    collected_keys = collected_fields.keys()
    for key in my_fields:
        if key in collected_keys:
            ret[key] = collected_fields[key]
        else:
            ret[key] = ''
    return ret


def converted_contacts(google_csv):
    with open(google_csv, 'r', newline='') as instream:
        reader = csv.DictReader(instream)
        fieldnames = reader.fieldnames
        for row in reader:
            keep = False
            new_record = {}
            for g, m in corresponding_fields:
                if row[g]:
                    new_record[m] = row[g]
            myphone_field = []
            for n in (1,2,3):
                p_key = 'Phone {} - Value'.format(n)
                t_key = 'Phone {} - Type'.format(n)
                if row[p_key]:
                    phone_number = row[p_key]
                    phone_number = (phone_number +
                    '({})'.format(row[t_key]))
                    myphone_field.append(phone_number)
            new_record['phone'] = ' '.join(myphone_field)
            email_field = []
            for n in (1,2):
                e_key = 'E-mail {} - Value'.format(n)
                if row[e_key]:
                    email_field.append(row[e_key].strip())
            new_record['email'] = ' '.join(email_field)
            yield complete_record(new_record)



def main():
    with open(output_csv, 'w', newline='') as outstream:
        writer = csv.DictWriter(outstream,
                fieldnames=my_fields,
          lineterminator='\n')

        writer.writeheader()
        for new_record in converted_contacts(google_csv):
#           _ = input(new_record)
            if new_record["address"]:
                writer.writerow(new_record)

if __name__ == '__main__':
    main()
