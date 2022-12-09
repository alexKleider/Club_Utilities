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


def get_fieldnames(csv_file: "name of csv file", report=True
        ) -> "list of the csv file's field names":
    """
    Returns the field names of the csv file named.
    """
    with open(csv_file, 'r', newline='') as file_object:
        if report and not club.quiet:
            print('DictReading file "{}"...'.format(file_object.name))
        dict_reader = csv.DictReader(file_object, restkey='extra')
        return dict_reader.fieldnames


def ck_malformed(club):
    """
    Deal with malformed memlist records (if any)
    """
    if not club.malformed:
        club.ok.append("No malformed records found.")
    else:
        print("Found Malformed Records.")
        helpers.add_sub_list("Malformed Records", club.malformed,
                club.ret)


def ck_fee_paying_labels(club):
    """
    Checks fee paying labels against memlist data.
    Appends results to club.ret.
    """
    fee_paying_contacts = get_fee_paying_contacts(club)
    fee_paying_contacts_set = set(fee_paying_contacts.keys())
    fee_paying_m_set = club.fee_category_by_m.keys()
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
        club.ret.append("\nfee_paying_contacts|=fee paying members")
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
            "Memlist vs contacts fee missmatches",
            club.ret, underline_char='=', extra_line=True)
        if only_in_contact_set:
            club.ret.append("Only in Contacts:")
            for item in only_in_contact_set:
                club.ret.append("\t{}".format(repr(item)))
        if only_in_paying_w_email_set:
            club.ret.append("Only in Member DB:")
            for item in only_in_paying_w_email_set:
                club.ret.append("\t{}".format(repr(item)))
        club.ret.extend(fee_missmatches)
    else:
        club.ok.append(
                'No memlist vs contacts fee missmatches')


def ck_gmail(club):
    """
    Checks that the main db matches gmail with regard to
    members & applicants and other stati (e.g. inactive.)
    """
    applicant_set = club.g_by_group[club.APPLICANT_GROUP]
#   _ = input(f"applicant_set: {applicant_set}")
    applicant_missmatches = helpers.check_sets(
        applicant_set,
        club.applicant_with_email_set,  # populated by 
                                        # gather_membership_data
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
            club.ret, underline_char='=', extra_line=True)
        club.ret.extend(special_status_missmatches)
    else:
        club.ok.append("No special status missmatches")


    if applicant_missmatches or member_missmatches:
        helpers.add_header2list(
            "Missmatch: Gmail groups vs Club data",
            club.ret, underline_char='=', extra_line=True)
        club.ret.extend(member_missmatches + applicant_missmatches)
    else:
        club.ok.append(
                "No Google Groups vs Member/Applicant Missmatch.")


def ck_applicants(club):
    g_members = club.g_by_group[club.MEMBER_GROUP]
    g_applicants = club.g_by_group[club.APPLICANT_GROUP]
    keys = sorted(club.ms_by_status.keys(), reverse=True)
    for key in keys:
        if not (key in member.APPLICANT_SET):
            val = (club.ms_by_status.pop(key))
    applicants_by_status = helpers.keys_removed(
            club.applicants_by_status, ('m', 'zae'))
    applicants_by_status = helpers.lists2sets(applicants_by_status)
    ms_by_status_sets = helpers.lists2sets(club.ms_by_status)
    if applicants_by_status != ms_by_status_sets:
#       ### debugging ###
#       helpers.send2file(
#           '\n'.join(
#               sorted(
#                   [key for key in applicants_by_status.keys()])),
#           'applicants_by_status')
#       helpers.send2file(
#           '\n'.join(
#               sorted(
#                   [key for key in ms_by_status_sets.keys()])),
#           'ms_by_status_sets')
#       helpers.store(applicants_by_status,
#               'applicants_by_status.json')
#       helpers.store(ms_by_status_sets,
#               'ms_by_status_sets.json')
#       ### debugging ###
        club.ret.append("\nApplicant problem:")
#       club.ret.append("The following data from applicant SPoT-")
#       club.ret.extend(helpers.show_dict(applicants_by_status,
#                                               extra_line=False))
#       club.ret.append(
#               "- does not match the following membership SPot-")
#       club.ret.extend(helpers.show_dict(club.ms_by_status,
#                  extra_line=False))
#       club.ret.append("- End of comparison -")
        club.ret.append(helpers.compare_dicts(
            applicants_by_status, ms_by_status_sets,
            "applicant_spot", "membership_spot"))
    else:
        club.ok.append("No applicant problem.")


