#!/usr/bin/env python3

# File: ck_data.py

"""
# This file began as a copy of the data.ck_data() function.

# A work in progress:
#  Goal is to clarify the data.ck_data() code.
#  'data.ck_data()' is 280 lines long and somewhat confusing
#  to say the least!  I'm hoping to replace it, perhaps with
#  a number of different functions.
"""

import os
import sys
import csv
import sys_globals as glbs
import helpers
import member
from rbc import Club


def get_applicants_by_status(club):
    """
    # only used by ck_data which we are trying to rewrite #
    Uses the <club> attribute <applicant_data> to return
    a dict keyed by status;
    Values are each a list of applicant ('last, first') names.
    Note: club.applicant_data is derived from the applicant.txt
    file. It is also possible to get applicant data directly
    from the main data => club.db_applicants.
    Implement use of club.current
    """
    ret = {}
    for name in club.applicant_data.keys():
        status = club.applicant_data[name]['status']
        _ = ret.setdefault(status, [])
        ret[status].append(name)
    return ret



def add_sponsors(rec, sponsors):
    """
    # used by populate_applicant_data #
    Returns a record with sponsor fields added.
    """
    first_last = [member.names_reversed(sponsor) for sponsor in
            sponsors]
    ret = helpers.Rec(rec)
    ret['sponsor1'] = first_last[0]
    ret['sponsor2'] = first_last[1]
    return ret


def move_date_listing_into_record(dates, record):
    """
    # used by applicant_data_line2record #
    <dates>: a listing (possibly incomplete) of relevant dates.
    <record>: a dict to which to add those dates by relevant key.
    returns the record
    """
    for key, index in (('app_rcvd',  0),
                       ('fee_rcvd',  1),
                       ('1st',       2),
                       ('2nd',       3),
                       ('3rd',       4),
                       ('inducted',  5),
                       ('dues_paid', 6)):
        try:
            record[key] = dates[index]
        except IndexError:
            record[key] = ''
            continue
    return record


def applicant_data_line2record(line):
    """
    # used only by populate_applicant_data #
    Assumes a valid line from the Data/applicant.txt file.
    Returns a dict with keys as listed in 
    Club.APPLICANT_DATA_FIELD_NAMES = (
        "first", "last", "status",
        "app_rcvd", "fee_rcvd",   #} date (or empty
        "1st", "2nd", "3rd",      #} string if event
        "inducted", "dues_paid",  #} hasn't happened.
        "sponsor1", "sponsor2",   # empty strings if not available
        )
    Note: terminates program if no dates are provided.
    """
    ret = {}
    for key in Club.APPLICANT_DATA_FIELD_NAMES:
        ret[key] = ''
    parts = line.split(glbs.SEPARATOR)
    while not parts[-1]:  # lose trailing empty fields
        parts = parts[:-1]
    parts = [part.strip() for part in parts]
    names = parts[0].split()
#   key = "{}, {}".format(names[1], names[0]) 
#   print(names)
    ret['first'] = names[0]
    ret['last'] = names[1]
    dates = parts[1:]
    l = len(dates)
    if parts[-1].startswith("Appl"):
        dates = dates[:-1]  # waste the text
        special_status = "zae"  # see members.STATUS_KEY_VALUES
        l -= 1
    elif parts[-1].startswith("w"):
        dates = dates[:-1]
        special_status = "aw"
        l -= 1
    else:
        special_status = ''
    if l == 0:       # Should never have an entry /w no dates.
        print("Entry for applicant {}{} is without any dates."
                .format(names[0], names[1]))
        sys.exit()
    elif l == 1:               # one date listed
        status = "a-"
    elif l == 2:
        status = "a0"
    elif l == 3:
        status = "a1"
    elif l == 4:
        status = "a2"
    elif l == 5:
        status = "a3"
    elif l == 6:
        status = "ad"
    elif l == 7:
        status = "m"
    else:
        print("Entry for {}{} has an invalid number of dates."
                .format(names[0], names[1]))
        sys.exit()
    move_date_listing_into_record(dates, ret)
    if special_status:
        ret['status'] = special_status
    else:
        ret['status'] = status
    return ret



