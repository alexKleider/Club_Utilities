"""
t1:
    Tests data.get_applicant_data
    and   data.get_sponsor_data
t2:
    Uses helpers.compare_dicts
    and  helpers.display_mismatches
    to show discrepancies between member data base and gmail.
"""

import sys
import data
import rbc
import helpers
import member


def t1():
    print("\n Running 't1'")
    sponsor_data = data.get_sponsor_data(rbc.Club.SPONSORS_SPoT)
    applicant_data = data.get_applicant_data(rbc.Club.APPLICANT_SPoT,
                                             rbc.Club.SPONSORS_SPoT)
    print("Sponsor Data:")
    for key in sponsor_data.keys():
        print('{}: {}'
              .format(key, 
                      ', '.join(sponsor_data[key])))
    print()
    print("Applicant Data:")
    for key in applicant_data.keys():
        print("{}: {}".format(key, repr(applicant_data[key])))

def t2():
    print("\n Running 't2'")
    club = rbc.Club()
    club.no_email = []
    data.gather_membership_data(club)
    data.gather_contacts_data(club)
    #for item in club.__dict__: print(item)
    #_ = input("any key to continue ")


    m_gmail_mismatchs = helpers.compare_dicts(
                                club.db_emails,
                                club.gmail_by_name,
                                specified_value=member.NO_EMAIL_KEY)
    print("member data checked vs gmail contacts:")
    mismatches = helpers.display_mismatches(m_gmail_mismatchs,
                                    "Members without email:",
                                    True)
    if mismatches: print('\n'.join(mismatches))
    else: print("No irregularities")

    gmail_m_mismatchs = helpers.compare_dicts(
                                club.gmail_by_name,
                                club.db_emails)
    print("Gmail contacts checked vs member data:")
    mismatches = helpers.display_mismatches(gmail_m_mismatchs)
    if mismatches: print('\n'.join(mismatches))
    else: print("No irregularities")

if __name__ == '__main__':
    t1()
    print()
    t2()