def ck_fees_spots(club):
    """
    Checks extra fees SPoTs against memlist data.
    Appends results to club.ret.
    """
    if (club.fees_by_category !=
            club.ms_by_fee_category):
        club_keys = set(club.fees_by_category.keys())
        file_keys = set(club.ms_by_fee_category.keys())
        if club_keys == file_keys:
            club.not_matching_notice = (
                "Fee amounts (by category) don't match")
            # traverse keys and report by name later
        else:
            club.ret.append("\nFees problem (by fee category):")
            club.ret.append("extra_fees_files:")
            club.ret.append(repr(club.fees_by_category))
            club.ret.append("###  !=  ###")
            club.ret.append("club.ms_by_fee_category:")
            club.ret.append(repr(club.ms_by_fee_category))
    else:
        club.ok.append("No fees by category problem.")
    if (club.fees_by_name != club.fee_category_by_m):
        club_keys = set(club.fees_by_name.keys())
        file_keys = set(club.fee_category_by_m.keys())
        if club_keys == file_keys:
            if club.fee_details:
                club.not_matching_notice = "Fee amounts don't match"
                # traverse keys and specify which amounts don't match
                sorted_club_keys = sorted([key for key in club_keys])
                for key in sorted_club_keys:
                    if (club.fees_by_name[key] !=
                            club.fee_category_by_m[key]):
                        club.varying_amounts.append('{}: {} != {}'
                            .format(
                                key,
                                club.fees_by_name[key],
                                club.fee_category_by_m[key]
                                ))
            else:
                club.not_matching_notice = (
            "Fee amounts don't match (try -d option for details)")
        else:
            club_set = set(club_keys)
            file_set = set(file_keys)
            club.ret.append("\nFees problem (by name):")
            club.ret.append(
                    "club.fee_category_by_m[club.NAME_KEY]:")
            sorted_keys = sorted(
                [key for key in club.fee_category_by_m.keys()])
            for key in sorted_keys:
                club.ret.append("{}: {}".format(key, 
                    club.fee_category_by_m[key]))
            club.ret.append("###  !=  ###")
            club.ret.append("club.fee_category_by_m:")
            for key, value in club.fee_category_by_m.items():
                club.ret.append("{}: {}".format(key, repr(value)))
    else:
        club.ok.append("No fees by name problem.")


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


def mail_only_keys(club):
    member.traverse_records(club.infile,
            (member.get_usps,  # populates club.usps_only
            ),
            club)  
    return helpers.collect_last_first_keys(club.usps_only)


def gather_contacts_data(club):    # used by ck_data #
    """
    The club attributes populated:
        g_by_name: /w values indexed by:
              ["email"] => email
              ["groups"] => set of labels
        g_by_group: keyed by labels /w values sets of names
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
            if (not(rec['status'] in member.APPLICANT_SET)
            and not club.all_applicants):
                continue
            name_key = member.fstrings['key'].format(**rec)
            if sponsors and name_key in sponsored:
                rec = add_sponsors(rec,
                        club.sponsors_by_applicant[name_key])
            club.applicant_data[name_key] = rec
        club.applicant_data_keys = club.applicant_data.keys()


def get_dict(source_file, sep=":", maxsplit=1):
    """
    # used by gather_extra_fees_data #
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


def gather_extra_fees_data(club):  # so far used only by ck_data
    # used to be populate_extra_fees; work towards convention:
    #   "populate" when only one &
    #   "gather" when more than one attribute is populated.
    """
    Populates club attrs fees_by_name & fees_by_category
    based on attr 'extra_fees_spots'..
    Tested by Tests.xtra_fees.py
    """
    def category(f):
        base, name = os.path.split(f)
        res = name.split('.')[0]
        return res

    fees_by_category = {}
    fees_by_name = {}

    for f in club.extra_fees_spots:
        res = get_dict(f)
        cat = category(f)
        for name, amt in res.items():
            # populate fees_by_name:
            _ = fees_by_name.setdefault(name, {})
            fees_by_name[name][cat] = int(amt)
            # populate fees_by_category
            _ = fees_by_category.setdefault(cat, {})
            fees_by_category[cat][name] = int(amt)
    club.fees_by_category = fees_by_category
    club.fees_by_name = fees_by_name