def populate_applicant_data(club):
    """
    # used by new code as well as ck_data #
    Reads applicant data file populating two attributes:
    1. club.applicant_data: a dict with keys == applicants
        and each value is a record with fields as listed in
        rbc.Club.APPLICANT_DATA_FIELD_NAMES.
    2. club.applicant_data_keys
    Note: Sponsor data is included if populate_sponsor_data has
    already been run, othwise, the values remain as empty strings.
    """
    sponsors = hasattr(club, 'sponsors_by_applicant')
    # ... populate_sponsor_data must have been run
    if sponsors:
        sponsored = club.sponsors_by_applicant.keys()
    club.applicant_data = {}
    with open(club.applicant_spot, 'r') as stream:
        if not club.quiet:
            print('Reading file "{}"...'.format(stream.name))
        for line in helpers.useful_lines(stream, comment='#'):
            rec = applicant_data_line2record(line)
            name_key = member.fstrings['key'].format(**rec)
            if sponsors and name_key in sponsored:
                rec = add_sponsors(rec,
                        club.sponsors_by_applicant[name_key])
            club.applicant_data[name_key] = rec
        club.applicant_data_keys = club.applicant_data.keys()



def parse_sponsor_data_line(line):
    """
    # used by populate_sponsor_data #
    Assumes blank and commented lines have already been removed.
    returns a 2 tuple: (for subsequent use as a key/value pair)
    t1 is "last,first" of applicant (can be used as a key)
    t2 is a tuple of sponsors ('first last')
    eg: ('Catz,John', ('Joe Shmo', 'Tom Duley'))
    Fails if encounters an invalid line!!!
    """
    parts = line.split(":")
    sponsored = parts[0].strip()
    names = sponsored.split()
    name = '{},{}'.format(names[1], names[0])
    part2 = parts[1]
    sponsors = (parts[1].split(', '))
    sponsors = tuple([sponsor.strip() for sponsor in sponsors])
    return (name, sponsors)



def populate_sponsor_data(club):
    """
    # used by new code as well as ck_data #
    Reads sponsor & membership data files populating attributes:
        club.sponsors_by_applicant, 
        club.applicant_set,
        club.sponsor_emails,
        club.sponsor_set.
    Is the following true???  (Should be 'last,first'!!!)
    All names (whether keys or values) are formated "last, first".
    Should be: keys are in format 'last,first' and 
    values in format 'last, first'
    """
    club.sponsor_set = set()  # eschew duplicates!
    club.sponsor_emails = dict()
    club.sponsors_by_applicant = dict()
    club.sponsor_tuple_by_applicant = dict()
    with open(club.sponsors_spot, 'r') as stream:
        if not club.quiet:
            print('Reading file "{}"...'.format(stream.name))
        for line in helpers.useful_lines(stream, comment='#'):
            name, sponsors = parse_sponsor_data_line(line)
            club.sponsor_tuple_by_applicant[name] = sponsors
            parts = line.split(':')
            names = parts[0].split()  # applicant 1st and 2nd names
            name = "{},{}".format(names[1], names[0])
            try:
                sponsors = parts[1].split(',')
            except IndexError:
                print("IndexError: {} sponsors???".format(name))
                sys.exit()
#           _ = input("sponsors = {}".format(repr(sponsors)))
            sponsors = [helpers.tofro_first_last(name)
                        for name in sponsors]
            for sponsor in sponsors:
                club.sponsor_set.add(sponsor)
            club.sponsors_by_applicant[name] = sponsors
            # key: applicant name
            # value: list of two sponsors in "last, first" format.
    with open(club.infile, 'r') as stream:
        dictreader = csv.DictReader(stream)
        for record in dictreader:
            record = helpers.Rec(record)
            name = record(member.fstrings['last_first'])
            if name in club.sponsor_set:
                club.sponsor_emails[name] = record['email']
    club.applicant_set = club.sponsors_by_applicant.keys()



