#!/usr/bin/env python3

# File: ck4fee_consistency.py

"""
developing data.ck4fee_consistency(contact_data,
                                    member_data,
                                    no_email_set):

"""

import data
import member
from rbc import Club

club = Club()

data.gather_contacts_data(club)
groups_by_name = club.groups_by_name
fee_paying_contacts = data.get_fee_paying_contacts(club)

data.gather_membership_data(club)
fee_paying_members = club.fee_category_by_m
no_email_recs = club.usps_only  # a list of records
no_email_set = {member.fstrings['key'].format(**rec)
                for rec in no_email_recs}
# fee_paying_w_email_set = fee_paying_m_set - no_email_set

def ck4fee_consistency(contact_data, # fee_paying_contacts
                        member_data, # club.fee_category_by_m
                        no_email_set):
    for name in contact_data.keys():
        contact_data[name] = frozenset(contact_data[name])
    contact_set = set([(name, value) for name, value in 
                            contact_data.items()])
    member_key_set = set(member_data.keys())
    keys2compare = member_key_set - no_email_set
    member_data2compare = {key: value for (key, value) in
            member_data.items() if key in keys2compare}
    for name in member_data2compare.keys():
        member_data2compare[name] = frozenset(
                member_data2compare[name].keys())
    member_set = set([(name, value) for name, value in
                            member_data2compare.items()])
    if member_set == contact_set:
        print("all is good")
    else:
        print("problems")
    pass
#   _ = input(repr(sorted(contact_set)))
#   _ = input(repr(sorted(member_data)))
#   _ = input(repr(sorted(member_key_set)))
#   _ = input(repr(sorted(keys2compare)))
#   _ = input(repr(sorted(no_email_set)))
#   _ = input(repr(member_set))

if __name__ == '__main__':
    ck4fee_consistency(fee_paying_contacts,
                        fee_paying_members,
                        no_email_set)