def populate_extra_fees(club):
    """
    ## plan to REDACT this in favour of gether_extra_fees_data
    Assumes <club> has attribute 'extra_fees_spots'.
    Populates club.by_name and club.by_category.
    Note also member.add2fee_data which (upon data traversal)
    populates club.fee_category_by_m and club.ms_by_fee_category.
    Both produce dicts in the same formats.
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


def output_extra_fees_report_by_name(club):
    """
    Client (utils.extra_fees_report_cmd) has already
    set all the options as attributes of club.
    """
    populate_extra_fees(club)
    by_name = club.by_name  # a dict (name keys) of
                            # dicts (fee keys => dollar amts)
    if club.json_file4output:
        with open(club.json_file4output, 'w') as stream:
            if not club.quiet:
                print('Data written to "{}".'.format(stream.name))
            json.dump(by_name, stream)

    name_keys = sorted(by_name.keys())

    if club.csv:
        if club.by_fee_category:
            print(
            "csv format not available for 'by_fee_category'")
        fieldnames = ["first","last","dock","kayak","mooring"]
        with open(club.csv_file4output, 'w', newline='') as f:
            dictwriter = csv.DictWriter(f, fieldnames)
            dictwriter.writeheader()
            for name in name_keys:
                names = helpers.tofro_first_last(name).split()
                rec = dict(first=names[0], last=names[1],
                        dock='', kayak='', mooring='')
                for key in by_name[name].keys():
                    rec[key] = by_name[name][key]
                dictwriter.writerow(rec)
            if not club.quiet:
                print(f"Data written to {f.name}")

    if club.text_file4output:
        res = []
        if club.include_headers:
            res.extend(["Members paying extra fees",
                        "=========================",
                        ])
        for name_key in name_keys:  # names alphabetically:
            fees = by_name[name_key]
            l = []
            for fee_key in sorted(fees.keys()):
                if club.include_fee_charged: # include fee amnts
                    l.append("{}: {}".format(fee_key, fees[fee_key]))
                else:
                    l.append("{}".format(fee_key))
            fees_paid = ', '.join(l)
            res.append("{}: {}".format(name_key, fees_paid))
        helpers.output('\n'.join(res),
                club.text_file4output, not club.quiet)


def output_extra_fees_report_by_category(club):
    """
    Client (utils.extra_fees_report_cmd) has already
    set all the options as attributes of club.
    """
    populate_extra_fees(club)
    by_category = club.by_category  # a dict (category keys) of
                            # dicts (name keys => dollar amts)
    if club.json_file4output:
        with open(club.json_file4output, 'w') as stream:
            if not club.quiet:
                print('Data written to "{}".'.format(stream.name))
            json.dump(by_category, stream)

    if club.csv_file4output:
        print(
"'--csv' and 'by_fee_category' are mutually exclusive options")
        sys.exit()

    if club.text_file4output:
        res = []
        if club.include_headers:
            res.extend(["Extra Fees (and who pays them)",
                        "==============================",
                        ])
        category_keys = sorted(by_category.keys())
        for category_key in category_keys:  #  alphabetically:
            names = by_category[category_key]
            if category_key == 'dock':
                header = (category_key +
                        ' (${})'.format(club.DOCK_FEE))
            elif category_key == 'kayak':
                header = (category_key +
                        ' (${})'.format(club.KAYAK_FEE))
            elif category_key == 'mooring':
               header = (category_key +
                       ' (fee varies)')
            else:
                print("Should never get here!!!!")
                sys.exit()
            res.append(header)
            for name_key in sorted(names.keys()):
                if (category_key == "mooring"
                and club.include_fee_charged): # include fee amnts
                    res.append("\t{}: {}".format(name_key, names[name_key]))
                else:
                    res.append("\t{}".format(name_key))

        helpers.output('\n'.join(res),
                club.text_file4output, not club.quiet)


def add_sponsors(rec, sponsors):
    """
    # used by populate_applicant_data #
    Returns a record with sponsor fields added.
    """
    first_last = [helpers.tofro_first_last(sponsor, as_key=False)
            for sponsor in sponsors]
    ret = helpers.Rec(rec)
    ret['sponsor1'] = first_last[0]
    ret['sponsor2'] = first_last[1]
    return ret

redacted = '''
def populate_applicant_data(club):
    """
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
        print('Reading file "{}"...'.format(stream.name))
        for line in helpers.useful_lines(stream, comment='#'):
            rec = applicant_data_line2record(line)
            name_key = member.fstrings['key'].format(**rec)
            if sponsors and name_key in sponsored:
                rec = add_sponsors(rec,
                        club.sponsors_by_applicant[name_key])
            club.applicant_data[name_key] = rec
        club.applicant_data_keys = club.applicant_data.keys()