def get_dict(source_file, sep=":", maxsplit=1):
    """
    # used by populate_extra_fees #
    A generic function to parse files.
    Blank lines or comments ('#') are ignored.
    All other lines must contains a 'first last' name followed by
    a separator (<sep> defaults to ':') and then anything else.
    Returned is a dict keyed by 'last,first' name and value: the
    string to right of <sep> (stripped of leading &/or trailing
    spaces. (It could be an empty string!)
    # Applicant data is populated one line at a time so this
    # function is not useful there
    """
    ret = {}
    with open(source_file, 'r') as stream:
        for line in stream:
            line = line.strip()
            if not line or line[0] == '#': continue
            parts = line.split(sep=sep, maxsplit=maxsplit)
            if len(parts) != 2: assert False
            names = parts[0].split()
            try:
                name_key = '{},{}'.format(names[1], names[0])
            except IndexError:
                _ = input("IndexError re line: '{}'"
                        .format(line))
            ret[name_key] = parts[1].strip()
    return ret



def populate_extra_fees(club):    # used by ck_data only (so far)
    """
    Populates club attrs by_name & by_category
    based on attr 'extra_fees_spots'..
    Tested by Tests.xtra_fees.py
    """
    def category(f):
        base, name = os.path.split(f)
        res = name.split('.')[0]
        return res

    by_category = {}
    by_name = {}

    for f in club.extra_fees_spots:
        res = get_dict(f)
        cat = category(f)
        for name, amt in res.items():
            # populate by_name:
            _ = by_name.setdefault(name, {})
            by_name[name][cat] = int(amt)
            # populate_by_category
            _ = by_category.setdefault(cat, {})
            by_category[cat][name] = int(amt)
    club.by_category = by_category
    club.by_name = by_name



def get_fee_paying_contacts(club): # so far used only by ck_data
    """
    Assumes club attribute <groups_by_name> has already been
    assigned (by data.gather_contacts_data.)
    Returns (and assigns to club.fee_paying_contacts) a list of
    dicts keyed by contact name (last,first) with values a list
    of dicts, keyed by fee categories (most are only one) with
    values amount owed.
    """
    collector = {}
    fee_groups = ["DockUsers", "Kayak", "Moorings"]
    fee_set = set(fee_groups)
    names = sorted(club.groups_by_name.keys())
    for name in names:
        intersect = club.groups_by_name[name].intersection(fee_set)
        if intersect:
            renamed_group = []
            for category in intersect:
                if category == 'DockUsers':
                    renamed_group.append('dock')
                if category == 'Kayak':
                    renamed_group.append('kayak')
                if category == 'Moorings':
                    renamed_group.append('mooring')
            if renamed_group:
                collector[name] = sorted(renamed_group)
    club.fee_paying_contacts = collector
#   helpers.store(collector, 'fee-paying-contacts.txt')
    return collector


def get_gmail_record(g_rec):
    """
    # used by gather_contacts_data #
    <g_rec> is a record from the gmail contacts file.
    Returns a dict with only the info we need.
    """
    g_email = g_rec["E-mail 1 - Value"]
    group_membership = (
        g_rec["Group Membership"].split(" ::: "))
    if (group_membership and
            group_membership[-1] == '* myContacts'):
        group_membership = group_membership[:-1]
    group_membership = set(group_membership)
    first_name = " ".join((
        g_rec["Given Name"],
        g_rec["Additional Name"],
        )).strip()
    last_name = " ".join((
        g_rec["Family Name"],
        g_rec["Name Suffix"],
        )).strip()
