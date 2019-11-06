#!/usr/bin/env python3

# File: ck_data.py

"""
Provides automated access to the 
Bolinas Rod and Boat Club's data files:
Those identified by the constants ending in "SPoT".
Motivated by the desire to have a way of checking for data integrity,
it then morphed into a way of collecting data for presentation:
    eg list of applicants by number of meetings attended.
    
"""

import os
import csv
import member

MEMBERSHIP_SPoT = "Data/memlist.csv"
CONTACTS_SPoT = os.path.expanduser('~/Downloads/contacts.csv')
EXTRA_FEES_SPoT = "Data/extra_fees.txt"
APPLICANT_SPoT = "Data/applicants.txt"

FIELD_SEPARATOR = "|"   #} Depends on strict adhearance to 
status_adjustment = 4   #} formatting of APPLICANT_SPoT 
                        #} Essentially used to count number of
                        #} FIELD_SEPARATORs.
NAME_KEY = "by_name"
CATEGORY_KEY = "by_category"


class Club(object):
    """
    Used to hold data for subsequent processing, display, ...
    """
    def __init__(self):
        self.previous_name = ""  # Used to check that all entries in
                                 # data base csv file are ordered.


def gather_membership_data(member_csv_file, club):
    """
    Gathers the info we want from the membership csv file.
    Sets up three dict and one list attributes of the Club
    instance specified by club and then populates them by
    reading the member_csv_file:
        m_by_name is keyed by "name" /w another dict as its value
            one key is "email" with value as email
            the other " stati" with a list of stati as value.
        m_by_email is keyed by email /w set of "name"s as value.
        m_by_status is keyed by status /w a set (of (last, first)
        name as values.
        malformed is a list of (last, first) names identifying
        members whose record seems to be malformed (or out of order.)
        fee_by_category { keyed by category or name, values are a
        fee_by_name     { set of names or categories
    """
    club.m_by_name = dict()    #{ member emails keyed by (first, last)
                               #{ name
    club.m_by_email = dict()   # sets of member names keyed by email
    club.m_by_status = dict()  # sets of member names keyed by status 
    club.malformed = []
    club.without_email = []
    club.fee_by_category = {}
    club.fee_by_name = {}
    err_code = member.traverse_records(member_csv_file,
        (member.add2m_by_name, member.add2m_by_email,
        member.add2m_by_status, member.add2malformed,
        member.add2fee_sets),
        club)
    if err_code:
        print("Error condition! #{}".format(err_code))
#   print("TEST OUTPUT ...")  # all is in order
#   stati = club.m_by_status
#   for status in stati:
#       print(status)
#       for item in club.m_by_status[status]:
#           print(item)
#   print("... TEST OUTPUT")


def gather_contacts_data(contacts, club):
    """
    Gathers up the info we want from a gmail contacts.csv file.
    Sets up three dict attributes of the Club instance specified
    by club and then populates them by reading the gmail contacts
    csv file.
    In what follows, "name" == "{}, {}".format(last, first).
    The attributes are :
        g_by_name: keyed by "name" /w values indexed as follows:
          ["email"] => email
          ["groups] => set of group memberships
        g_by_email: keyed by email /w values each a set of "names".
        g_by_group_membership: keyed by group membership /w values
        each a set of "names" of contacts sharing that group membership.
    """
    club.g_by_name = dict()
    club.g_by_email = dict()
    club.g_by_group_membership = dict()

    # Traverse contacts.csv => g_by_email and g_by_name
    with open(contacts, 'r', encoding='utf-8') as file_obj:
#       google_reader = csv.DictReader(file_obj, restkey='status')
        google_reader = csv.DictReader(file_obj)
        print('DictReading Google contacts file "{}".'
            .format(file_obj.name))
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
            gname = "{}, {}".format(last_name, first_name)

            _ = club.g_by_email.setdefault(contact_email, set())
            club.g_by_email[contact_email].add(gname)
            club.g_by_name[gname] = dict(
                    email= contact_email, 
                    groups= group_membership)

            for key in group_membership:
                _ = club.g_by_group_membership.setdefault(key, [])
                club.g_by_group_membership[key].append(gname)