'''

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


def line_of_meeting_dates(applicant_datum):
    """
    Returns a string: comma separated listing of meeting dates.
    """
    dates = []
    for date_key in Club.MEETING_DATE_NAMES:
        if applicant_datum[date_key]:
            dates.append(applicant_datum[date_key])
    return ', '.join(dates)


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


def ck_data(club):
    """
    Check integrity/consistency of of the Club's data bases:
    1.  MEMBERSHIP_SPoT  # the main club data base
    2.  CONTACTS_SPoT    # csv downloaded from gmail
    3.  APPLICANT_SPoT   #
    4.  SPONSORS_SPoT    #
    5.  EXTRA_FEES_SPoTs #
        ...
    The first 4 of the above all contain applicant data
    and must be checked for consistency.  Data in the 2nd
    and 5th must be consistent with that in the 1st.
    
    Returns a report (an array of lines) which (if <fee_details>
    is set to True) can be extended to include any discrepencies
    between what's billed each year vs what is still owed:
    useful after payments begin to come in.

    Consistency checks required:
    -memlist-    names emails stati&fees  which_fee&amt
    -contacts-   names emails  labels
    -sponsors-   names  (all sponsors (of current applicants) members?)
    -applicants- names        stati
    -extra_fees- names                    which_fee&amt
    [1] in future may keep records of non (no longer) members (and
    expired applicants.)
    """
#   print("Entering data.ck_data")
    club.ret = []
    club.ok = []
    club.varying_amounts = []
    club.not_matching_notice = ''
    helpers.add_header2list("Report Regarding Data Integrity",
                club.ret, underline_char='#', extra_line=True)
    gather_membership_data(club)  # from main data base
    gather_contacts_data(club)  # club gmail account contacts
    gather_extra_fees_data(club)  # data comes from SPoTs
    populate_sponsor_data(club)
    populate_applicant_data(club)
    club.applicants_by_status = get_applicants_by_status(club)


    ## First check that google groups match club data:
    # Deal with extra fees...
    ck_malformed(club)
    ck_fee_paying_labels(club)  # google groups vs club data
    ck_fees_spots(club)  # mem list vs extra fees SPoT
    # Keep in mind that after payment amounts won't match
    # Can use '-d' options for details.

   
    # Deal with applicants...
# if get a KeyError such as the following:
#     File "/home/alex/Git/Club/Utils/data.py", line ???, in ck_data
#       applicant_set = club.g_by_group[club.APPLICANT_GROUP]
#   KeyError: 'applicant'
# ... check that the contacts.cvs file came from the Club's gmail
# account, not someone else's!!!
    ck_gmail(club)


    ## do we compare gmail vs memlist emails anywhere????
    ## None of the following are populated!!!
    email_problems = []
    missing_emails = []
    non_member_contacts = []

    redact4now = '''
    if non_member_contacts:
        helpers.add_sub_list(
            "Contacts without a corresponding Member email",
            non_member_contacts, club.ret)
    else:
        club.ok.append('No contacts that are not members.')
    pass
    emails_missing_from_contacts = []
    common_emails = []

    if emails_missing_from_contacts:
        helpers.add_sub_list("Emails Missing from Google Contacts",
                             emails_missing_from_contacts, club.ret)
    else:
        club.ok.append("No emails missing from gmail contacts.")