#   gname = "{}, {}".format(last_name, first_name)
    gname = "{},{}".format(last_name, first_name)
    alias = "{}{}".format(first_name, last_name)
    muttname = '{} {}'.format(first_name, last_name)
    return dict(
        gname=gname,
        alias=alias,
        muttname=muttname,
        g_email=g_email,
        groups=group_membership,
        )


def gather_contacts_data(club):
    """
    # used by ck_data #
    Gathers up the info we want from a gmail contacts.csv file.
    Sets up three dict attributes of the Club instance specified
    by club and then populates them by reading the gmail contacts
    csv file.
    In what follows, "name" == "{}, {}".format(last, first).
    The attributes are :
        g_by_name: keyed by "name" /w values indexed as follows:
          ["email"] => email
          ["groups"] => set of group memberships
        g_by_group: keyed by group membership /w values
        each a set of "names" of contacts sharing that group membership.
    """
    club.gmail_by_name = dict()  # => string
    club.groups_by_name = dict()  # => set

    club.g_by_group = dict()  # >set of names

    # Traverse contacts.csv => g_by_name
    with open(club.contacts_spot, 'r',
        encoding='utf-8', newline='') as file_obj:
        google_reader = csv.DictReader(file_obj)
        if not club.quiet:
            print('DictReading Google contacts file "{}"...'
                .format(file_obj.name))
        for g_rec in google_reader:
            g_dict = get_gmail_record(g_rec)

            club.gmail_by_name[g_dict['gname']] = g_dict['g_email']
            club.groups_by_name[g_dict['gname']] = g_dict['groups']

            for key in g_dict["groups"]:
                _ = club.g_by_group.setdefault(key, set())
                club.g_by_group[key].add(g_dict["gname"])



def gather_membership_data(club):    # used by ck_data #
    """
    Gathers info from club.infile (default club.MEMBERSHIP_SPoT)
    into attributes of <club>.
    """
    club.previous_name = ''
    err_code = member.traverse_records(club.MEMBERSHIP_SPoT,
        (
        member.add2email_by_m,
        member.get_usps,  # > usps_only & usps_csv
        member.add2fee_data,  # > fee_category_by_m(ember)
                              # & ms_by_fee_category  
        member.add2stati_by_m,
        member.add2ms_by_status, #  also > entries_w_status{}
        member.increment_napplicants,
        member.add2malformed,
        member.add2member_with_email_set, # also > no_email_set
        member.add2applicant_with_email_set,
        ), club)
    if err_code:
        print("Error condition! #{}".format(err_code))

def exercise_ck_data():
    club = Club()
    club.format = member.fstrings['last_first']
    res = ck_data(club)
    for line in res:
        print(line)


def ck_data(club,    # 280 lines of code!! ?needs breaking up?
            fee_details=False):
    """
    Check integrity/consistency of of the Club's data bases:
    1.  MEMBERSHIP_SPoT  # the main club data base
    2.  CONTACTS_SPoT    # csv downloaded from gmail
    3.  APPLICANT_SPoT   #
    4.  SPONSORS_SPoT    #
    5.  EXTRA_FEES_SPoTs #
        ...
    The first 4 of the above all contain applicant data
    and must be checked for consistency.
    Data in each of the 2nd and 5th are compared with
    the first and checked.
    Returns a report in the form of an array of lines.
    <fee_details> if set to True extends the output to include
    any discrepencies between what's billed each year vs what is
    still owed; useful after payments begin to come in.
    """
