#!/usr/bin/env python3

# File: data.py

"""
# Originally called ck_data.py
Renamed data.py because it deals with reading data files:
    specifically the non csv (SPoT) files.
To avoid cross import problem, the class Club requires
a module of its own.

Provides automated access to the
Bolinas Rod and Boat Club's data files:
... those identified by the constants ending in "SPoT".
Motivated by the desire to have a way of checking for data integrity,
it then morphed into a way of collecting data for presentation:
    eg list of applicants by number of meetings attended.
Current version checks for data consistency across the four
files containing membership related data.
"""

import os
import sys
import csv
import json
import helpers
import member
import sys_globals as glbs
from rbc import Club

DEBUGGING_FILE = 'debug.txt'

def get_fieldnames(csv_file: "name of csv file"
        ) -> "list of the csv file's field names":
    with open(csv_file, 'r', newline='') as file_object:
        print('DictReading file "{}"...'.format(file_object.name))
        dict_reader = csv.DictReader(file_object, restkey='extra')
        return dict_reader.fieldnames


def gather_membership_data(club):
    """
    Gathers the info we want from the membership csv file
    which is defined by club.MEMBERSHIP_SPoT.

    Sets up a number of collectors as attributes of <club>
    and then calls member.traverse_records to populate them.
    See member.add2... functions corresponding to each[1] of the
    following <club> attributes.
    [1] except both 'fee_category' collectors are populated by
    member.add2fee_data function and
    both 'email' collectors.
    """
    err_code = member.traverse_records(club.MEMBERSHIP_SPoT,
                                       (member.add2db_emails,
#                                       member.add2email_data,
                                        member.add2email_by_m,
                                        member.add2fee_data,
                                        member.add2stati_by_m,
                                        member.add2ms_by_status,
                                        member.increment_napplicants,
                                        member.add2malformed,
                                        member.add2member_with_email_set,
                                        member.add2applicant_with_email_set,
                                        ), club)
    if err_code:
        print("Error condition! #{}".format(err_code))