def gather_applicant_data(in_file):
    """
    Reads the in_file (APPLICANT_SPoT) and returns a dict With keys:
        "expired": list of applicants who've let applications expire.
        "applicants": a dict- set of applicants keyed by status.
            (Client will want to sort keys for presentation.)
    """
    expired_applications = []
    applicants = {}
    with open(in_file, 'r') as f_obj:
        print('Reading file "{}".'
            .format(f_obj.name))
        for line in f_obj:
            line = line.strip()
            if line:
#               print("Processing: {}".format(line))
                parts = [part.strip() for part in line.split(
                                        FIELD_SEPARATOR)]
#               print("parts: {}".format(repr(parts)))
                length = len(parts)
                if length > 2:
                    index = length - status_adjustment
                    try:
                        status = member.STATI[:5][index]
                    except IndexError:
#                       print("IndexError: {}".format(line))  # got none
                        continue
                    name = parts[0]
                    names = name.split()
                    if len(names) == 2:
                        first = names[0]
                        last = names[1]
                        last_first = "{}, {}".format(last, first)
                        last_segment = parts[-1]
#                       print("last_segment is '{}'"
#                           .format(last_segment))
                        if last_segment == "Application expired.":
                            expired_applications.append(last_first)
                        else:
                            _ = applicants.setdefault(status,set())
                            applicants[status].add(
                                "{}".format(last_first))
    return {"expired": expired_applications,  # just a list
            "applicants": applicants,  # sets keyed by status:
                        # client will want to sort the keys.
     # i.e. keys = sorted([key for key in data["applicants"]])
            }


def gather_extra_fees_data(in_file, without_fees=False):
    """
    Reads in_file and returns a dict with keys:
        "by_category": a dict keyed by category with
            each a set of (last_first, amount) tuples.
        "by_name": a dict keyed by name with
            each a set of (category, amount) tuples.
    If without_fees is True: then sets are not of tuples
    but rather just strings: last_first or category.

    Input file must have the following (that of
    Data/extra_fees.txt) format:

    Members paying for a Mooring:
    Michael Cook:  114
    ...

    Members paying for Dock privileges:
    Rick Butler:  75
    Jeff McPhearson:  75
    ...

    Members paying for Kayak storage:
    Doug Birch:  70
    Kathryn Cook:  70
    Jeff McPhearson:  70
    ...
    """
    by_name = {}
    by_category = dict(  # json version of input file
        Kayak= set(),
        Dock= set(),
        Mooring= set(),
        )
    categories = [key for key in by_category.keys()]

    with open(in_file, 'r') as f_obj:
        print('Reading file "{}".'.format(f_obj.name))
        line_number = 0
        category = ""
        for line in f_obj:
            line = line.strip()
            line_number += 1
            if not line:
                continue
            category_change = False
            if line[-1] == ':':  # category change
    #           print("Should get a category change...")
                words = line[:-1].split()
                for word in words:
                    if word in categories:
                        category = word
                        category_change = True
    #                   print("Switching category to '{}'."
    #                       .format(category))
                        continue
            else:  # Expect a name with fee for current category...
                parts = line.split(':')
    #           print(parts)
                fee = int(parts[1])
                names = parts[0].split()
                first_name = names[0]
                last_name = names[1]
                name_key = "{}, {}".format(last_name, first_name)
                _ = by_name.setdefault(name_key, set())
                _ = by_category.setdefault(category, set())
                if without_fees:
                    by_name[name_key].add(category)
                    by_category[category].add(name_key)
                else:
                    by_name[name_key].add((category, fee))
                    by_category[category].add((name_key, fee))
    return {"by_name": by_name,
           "by_category": by_category,
            }


def present_fees_by_name(extra_fees, raw=False):
    """
    Param would typically be the returned value of
    gather_extra_fees_data(infile)
    or its NAME_KEY value.
    Returns a text listing with or (if raw=True) without a header.
    """
    if NAME_KEY in extra_fees:
        jv = extra_fees[NAME_KEY]
    else:
        jv = extra_fees
    ret = []
    if not raw:
        ret.append("Extra fees by member:")
        ret.append("=====================")
    for key in jv:
        entry = key + ':'
        for value in jv[key]:
            entry = entry + " {} {}".format(value[0], value[1]) 
        ret.append(entry)
    return ret