#   print("Entering data.ck_data")
    ret = []
    ok = []
    temp_list = []
    varying_amounts = []
    helpers.add_header2list("Report Regarding Data Integrity",
                        ret, underline_char='#', extra_line=True)
    # Collect data from csv files ==> club attributes:
    # collect info from main data base:
    gather_membership_data(club)
    # collect info from club gmail account contacts:
    gather_contacts_data(club)  # Sets up and populates:
    # club.gmail_by_name (string)
    # club.groups_by_name (set)     # club.g_by_group (set)

    ## First check that google groups match club data:
    # Deal with extra fees...
    fee_paying_contacts = get_fee_paying_contacts(club)
    fee_paying_contacts_set = set(fee_paying_contacts.keys())
    fee_paying_m_set = club.fee_category_by_m.keys()  #NOTE#
    no_email_recs = club.usps_only  # a list of records
    no_email_set = {member.fstrings['key'].format(**rec)
                    for rec in no_email_recs}
    fee_paying_w_email_set = fee_paying_m_set - no_email_set
    collector = {}
    for name in sorted(fee_paying_w_email_set):
        collector[name] = [key for key in 
                sorted(club.fee_category_by_m[name].keys())]
#   helpers.store(collector, 'fee-paying-members.txt')
    if not club.fee_paying_contacts==collector:
        ret.append("\nfee_paying_contacts|=fee paying members")
    fee_missmatches = helpers.check_sets(
        fee_paying_contacts_set,
        fee_paying_w_email_set,
        "Fee paying contacts not in member listing",
        "Fee paying members not in google contacts",
        )
    if fee_missmatches:
        only_in_contact_set = (fee_paying_contacts_set
                                    - fee_paying_w_email_set)
        only_in_paying_w_email_set = (fee_paying_w_email_set
                                    - fee_paying_contacts_set)
        helpers.add_header2list(
            "Extra fees missmatches",
            ret, underline_char='=', extra_line=True)
        if only_in_contact_set:
            ret.append("Only in Contacts:")
            for item in only_in_contact_set:
                ret.append("\t{}".format(repr(item)))
        if only_in_paying_w_email_set:
            ret.append("Only in Member DB:")
            for item in only_in_paying_w_email_set:
                ret.append("\t{}".format(repr(item)))
        ret.extend(fee_missmatches)
    else:
        ok.append('No fee missmatches')

   
    # Deal with applicants...
# if get a KeyError such as the following:
#     File "/home/alex/Git/Club/Utils/data.py", line ???, in ck_data
#       applicant_set = club.g_by_group[club.APPLICANT_GROUP]
#   KeyError: 'applicant'
# ... check that the contacts.cvs file came from the Club's gmail
# account, not someone else's!!!
    applicant_set = club.g_by_group[club.APPLICANT_GROUP]
