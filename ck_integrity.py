#!/usr/bin/env python3

# File: ck_integrity.py  (expect to merge into utils.py)

import member

def gather_contacts_info(contacts, club):
    """
    Gathers up the info we want from a gmail contacts.csv file.
    Sets up three dict attributes of the utils.Membership instance
    specified by club and then populates them by reading the gmail
    contacts csv file:
        g_by_name is keyed by (last, first) name tuple /w values
        indexed as follows:
          [0] => email
          [1] => set of group memberships
        g_by_email is keyed by email /w values indexed as follows:
          [0] => last name
          [1] => first name
        g_by_group_membership is keyed by group membership /w values being lists
        of contacts sharing that group membership.
    """
    club.g_by_name = dict()
    club.g_by_email = dict()
    club.g_by_group_membership = dict()

    # Traverse contacts.csv => g_by_email and g_by_name
    with open(contacts, 'r', encoding='utf-8') as file_obj:
#       google_reader = csv.DictReader(file_obj, restkey='status')
        google_reader = csv.DictReader(file_obj)
        print('DictReading Google contacts file "{}".'
            .format(fileobj.name))
        for g_rec in google_reader:
            contact_email = g_rec["E-mail 1 - Value"]
            group_membership = (
                g_rec["Group Membership"].split(" ::: "))
            if (group_membership
            and group_membership[-1] =='* myContacts'):
                group_membership = group_membership[:-1]
            group_membership = {group for group in group_membership}
            first_name = " ".join((
                g_rec["Given Name"],
                g_rec["Additional Name"],
                )).strip()
            last_name = " ".join((
                g_rec["Family Name"],
                g_rec["Name Suffix"],
                )).strip()
            name_tuple = (last_name, first_name)

            key = contact_email
            club.g_by_email[key] = name_tuple
            key = name_tuple
            club.g_by_name[key] = (contact_email, group_membership)

            for key in group_membership:
                _ = club.g_by_group_membership.setdefault(key, [])
                club.g_by_group_membership[key].append(name_tuple)

def gather_membership_info(club, member_csv_file):
    """
    Gathers the info we want from the membership csv file.
    Sets up three dict and one list attributes of the utils.Membershp
    instance specified by club and then populates them by reading the
    member_csv_file:
        m_by_name is keyed by (last, first) name tuple /w emails as
        values.
        m_by_email is keyed by email /w (last, first) name tuple as
        value.
        m_by_status is keyed by status /w a list (of (last, first)
        name tuples as values.
        malformed is a list of (last, first) name tuples identifying
        members whose record seems to be malformed (or out of order.)
    """
    club.m_by_name = dict()    #{ member emails keyed by (first, last)
                               #{ name tuple
    club.m_by_email = dict()   # member names keyed by email
    club.m_by_status = dict()  # member names keyed by status 
    club.malformed = []
    err_code = member.traverse_records(member_csv_file,
        (member.add2m_by_name, member.add2m_by_email,
        member.add2m_by_status, member.add2malformed),
        club)
    if err_code:
        print("Error condition! #{}".format(err_code))


def ck_integrity(club, member_csv_file, contacts_csv_file):
    """
    Assume the client has called:
        club = Membership(Dummy)
    Working on a function that will check the integrity of the Club's
    data base(s.)  It will combine the ck_fields and compare_gmail
    commands and also possibly check for consistency with the
    'extra_fees'/'extra_charges', 'stati', ... etc categories.
    """
    gather_contacts_info(contacts_csv_file, club)
    gather_membership_info(member_csv_file, club)
    ret = []
    # First check for malformed records:
    if not club.malformed:
        ret.append("No malformed records found.")
    else:
        if not args['--raw']:
            ret = [
                'Malformed Records',
                '================='] + club.malformed
    if args["-S"]:
        ret.extend(["", "Members /w 'status' Content",
                       '---------------------------']
                       + club.status_list)
    """
    output("\n".join(ret))
    if args['-o']:
        print("Output sent to {}.".format(args['-o']))
    print("...done checking fields.")
    """