def present_fees_by_category(extra_fees, raw=False):
    """
    Param would typically be the returned value of
    gather_extra_fees_data(infile)
    or its CATEGORY_KEY value.
    Returns a text listing with or (if raw=True) without a header.
    """
    if CATEGORY_KEY in extra_fees:
        jv = extra_fees[CATEGORY_KEY]
    else:
        jv = extra_fees
    categories = sorted([key for key in jv])
    ret = []
    if not raw:
        ret.append("Extra fees by category:")
        ret.append("=======================")
    for key in categories:
        ret.append('\n' + key)
        ret.append("-" * len(key))
        for value in jv[key]:
            ret.append("{0}: ${1}".format(*value))
    return ret


def present_expired(list_of_expired_applications, raw=False):
    """
    Returns a list of strings which can be "\n".join(ed).
    It's expected that the parameter will be the the following:
    gather_applicant_data(APPLICANT_SPoT)["expired"]
    which is just a list of last_first names.
    """
    if raw:
        ret = []
    else:
        ret = ["Applicants whos applications have expired:",
               "=========================================="]
    for name in list_of_expired_applications:
        ret.append(name)
    return ret


def present_applicants(applicants_keyed_by_status, raw=False):
    """
    Returns a list of strings which can be "\n".join(ed).
    It's expected that the parameter will be the the following:
    gather_applicant_data(APPLICANT_SPoT)["applicants"]
    which is a dict keyed by status /w each value => set
    of last_first names.
    """
    if raw:
        ret = []
    else:
        ret = ["Applicants by status:",
               "====================="]
    keys = sorted([key for key in applicants_keyed_by_status])
    for key in keys:
        if not raw:
            ret.append("")
        ret.append("{}:".format(key))
        values = sorted(list(applicants_keyed_by_status[key]))
        for value in values:
            ret.append("{}".format(value))
    return ret



def add2problems(problem_header, problem_list, problems,
                underline_with="=",
                raw=False, line_or_formfeed="\n",
                preface_w_linefeed=True):
    if problem_list:
        if preface_w_linefeed:
            problems.append(line_or_formfeed)
        if not raw:
            problems.append(problem_header)
            problems.append(underline_with * len(problem_header))
        problems.extend(problem_list)


def ck_data(member_csv_file,
            contacts_csv_file,
            extra_fees_txt_file,
            applicants_txt_file,
            report_status=True,
            raw=False,
            line_or_formfeed="\n"):
    """
    Check integrity/consistency of of the Club's data base(s.)
    (Meant to replace ck_fields and compare_gmail as well as 
    dealing with 'extra_fees'/'extra_charges', applicant 'stati',
    and perhaps other things.
    We collect data from the membership data base (memlist.csv)
    and compare it with data collected from other sources,
    specifically:
        gmail contacts
        applicants.txt
        extra_fees.txt
        ...
    """
    club = Club()
    ret = ["Checking data integrity...\n"]

    # Collect data:
    gather_membership_data(member_csv_file, club)
    gather_contacts_data(contacts_csv_file, club)

    # Deal with MEMBERSHIP data-
    # First check for malformed records:
    if not club.malformed:
        ret.append("No malformed records found.")
    else:
        add2problems("Malformed Records", club.malformed, ret,
            underline_with="=", raw=False, line_or_formfeed="\n")
    
    # Catch problem cases & set ==> one name for each email.
    dangling_m_email = []
    shared_m_email = []
    for m_email in club.m_by_email:
        n_in_set = len(club.m_by_email[m_email])
        if n_in_set == 0:
            dangling_m_email.append(m_email)
        elif n_in_set ==1:
            club.m_by_email[m_email] = club.m_by_email[m_email].pop()
        else:
            names = ", ".join(sorted(
                [name for name in club.m_by_email[m_email]]))
            shared_m_email.append("{} <== [{}]"
                .format(m_email, names))
    add2problems("Dangling Member Email(s)", dangling_m_email, ret,
            underline_with="=", raw=False, line_or_formfeed="\n")
    add2problems("Shared Member Email(s)", shared_m_email, ret,
            underline_with="=", raw=False, line_or_formfeed="\n")

    # Deal with (gmail) CONTACTS data
    # Catch problem cases & set ==> one name for each email.
    #### NOTE: Seems to not be picking up contacts  ####
    #### entered twice with differing emails.       ####
    dangling_g_email = []
    shared_g_email = []
    for g_email in club.g_by_email:
        n_in_set = len(club.g_by_email[g_email])
        if n_in_set == 0:
            dangling_g_email.append(g_email)
        elif n_in_set ==1:
            club.g_by_email[g_email] = club.g_by_email[g_email].pop()
        else:
            names = ", ".join(sorted(
                [name for name in club.g_by_email[g_email]]))
            shared_g_email.append("{} <== [{}]"
                .format(g_email, names))
    add2problems("Dangling Contact Email(s)", dangling_g_email, ret,
            underline_with="=", raw=False, line_or_formfeed="\n")
    add2problems("Shared Contact Email(s)", shared_g_email, ret,
            underline_with="=", raw=False, line_or_formfeed="\n")

    # Provide listing of those with 'stati':
    if report_status:
        ret.append(line_or_formfeed)
        if not raw:
            ret.extend(["Members /w 'status' Content",
                        '==========================='])
        stati_w_members = sorted(club.m_by_status.keys())