def get_gmail_record(g_rec):
    """
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
    gname = "{}, {}".format(last_name, first_name)
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
    with open(club.CONTACTS_SPoT, 'r',
        encoding='utf-8', newline='') as file_obj:
        google_reader = csv.DictReader(file_obj)
        print('DictReading Google contacts file "{}"...'.format(
                                                    file_obj.name))
        for g_rec in google_reader:
            g_dict = get_gmail_record(g_rec)


            club.gmail_by_name[g_dict['gname']] = g_dict['g_email']
            club.groups_by_name[g_dict['gname']] = g_dict['groups']

            for key in g_dict["groups"]:
                _ = club.g_by_group.setdefault(key, set())
                club.g_by_group[key].add(g_dict["gname"])


def move_date_listing_into_record(dates, record):
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
            continue
            record[key] = ''


def applicant_data_line2record(line):
    """
    Assumes a valid line from the Data/applicant.txt file.
    Otherwise a dict is returned with keys listed in 
    Club.APPLICANT_DATA_FIELD_NAMES: "first", "last", "status", 
        "app_rcvd", "fee_rcvd", 
        "1st", "2nd", "3rd",
        "inducted", "dues_paid",
        "Sponsor1", "Sponsor2",
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
        _status = "zae"  # see members.STATUS_KEY_VALUES
        l -= 1
    else:
        _status = ''
    if l == 0:           # Should never have an entry /w no dates.
        status = "zaa"   # No longer a valid status
        print("Entry for {}{} is without any dates."
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
    if _status:
        ret['status'] = _status
    else:
        ret['status'] = status
    return ret


def populate_applicant_data(club):
    """
    Reads applicant data file populating two attributes:
    1. club.applicant_data: a dict with keys == applicants
        and each value is a record with the following fields:
            "first", "last", "status",
            "app_rcvd", "fee_rcvd",   #} date (or empty
            "1st", "2nd", "3rd",      #} string if event
            "inducted", "dues_paid",  #} hasn't happened.
            "Sponsor1", "Sponsor2"   # empty string if not available
    2. club.applicant_data_keys
    Note: Sponsor data is included if populate_sponsor_data has
    already been run, othwise, the values remain as empty strings.
    """
    sponsors = hasattr(club, 'sponsors_by_applicant')
    if sponsors: sponsored = club.sponsors_by_applicant.keys()
    club.applicant_data = {}
    with open(club.applicant_spot, 'r') as stream:
        print('Reading file "{}"...'.format(stream.name))
        for line in helpers.useful_lines(stream, comment='#'):
            rec = applicant_data_line2record(line)
            name = member.get_last_first(rec)
            rec = applicant_data_line2record(line)
            if sponsors and name in sponsored:
                rec["sponsors"] = club.sponsors_by_applicant[name]
            club.applicant_data[name] = rec
        club.applicant_data_keys = club.applicant_data.keys()


redacted = '''
### Expect to redact the following in favour of the above. ###
#   But must first refactor ck_data which still uses it!     #

def get_applicant_data(spot, sponsor_file=None):
    """
    Reads SPoT(s): the applicant data file +/- the sponsor file.
    Returns a dict keyed by applicant names ("last, first").
    Values are records (dicts) with fields as defined by
    rbc.Club.APPLICANT_DATA_FIELD_NAMES.
    """
    if sponsor_file:
        sponsor_data = get_sponsor_data(sponsor_file)
        sponsored_applicants = set(sponsor_data.keys())
    ret = {}
    with open(spot, 'r') as src:
        print('Reading file "{}"...'.format(src.name))
        for line in helpers.useful_lines(src, comment='#'):
            res = applicant_data_line2record(line)
            name = member.get_last_first(res)
            ret[name] = res
            if sponsor_file and name in sponsored_applicants:
                sponsors = sponsor_data[name]
                assert len(sponsors) == 2
                ret[name]['Sponsor1'] = sponsors[0].strip()
                ret[name]['Sponsor2'] = sponsors[1].strip()
    return ret


### Expect to redact the following.                      ###
#   But must first refactor ck_data which still uses it!   #

def get_applicants_by_status(applicant_data):
    """
    Param is what's returned by get_applicant_data.
    Returns a dict keyed by status; values are each
    a list of applicant ('last, first') names.
    Note: also possible to get applicants by status from the main data
    base- this function uses data supplied by get_applicant_data which
    uses the applicant data files (rather than the main data base.)
    """
    #### Want to refactor so 'club' is a parameter along with  ####
    #### a format string which defaults to "{first} {last}".   ####
    # def get_applicants_by_status(club, fmt_str='{first} {last'}):
    ret = {}
    for name in applicant_data.keys():
        status = applicant_data[name]['status']
        _ = ret.setdefault(status, [])
        ret[status].append(name)
    return ret
'''


def parse_sponsor_data_line(line):
    """
    Assumes blank and commented lines have already been removed.
    returns a 2 tuple: (for subsequent use as a key/value pair)
    t1 is "last, first" name
    t2 is a tuple of sponsors ('last, first')
    Fails if encounters an invalid line!!!
    """
    parts = line.split(":")
    sponsored = parts[0].strip()
    names = sponsored.split()
    name = '{}, {}'.format(names[1], names[0])
    part2 = parts[1]
    sponsors = tuple([
        helpers.tofro_first_last(sponsor.strip())
        for sponsor in parts[1].split(", ")])
    return (name, sponsors)


def populate_sponsor_data(club):
    """
    Reads sponsor & membership data files populating attributes:
        club.sponsors_by_applicant, 
        club.applicant_set,
        club.sponsor_emails,
        club.sponsor_set.
    All names (whether keys or values) are formated "last, first".
    """
    club.sponsor_set = set()  # eschew duplicates!
    club.sponsor_emails = dict()
    club.sponsors_by_applicant = dict()
    with open(club.sponsor_spot, 'r') as stream:
        print('Reading file "{}"...'.format(stream.name))
        for line in helpers.useful_lines(stream, comment='#'):
            parts = line.split(':')
            names = parts[0].split()  # applicant 1st and 2nd names
            name = "{}, {}".format(names[1], names[0])
            try:
                sponsors = parts[1].split(',')
            except IndexError:
                print("IndexError: {} sponsors???".format(name))
                sys.exit()
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
            name = member.member_name(record, club)
            if name in club.sponsor_set:
                club.sponsor_emails[name] = record['email']
    club.applicant_set = club.sponsors_by_applicant.keys()


redacted = '''
## Plan to redact the following in favour of the above function.
# it's being used by get_applicant_data which is also to be redacted.
def get_sponsor_data(spot):
    """
    <spot> is name of file (usual default: rbc.Club.SPONSORS_SPoT.
    Returns a dict: keys are '2nd, 1st' names,
                    values are tuples of sponsors.
    Used by get_applicant_data (if sponsor_file is specified.)
    Also used when sponsors are to be 'cc'ed emails to applicants
    """
    ret = {}
    with open(spot.strip(), 'r') as src:
        print('Reading file "{}"...'.format(src.name))
        for line in helpers.useful_lines(src, comment='#'):
            tup = parse_sponsor_data_line(line)
            (name, sponsors) = (tup[0], tup[1])
            ret[name] = sponsors
    return ret
'''


def line_of_meeting_dates(applicant_datum):
    """
    Returns a string: comma separated listing of meeting dates.
    """
    dates = []
    for date_key in Club.MEETING_DATE_NAMES:
        if applicant_datum[date_key]:
            dates.append(applicant_datum[date_key])
    return ', '.join(dates)


redacted = '''
def get_emails(list_of_members, file_name=Club.MEMBERSHIP_SPoT):
    """
    <list_of_members> is a list in '{last}, {first}' format.
    Returns a dict keyed by members of the list with their email
    address as a value for each.
    """
    ret = dict()
    with open(file_name, 'r') as stream:
        d_reader = csv.DictReader(stream)
        for record in d_reader:
            pass
    return ret


def list_of_dates(applicant_datum):
    """
    Returns a list if meeting dates.
    """
    dates = []
    for date_key in Club.MEETING_DATE_NAMES:
        if applicant_datum[date_key]:
            dates.append(applicant_datum[date_key])
    return dates


def get_meeting_dates(applicant, club):
    """
    Depends on the club.applicant_data attribute.
    Returns None if data unavailable, otherwise:
    Returns a dict with two entries (each possibly empty:)
        'dates': list (possible empty) of meeting dates attended 
        'sponsors': list (possibly empty) of sponsors)
    """
    if not hasattr(club, applicant_data):
        print("!! No club.applicant_data attribute  !!")
        return 
    try:
        rec = club.applicant_data[applicant]
    except KeyError:
        print("!! No data for applicant {} !!".format(applicant))
        return
    ret = {"dates": [], "sponsors": []}
    dates = []
    for key in ("1st", "2nd", "3rd", "inducted", "dues_paid"):
        val = rec[key]
        if val:
            dates.append(val)
    if dates:
        ret["dates"] = (', '.join(dates))
    sponsors = []
    for key in ("Sponsor1", "Sponsor2"):
        val = rec[key]
        if val:
            sponsors.append(val)
    if sponsors:
        ret['sponsors'](', ',join(sponsors))
    return ret


def gather_sponsors(infile):
    """
    Read file typified by Data/sponsors.txt
    and return a dict keyed by 'last, first' names with sponsors as
    values.
    """
    ret = {}
    with open(infile, 'r') as file_obj:
        for line in helpers.useful_lines(file_obj, comment='#'):
            parts = line.split(':')
            names = parts[0].split()
            name = "{}, {}".format(names[1], names[0])
            sponsors = parts[1].strip()
            ret[name] = sponsors
    return ret
'''


def gather_extra_fees_data(extra_fees_spot, json_file=None):
    """
    Reads in_file and returns a dict with keys:
        Club.NAME_KEY: a dict keyed by name with
            each a set of (category, amount) tuples[1].
        Club.CATEGORY_KEY: a dict keyed by category with
            each a set of (last_first, amount) tuples.

    Input file must have three header lines each containing
    one of the following words: Mooring, Dock, Kayak,
    and ending with ':'.
    Other lines must contain 'First Last: amt'.
    ...as can be seen in Data/extra_fees.txt.
    If <json_file> is specified (name of a file) the
    'by_name' dict is dumped into a json file of that name.
    [1] The 'by_name' component can be converted so that its
    values are all a single string using the json_fees_by_name
    function.
    """
    by_name = {}
    by_category = dict(  # json version of input file
        Kayak=[],
        Dock=[],
        Mooring=[],
        )
    categories = [key for key in by_category.keys()]

    with open(extra_fees_spot, 'r') as f_obj:
        print('Reading file "{}"...'.format(f_obj.name))
        category = ""
        for line in helpers.useful_lines(f_obj, comment='#'):
            category_change = False
            if line[-1] == ':':  # line ending in ':' means
                                 # there's been acategory change
                words = line[:-1].split()
                for word in words:
                    if word in categories:
                        category = word
                        category_change = True
                        continue
            else:  # Expect a name with fee for current category...
#               print("line: {}".format(line))
                parts = line.split(':')
                fee = int(parts[1])
                names = parts[0].split()
                first_name = names[0]
                last_name = names[1]
                name_key = "{}, {}".format(last_name, first_name)
                _ = by_name.setdefault(name_key, [])
                _ = by_category.setdefault(category, [])
                by_name[name_key].append((category, fee))
                by_category[category].append((name_key, fee))
    if json_file:
        helpers.dump2json_file(by_name, json_file, verbose=True)
    #   else:
    #       print("No json file specified.")
    return {Club.NAME_KEY: by_name,
            Club.CATEGORY_KEY: by_category,
            }

def extra_charges(club, raw=False):
    """
    Returns a report of members with extra charges.
    Only client is extra_charges_cmd.
    Also creates a json file if requested.
    Instance of Club must be set up by client along with
    the following attributes (from command line arguments):
        infile, json_file,
        presentation_format, width
    """
    print('Retrieving input data from "{}"'.format(club.infile))
    if club.presentation_format == 'listing':
        if club.json_file:   # do we want a json file..
            _ = gather_extra_fees_data(club.EXTRA_FEES_SPoT,
                                       json_file=club.json_file)
        # Just return file content:
        with open(club.infile, 'r') as f_object:
            return [line.strip() for line in f_object]
    extra_fees = gather_extra_fees_data(club.EXTRA_FEES_SPoT,
                                        json_file=club.json_file)
    by_name = extra_fees[club.NAME_KEY]
    by_category = extra_fees[club.CATEGORY_KEY]
    if club.presentation_format == 'table':  # Names /w fees in columns:
        res = present_fees_by_name(by_name)
        if raw:
            ret = []
        else:
            ret = ["Extra fees by member:",
                   "=====================", ]
        ret.extend(helpers.tabulate(res, down=True,
                   max_width=club.max_width, separator=' '))
        return(ret)
    elif club.presentation_format == 'listings':
        return(present_fees_by_category(extra_fees, raw=raw))
    else:
        print(club.bad_format_warning)
        sys.exit()



def present_fees_by_name(extra_fees, raw=False):
    """
    Param would typically be the returned value of
    gather_extra_fees_data(extra_fees_spot)
    or its NAME_KEY value.
    Returns a text listing with or (if raw=True) without a header.
    """
    if Club.NAME_KEY in extra_fees:
        jv = extra_fees[Club.NAME_KEY]
    else:
        jv = extra_fees
    ret = []
    for key in jv:
        charges = []
        for value in jv[key]:
            charges.append("{} {}".format(value[0], value[1]))
        charges = ', '.join(charges)
        ret.append("{key}: {charges}".format(
                key=key, charges=charges))
    return sorted(ret)


def present_fees_by_category(extra_fees, raw=False,
                             always_incl_fees=False,  # not implemented
                             ):
    """
    Param would typically be the returned value of
    gather_extra_fees_data(extra_fees_spot)
    or its CATEGORY_KEY value.
    Returns a text listing with or (if raw=True) without a header.
    Last parameter (not yet implemented) changes the default of
    showing individuals' fees only for mooring since fees for dock
    use and kayak storage are the same for everyone .
    """
    if Club.CATEGORY_KEY in extra_fees:
        jv = extra_fees[Club.CATEGORY_KEY]
    else:
        jv = extra_fees
    categories = sorted([key for key in jv])
    ret = {}
    max_width = {}
    for category in categories:
        ret[category] = []
        max_width[category] = 0
    if raw:
        header = []
    else:
        header = ["Extra fees by category",
                  "======================",
                  '']
    for category in categories:
        if category == 'Kayak':
            ret[category].append(category + ': ${}'.format(
                        Club.KAYAK_FEE))
        elif category == 'Dock':
            ret[category].append(category + ': ${}'.format(
                        Club.DOCK_FEE))
        elif category == 'Mooring':
            ret[category].append(category)
        else:
            assert False
        ret[category].append('-' * len(ret[category][0]))
        max_width[category] = len(ret[category][0])
        for value in jv[category]:
            if category == 'Mooring':
                ret[category].append("{0}: ${1}".format(*value))
            else:
                ret[category].append("{}".format(value[0]))
            if len(ret[category][-1]) > max_width[category]:
                max_width[category] = len(ret[category][-1])
    max_n = 0
    new_ret = {}
    for category in categories:
        new_ret[category] = []
        if len(ret[category]) > max_n:
            max_n = len(ret[category])
        for line in ret[category]:
            line = line + ' ' * (max_width[category] - len(line))
            new_ret[category].append(line)
    for category in categories:
        new_ret[category].extend([' ' * max_width[category], ]
                                 * (max_n - len(new_ret[category])))
    zipped = zip(*[value for value in new_ret.values()])
    res = []
    for item in zipped:
        res.append('{}  {}  {}'.format(*item))
    return header + res



def ck_data(club,
            fee_details=False):
    """
    Check integrity/consistency of of the Club's data bases:
    1.  MEMBERSHIP_SPoT  # the main club data base
    2.  CONTACTS_SPoT    # csv downloaded from gmail
    3.  APPLICANT_SPoT   #
    4.  SPONSORS_SPoT    #
    5.  EXTRA_FEES_SPoT  #
        ...
    The first 4 of the above all contain applicant data
    and must be checked for consistency.
    Data in each of the 2nd and 5th are compared with
    the first and checked.
    Returns a report in the form of an array of lines.
    <fee_details> if set to True extends the output to include
    any discrepencies between what's billed each year vs what is
    still owed; expected after payments begin to come in.
    """
    print("Entering data.ck_data")
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
    # Deal with applicants...
# if get a KeyError such as the following:
#     File "/home/alex/Git/Club/Utils/data.py", line ???, in ck_data
#       applicant_set = club.g_by_group[club.APPLICANT_GROUP]
#   KeyError: 'applicant'
# ... check that the contacts.cvs file came from the Club's gmail
# account, not someone else's!!!
    applicant_set = club.g_by_group[club.APPLICANT_GROUP]
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
    special_status_missmatches = helpers.check_sets(
        club.g_by_group[club.INACTIVE_GROUP],
        set(club.ms_by_status['m']),
        "{} doesn't match membership listing"
            .format(club.INACTIVE_GROUP),
        "'m' status (inactive) not reflected in google contacts"
        )


    if (
        applicant_missmatches or
        member_missmatches or
        special_status_missmatches):
        helpers.add_header2list(
            "Missmatch: Gmail groups vs Club data",
            ret, underline_char='=', extra_line=True)
        ret.extend(member_missmatches + applicant_missmatches)
    else:
        ok.append("No Google Groups vs Member/Applicant Missmatch.")

    # Collect data from custom files ==> local variables
    extra_fees_info = gather_extra_fees_data(club.extra_fees_spot)
    populate_sponsor_data(club)
    populate_applicant_data(club)
    applicants_by_status = get_applicants_by_status(
        club.applicant_data)

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
    if (extra_fees_info[club.CATEGORY_KEY] !=
            club.ms_by_fee_category):
        club_keys = set(extra_fees_info[club.CATEGORY_KEY].keys())
        file_keys = set(club.ms_by_fee_category.keys())
        if club_keys == file_keys:
            not_matching_notice = (
                "Fee amounts (by category) don't match")
            # traverse keys and report by name later
        else:
            ret.append("\nFees problem (by fee category):")
            ret.append("extra_fees_info[club.CATEGORY_KEY]:")
            ret.append(repr(extra_fees_info[club.CATEGORY_KEY]))
            ret.append("###  !=  ###")
            ret.append("club.ms_by_fee_category:")
            ret.append(repr(club.ms_by_fee_category))
    else:
        ok.append("No fees by category problem.")

    if (extra_fees_info[club.NAME_KEY] != club.fee_category_by_m):
        club_keys = set(extra_fees_info[club.NAME_KEY].keys())
        file_keys = set(club.fee_category_by_m.keys())
        if club_keys == file_keys:
            if fee_details:
                not_matching_notice = "Fee amounts don't match"
                # traverse keys and specify which amounts don't match
                club_keys = sorted([key for key in club_keys])
                for key in club_keys:
                    if (extra_fees_info[club.NAME_KEY][key] !=
                            club.fee_category_by_m[key]):
                        varying_amounts.append('{}: {} != {}'.format(
                                key,
                                extra_fees_info[club.NAME_KEY][key],
                                club.fee_category_by_m[key]
                                ))
            else:
                not_matching_notice = (
                    "Fee amounts don't match (try -d option for details)")
        else:
            print(sorted(club_keys))
            print(sorted(file_keys))
            ret.append("\nFees problem (by name):")
            ret.append("extra_fees_info[club.NAME_KEY]:")
            sorted_keys = sorted(
                [key for key in extra_fees_info[club.NAME_KEY].keys()])
            for key in sorted_keys:
                ret.append("{}: {}".format(key, extra_fees_info[club.NAME_KEY][key]))
#           ret.append(repr(extra_fees_info[club.NAME_KEY]))
            ret.append("###  !=  ###")
            ret.append("club.fee_category_by_m:")
            for key, value in club.fee_category_by_m.items():
                ret.append("{}: {}".format(key, repr(value)))
#           ret.append(repr(club.fee_category_by_m))
    else:
        ok.append("No fees by name problem.")

    if ok:
        helpers.add_sub_list("No Problems with the Following", ok, ret)
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


def restore_fees(club):
    """
    Sets up and leaves a new list of records in club.new_db:
    Dues and relevant fees are applied to each member's record.
    Also populates the following:
        <club.name_set>   
        <club.errors>
    The <club.errors> list is populated by names that are found
    in the <fees_json_file> but not in the <membership_csv_file>.
    Also listed will be any members still owing.
    Other warnings may also appear.
    """
    print(
        "Preparing to restore dues and fees to the data base...")
    print(
        "  1st check that no one is still owing ...")
    club.errors = []
    club.new_db = []
    club.non0balance = {}
    club.name_set = set()
    club.by_name = gather_extra_fees_data(club.extra_fees_spot
                                         )[Club.NAME_KEY]
    club.extra_fee_names = set([key for key in club.by_name.keys()])
    err_code = member.traverse_records(club.infile, (
        member.populate_non0balance_func,
        member.populate_name_set_func,
        member.add_dues_fees2new_db_func,
        ), club)
    names_not_members = club.extra_fee_names - club.name_set
    if names_not_members:
        warning = "Not all in extra fees listing are members!"
        print(warning)
        club.errors.append(warning)
        for name in names_not_members:
            club.errors.append(
                "\t{} listed as paying fee(s) but not a member."
                .format(name))

# save_db moved to helpers


def data_listed(data, underline_char='=', inline=False):
    """
    Assumes 'data' is a dict with list values.
    Returns a list of lines: each key as a header +/- underlining
    followed by its values one per line, or (if 'inline'=True) on
    the same line separated by commas after a colon.
    """
    ret = []
    keys = sorted(data.keys())
    for key in keys:
        values = sorted(data[key])
        if inline:
            ret.append(key + " :" + ", ".join(values))
        else:
            ret.append("\n" + key)
            ret.append(underline_char * len(key))
            ret.extend(values)
    return ret


# the following (compare function) is not used?  Redact?
def compare(data1, data2, underline_char='=', inline=False):
    ret = []
    if data1 == data2:
        ret.append("Good News: data1 == data2")
    else:
        ret.append("Bad News: data1 != data2")
    ret.append("\nListing1...")
    ret.extend(data_listed(data1, underline_char, inline))
    ret.append("\nListing2...")
    ret.extend(data_listed(data2, underline_char, inline))
    ret.append("... end of listings")
    return ret


redacted = '''
def test_ck_data():
    club = Club
    return ck_data(club)
#   print("Call to ck_integrity has returned...")
#   print(res)
#   return res
'''

def list_mooring_data(extra_fees_spot):
    extra_fees_data = gather_extra_fees_data(extra_fees_spot)
#   data = extra_fees_data[Club.CATEGORY_KEY]
#   print(repr(data["Mooring"]))
    mooring_data = extra_fees_data[Club.CATEGORY_KEY]["Mooring"]
    return sorted(
        ["{0} - {1}".format(*datum) for datum in mooring_data])



if __name__ == '__main__':
    print("data.py compiles OK.")
    redacted = '''
else:
    def print(*args, **kwargs):
        pass
'''