'''

    ck_applicants(club)

    if club.ok:
        helpers.add_sub_list(
                "No Problems with the Following", club.ok, club.ret)
    ai_notice = "Acceptable Inconsistency"
    if club.not_matching_notice:
        helpers.add_header2list(ai_notice,
                                club.ret, underline_char='=')
        club.ret.append(club.not_matching_notice)
    if club.varying_amounts:
        helpers.add_header2list(
            "Fee Disparities: probably some have paid",
            club.ret, underline_char='-', extra_line=True)
        club.ret.extend(club.varying_amounts)
    return club.ret


def club_with_payables_dict(infile=None, args=None):
    """
    !?UNUSED?!
    Returns an instance of Club with required attributes:
        owing_dict     } both of which
        credits_dict   }  are dicts
    <args> provides for optional docopt args
    """
    club = Club(args)
    if infile: club.infile = infile
    club.owing_dict = {}
    club.credits_dict = {}
    err_code = member.traverse_records(club.infile,
                                       member.get_payables_dict,
                                       club)
    return club


def club_with_payables_listing(args=None, asterixUSPS=False):
    """
    Returns an instance of Club with required attributes:
        still_owing         } both of which
        advance_payments    }  are lists
    <args> provides for optional docopt args
    <asterixUSPS> if True adds an "*" to those without email
    """
    club = Club(args)
    club.still_owing = []
    club.advance_payments = []
    club.asterixUSPS = asterixUSPS
    err_code = member.traverse_records(club.infile,
                                       member.get_payables,
                                       club)
    return club


def payables_report(club, tabulate=False, max_width=None):
    ret = []
    if club.still_owing:
        helpers.add_header2list(
            "Members owing ({} in number)"
            .format(len(club.still_owing)),
            ret, underline_char='=', extra_line=True)
        if not max_width: max_width = 80
        else: max_width = int(max_width)
        if tabulate:
            tabulated = helpers.tabulate(club.still_owing,
                                         max_width=max_width,
                                         separator='  ')
            ret.extend(tabulated)
        else:
            ret.extend(club.still_owing)
    if club.advance_payments:
        ret.append("\n")
        ret.extend(["Members with a Credit",
                       "---------------------"])
        ret.extend(club.advance_payments)
#   print('\n'.join(ret))
    ret.append("\n\nReport prepared {}".format(helpers.date))
    ret.append(
            "(*) names ({}) with an asterix indicate usps vs email"
            .format(club.n_no_email))
    return ret



def restore_fees(club):
    """
    Sets up and leaves a new list of records in club.new_db:
    Dues and relevant fees are applied to each member's record.
    Also populates <club.name_set> & <club.errors>
    The <club.errors> includes names that are found in the
    <fees_json_file> but not in the <membership_csv_file> and 
    those still owing before new fees/dues are added.
    """
    print("Restore dues and fees to the data base...")
    club.errors = []; club.new_db = [];
    club.non0balance = {}; club.name_set = set();
    populate_extra_fees(club)
    club.extra_fee_names = set([key for key in club.by_name.keys()])
    err_code = member.traverse_records(club.infile, (
        member.populate_non0balance_func,
        member.populate_name_set_func,
        member.add_dues_fees2new_db_func,
        ), club)
    if club.non0balance:
        warning = "Non zero balances..."
#       print(warning)
        club.errors.append(warning)
        for name in sorted(club.non0balance.keys()):
            club.errors.append("{}: {}"
                    .format(name, repr(club.non0balance[name])))
    names_not_members = club.extra_fee_names - club.name_set
    if names_not_members:
        warning = "Not all listed as paying extra fees are members!"
#       print(warning)
        club.errors.append(warning)
        for name in names_not_members:
            club.errors.append(
                "\t{}: non member listed as paying fee(s)."
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
    """
    !?UNUSED?!
    """
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


def parse_kayak_data(raw_dict):
    """
    Modifies values in <raw_dict> as appropriate
    for the KAYAK.SPoT file.
    ## One time use for when fee has already been paid
    """
    for key in raw_dict.keys():
        value = raw_dict[key].split()
        l = len(value)
        if l > 2 or l < 1: assert False
        if value[-1] == '*': amt = 0
        else: amt = int(value[0])
        raw_dict[key] = amt


def populate_kayak_fees(club):
    """
    !?UNUSED?!
    NOTE: one time use; should be REDACTed!!!
    Parse club.KAYAK_SPoT and set up club.kayak_fees, a dict:
        keys- last/first name
        value- amount to be paid
    Lines terminating in an asterix have already paid
    and 'amount to be paid' for them should be 0.
    Must be referenced within func_dict.
    # Note: non kayak storage members should have a null in the
    # 'kayak' field of the main db.
    Format of each line in KAYAK_SPoT: "First Last:  AMT  [*]"
    """
    club.kayak_fees = parse_kayak_data(get_dict(club.KAYAk_SPoT))

func_dict = {
        "populate_kayak_fees": populate_kayak_fees,
        }


redact = '''
def exercise_ck_data(args=None):
    club = Club()
    if args and '-d' in args[1:]:
        club.fee_details = True
    club.format = member.fstrings['last_first']
    res = ck_data(club)
    for line in res:
        print(line)
'''

if __name__ == '__main__':
    print("data.py compiles without errors.")
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