#       print("Stati w members: {}".format(repr(stati_w_members)))
        for key in stati_w_members:
            add2problems(("\n" + key), 
                [member for member in club.m_by_status[key]], ret,
            underline_with="-", raw=False, line_or_formfeed="\n",
            preface_w_linefeed=False)


    # Compare gmail vs memlist emails and then memlist vs gmail
    # now that both listings have names rather than sets of names:
    email_problems = []
    missing_emails = []
    non_member_contacts = []
    emails_missing_from_contacts = []
    common_emails = []

    for m_email in club.m_by_email:
        m_name = club.m_by_email[m_email]  # member name
        try:
            g = club.g_by_email[m_email]  # contact name
        except KeyError:
            emails_missing_from_contacts.append(
                "{} ({})".format(m_email, m_name))

    add2problems("Emails Missing from Contacts",
            emails_missing_from_contacts, ret,
            underline_with="=", raw=False, line_or_formfeed="\n")

    for g_email in club.g_by_email:
        g = club.g_by_email[g_email]  # contact name
        try:
            m = club.m_by_email[g_email]  # member name
        except KeyError:
            non_member_contacts.append("{} ({})"
                    .format(g_email, g))
     
    # Compare results of the next sets of data with
    # membership data already collected:
    extra_fees_info = gather_extra_fees_data(
                    extra_fees_txt_file, without_fees=True)
    applicants_by_status = gather_applicant_data(
                                    APPLICANT_SPoT)["applicants"]
    
    keys = [key for key in club.m_by_status.keys()]
    temp_ret = []
    for key in keys:
        if not 'a' in key:
            val = (club.m_by_status.pop(key))
            temp_ret.append(key)
    if temp_ret:
        ret.append("\nNon Applicant Stati: {}"
            .format(','.join(temp_ret)))
    if applicants_by_status != club.m_by_status:
        ret.append("\nApplicant problem:")
        ret.append("The following-")
        ret.extend(applicants_by_status)
        ret.append("- is not the same as what follows-")
        ret.extend(club.m_by_status)
        ret.append("- End of comparison -")
    else:
        ret.append("\nNo applicant problem.")

    add2problems("Contacts that are Not Members",
            non_member_contacts, ret,
            underline_with="=", raw=False, line_or_formfeed="\n")
            
    if ((extra_fees_info["by_category"] != club.fee_by_category) or
                (extra_fees_info["by_name"] != club.fee_by_name)):
        ret.append("\nFees problem:")
        ret.append(repr(extra_fees_info["by_category"]))
        ret.append(repr(club.fee_by_category))
    else:
        ret.append("\nNo fees problem.")
    return ret


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


def compare(data1, data2, underline_char='=', inline=False):
    ret = []
    if data1 == data2:
        ret.append("Good News: data1 == data2")
    else:
        ret.append("Bad News: data1 != data2")
    ret.append("\nListing1...")
    ret.append(data_listed(data1, underline_char, inline))
    ret.append("\nListing2...")
    ret.append(data_listed(data2, underline_char, inline))
    ret.append("... end of listings")
    return ret