#   _ = input(f"applicant_set: {applicant_set}")
    applicant_missmatches = helpers.check_sets(
        applicant_set,
        club.applicant_with_email_set,
        "Applicant(s) in Google Contacts not in Member Listing",
        "Applicant(s) in Member Listing not in Google Contacts"
        )
    # Deal with members...
    member_missmatches = helpers.check_sets(
        club.g_by_group[club.MEMBER_GROUP],
        club.member_with_email_set,
        "Member(s) in Google Contacts not in Member Listing",
        "Member(s) in Member Listing not in Google Contacts"
        )

    g_inactive = club.g_by_group[club.INACTIVE_GROUP]
    m_inactive = set(club.ms_by_status['m'])
    special_status_missmatches = helpers.check_sets(
        g_inactive,
        m_inactive,
        "{} doesn't match membership listing"
            .format(club.INACTIVE_GROUP),
        "'m' status (inactive) not reflected in google contacts"
        )


    if special_status_missmatches:
        helpers.add_header2list(
            "Special status missmatches",
            ret, underline_char='=', extra_line=True)
        ret.extend(special_status_missmatches)
    else:
        ok.append("No special status missmatches")


    if applicant_missmatches or member_missmatches:
        helpers.add_header2list(
            "Missmatch: Gmail groups vs Club data",
            ret, underline_char='=', extra_line=True)
        ret.extend(member_missmatches + applicant_missmatches)
    else:
        ok.append("No Google Groups vs Member/Applicant Missmatch.")

    # Collect data from custom files ==> local variables
    populate_extra_fees(club)
    populate_sponsor_data(club)
    populate_applicant_data(club)
    applicants_by_status = get_applicants_by_status(club)

    # Deal with MEMBERSHIP data-
    # First check for malformed records:
    if not club.malformed:
        ok.append("No malformed records found.")
    else:
        print("Found Malformed Records.")
        helpers.add_sub_list("Malformed Records", club.malformed, ret)


    # Compare gmail vs memlist emails and then memlist vs gmail
    # now that both listings have names rather than sets of names:
    email_problems = []
    missing_emails = []
    non_member_contacts = []
    emails_missing_from_contacts = []
    common_emails = []

    if emails_missing_from_contacts:
        helpers.add_sub_list("Emails Missing from Google Contacts",
                             emails_missing_from_contacts, ret)
    else:
        ok.append("No emails missing from gmail contacts.")


    g_members = club.g_by_group[club.MEMBER_GROUP]
    g_applicants = club.g_by_group[club.APPLICANT_GROUP]
    keys = sorted(club.ms_by_status.keys(), reverse=True)
    for key in keys:
        if not (key in member.APPLICANT_SET):
            val = (club.ms_by_status.pop(key))
    applicants_by_status = helpers.keys_removed(applicants_by_status,
                                        ('m', 'zae'))
    applicants_by_status = helpers.lists2sets(applicants_by_status)
    ms_by_status_sets = helpers.lists2sets(club.ms_by_status)
    if applicants_by_status != ms_by_status_sets:
        ret.append("\nApplicant problem:")
        ret.append("The following data from applicant SPoT-")
        ret.extend(helpers.show_dict(applicants_by_status, extra_line=False))
        ret.append("- does not match the following membership SPot-")
        ret.extend(helpers.show_dict(club.ms_by_status,
                   extra_line=False))
        ret.append("- End of comparison -")
    else:
        ok.append("No applicant problem.")

    if non_member_contacts:
        helpers.add_sub_list(
            "Contacts without a corresponding Member email",
            non_member_contacts, ret)
    else:
        ok.append('No contacts that are not members.')

    # Now check fees: mem list vs extra fees SPoT
    # Keep in mind that after payment amounts won't match
    not_matching_notice = ''
    if (club.by_category !=
            club.ms_by_fee_category):
        club_keys = set(club.by_category.keys())
        file_keys = set(club.ms_by_fee_category.keys())
        if club_keys == file_keys:
#           print("{} vs {}".format(club_keys, file_keys))
            not_matching_notice = (
                "Fee amounts (by category) don't match")
            # traverse keys and report by name later
        else:
            ret.append("\nFees problem (by fee category):")
            ret.append("extra_fees_files:")
            ret.append(repr(club.by_category))
            ret.append("###  !=  ###")
            ret.append("club.ms_by_fee_category:")
            ret.append(repr(club.ms_by_fee_category))
    else:
        ok.append("No fees by category problem.")

    if (club.by_name != club.fee_category_by_m):
        club_keys = set(club.by_name.keys())
        file_keys = set(club.fee_category_by_m.keys())
        if club_keys == file_keys:
            if fee_details:
                not_matching_notice = "Fee amounts don't match"
                # traverse keys and specify which amounts don't match
                sorted_club_keys = sorted([key for key in club_keys])
                for key in sorted_club_keys:
                    if (club.by_name[key] !=
                            club.fee_category_by_m[key]):
                        varying_amounts.append('{}: {} != {}'.format(
                                key,
                                club.by_name[key],
                                club.fee_category_by_m[key]
                                ))
            else:
                not_matching_notice = (
            "Fee amounts don't match (try -d option for details)")
        else:
            print("club_keys != file_keys")
            club_set = set(club_keys)
            file_set = set(file_keys)
            print(club_keys - file_keys)
            print(file_keys - club_keys)
