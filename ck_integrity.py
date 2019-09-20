#!/usr/bin/env python3

# File: ck_integrity.py  (expect to merge into utils.py)

import member

def ck_integrity(club, member_csv_file, contacts_csv):
    """
    Assume the client has called:
        club = Membership(Dummy)
    Working on a function that will check the integrity of the Club's
    data base(s.)  It will combine the ck_fields and compare_gmail
    commands and also possibly check for consistency with the
    'extra_fees'/'extra_charges', 'stati', ... etc categories.
    """
    # Set up collectors by name and by email each
    # for gmail and for memlist db.
    # 'names' will be (last, first) tuples.
    club.g_by_name = dict()    # gmail contacts keyed by name
    club.g_by_email = dict()   # gmail contacts keyed by email
    club.m_by_name = dict()    # member emails keyed by name
    club.m_by_email = dict()   # member names keyed by email
    club.m_by_status = dict()  # member names keyed by status 
    club.malformed = []
    if member.traverse_records(member_csv_file,
        (member.add2m_by_name, member.add2m_by_email,
        member.add2malformed, member.add2mem_by_status),
        club):
        print("Error condition! #{}".format(err_code))
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

def get2dicts_from_gmail_contacts(contacts, club):
    """
    """
    # Traverse contacts.csv => g_dict_e and g_dict_n
    with open(contacts, 'r', encoding='utf-8') as file_obj:
        google_reader = csv.DictReader(file_obj, restkey='status')
        print('DictReading Google contacts file "{}".'
            .format(fileobj.name))
        for g_rec in google_reader:
            contact_email = g_rec["E-mail 1 - Value"]
            first_name = " ".join((
                g_rec["Given Name"],
                g_rec["Additional Name"],
                )).strip()
            last_name = " ".join((
                g_rec["Family Name"],
                g_rec["Name Suffix"],
                )).strip()

            key = contact_email
            g_dict_e[key] = (
                first_name,
                last_name,
                g_rec["Group Membership"],  # ?for future use?
                )
            
            key = (first_name, last_name,)
            g_dict_n[key] = contact_email
            key = (first_name, last_name,)
            g_dict_n[key] = contact_email
    # We now have two dicts: g_dict_e & g_dict_n
    # One keyed by email: values can be indexed as follows:
    #     [0] => first name
    #     [1] => last name
    #     [2] => colon separated list of groups
    # The other keyed by name tuple: value is email
    return ... 