def ret2file(ret, outfile):
    with open(outfile, 'w') as f_obj:
        f_obj.write("\n".join(ret))
    print("Results written to '{}'."
        .format(f_obj.name))

def test_extras():
    club = Club()
    ret = []
    gather_membership_data(MEMBERSHIP_SPoT, club)
    data = club.fee_by_category
#   print("\n".join(data_listed(data)))
    return data_listed(data)

#   return
    extra_fees_data = gather_extra_fees_data(
        EXTRA_FEES_SPoT, without_fees=True)
    ret.append("\nmemlist compared to extra_fees file by Category:")
    ret.extend(compare(club.fee_by_category,
            extra_fees_data["by_category"]))
    ret.append("\nmemlist compared to extra_fees file by Name:")
    ret.extend(compare(club.fee_by_name,
            extra_fees_data["by_name"], inline=True))


def test_ck_data(outfile):
    ret2file(ck_data(
                MEMBERSHIP_SPoT,
                CONTACTS_SPoT,
                EXTRA_FEES_SPoT,
                APPLICANT_SPoT),
            outfile)
#   print("Call to ck_integrity has returned...")
#   print(res)
#   return res


def list_mooring_data(extra_fees_spot):
    extra_fees_data = gather_extra_fees_data(
        extra_fees_spot, without_fees=False)
#   data = extra_fees_data["by_category"]
#   print(repr(data["Mooring"]))
    mooring_data = extra_fees_data["by_category"]["Mooring"]
    return sorted(
#       ["{} - {}".format(datum[0], datum[1]) for datum in mooring_data])
        ["{0} - {1}".format(*datum) for datum in mooring_data])

    
def test_list_mooring():
    return list_mooring_data(EXTRA_FEES_SPoT )


def test_fees_by():
    ret = []
    data = gather_extra_fees_data(EXTRA_FEES_SPoT)
    by_name0= present_fees_by_name(data)
    by_category0= present_fees_by_category(data)
    by_name1= present_fees_by_name(data[NAME_KEY])
    by_category1= present_fees_by_category(data[CATEGORY_KEY])
    ret.append("\nBy Name (0)...")
    ret.extend(by_name0)
    ret.append("\nBy Name (1)...")
    ret.extend(by_name1)
    ret.append("\nBy Category (0)...")
    ret.extend(by_category0)
    ret.append("\nBy Category (1)...")
    ret.extend(by_category1)
    return ret


def test_applicant_presentations():
    ret = []
    data = gather_applicant_data(APPLICANT_SPoT)
    ret.extend(present_applicants(data["applicants"]))
    ret.append("\n\n")
    ret.extend(present_expired(data["expired"]))
    return ret


def test_applicants_incl_expired():
    expired = present_expired(
        gather_applicant_data(APPLICANT_SPoT)["expired"])
    applicants = present_applicants(
        gather_applicant_data(APPLICANT_SPoT)["applicants"])
    ret = ["\nExpired Applications..."]
    ret.extend(expired)
    ret.append("\nApplicants...")
    ret.extend(applicants)
    return ret
    

def ck_all():
    n = 0
    for test_routine in (
        test_applicant_presentations,  #1
        test_applicants_incl_expired,  #2
        test_extras,                   #3
        test_ck_data,                  #4
        test_fees_by,                  #5
        test_list_mooring,             #6
    ):
        n += 1
        print("Test #{}: {}".format(n, test_routine.__name__))
        res = "\n".join(test_routine())
        file_name = "2check{}".format(str(n))
        with open(file_name, "w") as f_obj:
            header = "Result of ({}) {}...".format(n,
                test_routine.__name__)
            f_obj.write(header + "\n")
            f_obj.write("=" * len(header) + "\n")
            f_obj.write(res)


if __name__ == "__main__":

#   ck_all()
#   club = Club()
    
#   test_applicant_presentations()
#   test_applicants_incl_expired()
#   test_extras()
    test_ck_data("2check")
#   test_fees_by()
#   test_list_mooring()    
#   applicants = gather_applicant_data(APPLICANT_SPoT)
#   print(repr(applicants))

   