#           print(sorted(club_keys))
#           print(sorted(file_keys))
            ret.append("\nFees problem (by name):")
            ret.append(
                    "club.fee_category_by_m[club.NAME_KEY]:")
            sorted_keys = sorted(
#               [key for key in club.fee_category_by_m[
#                   club.NAME_KEY].keys()])
                [key for key in club.fee_category_by_m.keys()])
            for key in sorted_keys:
                ret.append("{}: {}".format(key, 
                    club.fee_category_by_m[key]))
#           ret.append(repr(fees_by_name))
            ret.append("###  !=  ###")
            ret.append("club.fee_category_by_m:")
            for key, value in club.fee_category_by_m.items():
                ret.append("{}: {}".format(key, repr(value)))
#           ret.append(repr(club.fee_category_by_m))
    else:
        ok.append("No fees by name problem.")

    if ok:
        helpers.add_sub_list(
                "No Problems with the Following", ok, ret)
    ai_notice = "Acceptable Inconsistency"
    if not_matching_notice:
        helpers.add_header2list(ai_notice,
                                ret, underline_char='=')
        ret.append(not_matching_notice)
    if varying_amounts:
        helpers.add_header2list(
            "Fee Disparities: probably some have paid",
            ret, underline_char='-', extra_line=True)
        ret.extend(varying_amounts)
    return ret


def applicant_csv(club):
    """
    Expects it's parameter <club> to have the attribute
    club.applicant_data created by running both
    populate_sponsor_data and populate_applicant_data (in that order.)
    Returns a list (ordered by last,first) of dicts with the following keys:
    'first', 'last', 'status', 'app_rcvd' 'fee_rcvd',
    '1st', '2nd' '3rd', 'inducted', 'dues_paid', 'sponsor1', 'sponsor2'
    If club.applicant_csv is set, the data is sent to that file.
    If boolean club.all_applicants is set then all past as well as
    current applicants will be included.  i.e. All that are in the DB.
    Data comes from applicant and sponsors data files, not from the 
    main membership DB. Use get_applicant_data for that.
    """
    ret = []
    data = [club.applicant_data[key] for key in
            sorted(club.applicant_data.keys())]
    with open(club.applicant_csv, 'w', newline='') as stream:
        dictwriter = csv.DictWriter(stream,
                fieldnames=club.APPLICANT_DATA_FIELD_NAMES)
        dictwriter.writeheader()
        for row in data:
            ca = member.is_applicant(row)
            if club.all_applicants:
                dictwriter.writerow(row)
                ret.append(row)
            else:
                if member.is_applicant(row):
                    dictwriter.writerow(row)
                    ret.append(row)
    return ret


def applicants_by_status(applicant_data):
    """
    Expects its parameter (<applicant_data>) to be
    what's returned by the applicant_csv function.
    (See its docstring for details.)
    Returns a dict keyed by status, values are lists
    of the corresponsing entries in <applicant_data>.
    """
    collector = {}
    for record in applicant_data:
        _ = collector.setdefault(record['status'], [])
        collector[record['status']].append(record)
    return collector


if __name__ == '__main__':
    exercise_ck_data()
    sys.exit()
    club = Club()
    populate_sponsor_data(club)    # { Must do this before
    populate_applicant_data(club)  # { this
               # { for club.applicant_data to be complete. 
    club.applicant_csv = "applicant.csv"
#   club.all_applicants = True   # default is False
    res = applicant_csv(club)
    by_status = applicants_by_status(res)
    collector = []
    sorted_keys = sorted([key for key in by_status.keys()],
            reverse=True)
    for key in sorted_keys:
        collector.append(key)
        for item in by_status[key]:
            values = [value for value in item.values()]
            output = [f"{values[0]} {values[1]}", ]
            output.extend(values[2:])
#           collector.append( ', '.join(item.values()))
            collector.append( ', '.join(output))
    helpers.send2file('\n'.join(collector), 'by_status.txt')



