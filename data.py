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
import csv
import helpers
import member
from rbc import Club


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
    club.email_by_m = {} # m => str (email)
    club.stati_by_m = {} # m => set (stati)
    # lists (no need to sort since members and fees are ordered):
    club.fee_category_by_m = {}  # m => list (fee_categories /w fee)
    club.ms_by_email = {}  # email => list (members)
    club.ms_by_status = {}  # status => list (members)
    club.ms_by_fee_category = {}  # fee_category => list (members)

    club.malformed = []  # populated by member.add2malformed
    club.without_email = []  # populated by member.add2email_data
    club.napplicants = 0  # incremented prn by member.add2ms_by_status

    err_code = member.traverse_records(club.MEMBERSHIP_SPoT,
        (member.add2email_data,
        member.add2fee_data,
        member.add2status_data,
        member.add2malformed,  ),
        club)
    if err_code:
        print("Error condition! #{}".format(err_code))


def get_gmail_record_info(g_rec):
    """
    <g_rec> is a record from the gmail contacts file.
    Returns a dict with only the info we need.
    """
    g_email = g_rec["E-mail 1 - Value"]
    group_membership = (
        g_rec["Group Membership"].split(" ::: "))
    if (group_membership
    and group_membership[-1] =='* myContacts'):
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
    return dict(
        gname= gname,
        g_email= g_email,
        groups= group_membership,
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
        g_by_email: keyed by email /w values each a set of "names".
        g_by_group: keyed by group membership /w values
        each a set of "names" of contacts sharing that group membership.
    """
    club.g_by_name = dict()  # ea value is a dict --["email"] > email
    club.g_by_email = dict() # >set of names  #   \ ['groups'] > set
    club.g_by_group = dict() # >set of names

    # Traverse contacts.csv => g_by_email and g_by_name
    with open(club.CONTACTS_SPoT, 'r', encoding='utf-8') as file_obj:
#       google_reader = csv.DictReader(file_obj, restkey='status')
        google_reader = csv.DictReader(file_obj)
        print('DictReading Google contacts file "{}".'
            .format(file_obj.name))
        for g_rec in google_reader:
            g_dict = get_gmail_record_info(g_rec)

            _ = club.g_by_email.setdefault(g_dict["g_email"], set())
            club.g_by_email[g_dict["g_email"]].add(g_dict["gname"])
            club.g_by_name[g_dict["gname"]] = dict(
                    email= g_dict["g_email"], 
                    groups= g_dict["groups"])

            for key in g_dict["groups"]:
                _ = club.g_by_group.setdefault(key, set())
                club.g_by_group[key].add(g_dict["gname"])


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
        for raw_line in f_obj:
            line = raw_line.strip()
            if line:
#               print("Processing: {}".format(line))
                parts = [part.strip() for part in line.split(
                                        Club.SEPARATOR)]
                if not parts[-1]:       #} neutilizes empty field
                    parts = parts[:-1]  #} after trailing SEPARATOR
#               print("parts: {}".format(repr(parts)))
                length = len(parts)
                if length > 2:  # to exclude non applicants (name|appl|fee)
                    index = length - Club.N_SEPARATORS
#                   print(length)
                    try:
                        status = member.APPLICANT_STATI[index]
                    except IndexError:
#                       print("IndexError: {}".format(line))  # got none
                        continue
                    name = parts[0]
                    names = name.split()
                    if len(names) == 2:
                        last_first = ", ".join((names[1], names[0]))
#                       print("Processing '{}'.".format(last_first))
                        last_segment = parts[-1]
#                       print("last_segment is '{}'"
#                           .format(last_segment))
                        if last_segment == "Application expired.":
                            expired_applications.append(last_first)
                        else:
                            _ = applicants.setdefault(status,set())
#                           print("Adding '{}'.".format(last_first))
                            applicants[status].add(last_first)
                    elif name:
                        print(
                        "Difficulty processing applicant '{}' in line:"
                                .format(name))
#                       print(raw_line)
    return {"expired": expired_applications,  # just a list
            "applicants": applicants,  # sets keyed by status:
                        # client will want to sort the keys.
     # i.e. keys = sorted([key for key in data["applicants"]])
            }


def gather_extra_fees_data(in_file, without_fees=False):
    """
    Reads in_file and returns a dict with keys:
        CATEGORY_KEY: a dict keyed by category with
            each a set of (last_first, amount) tuples.
        NAME_KEY: a dict keyed by name with
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
    return {Club.NAME_KEY: by_name,
           Club.CATEGORY_KEY: by_category,
            }


def present_fees_by_name(extra_fees, raw=False):
    """
    Param would typically be the returned value of
    gather_extra_fees_data(infile)
    or its NAME_KEY value.
    Returns a text listing with or (if raw=True) without a header.
    """
    if Club.NAME_KEY in extra_fees:
        jv = extra_fees[Club.NAME_KEY]
    else:
        jv = extra_fees
    ret = []
    if not raw:
        ret.append("Extra fees by member:")
        ret.append("=====================")
    for key in jv:
        charges = []
        for value in jv[key]:
            charges.append("{} {}".format(value[0], value[1]))
        charges = ', '.join(charges)
        ret.append(key + ': ' + charges)
    return ret


def present_fees_by_category(extra_fees, raw=False):
    """
    Param would typically be the returned value of
    gather_extra_fees_data(infile)
    or its CATEGORY_KEY value.
    Returns a text listing with or (if raw=True) without a header.
    """
    if Club.CATEGORY_KEY in extra_fees:
        jv = extra_fees[Club.CATEGORY_KEY]
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



def add2problems(problem_header, new_problems, problem_list,
                separator=[""], underline_with=["="], raw=False):
    """
    Extends an existing <problem_list> with a sorted version of
    <new_problems>.
    The added part is separated from the original by <separator> which
    must be a (possibly empty) list of strings- it defaults to a
    list of one empty string.
    If <problem_header> is not an empty empty string it will be used
    as a header separated from the ensuing list by what is defined by
    <underline_with> which must be a list (possibly empty.) If not
    empty, the first item of this list should be a single character,
    typically "=" or "-" which will be expanded to the length of
    <problem_header> (serving as an underline) and then followed by
    the remaining part of the list (if there is any.)
    """
    if problem_list:
#       print("Extending '{}' with:".format(problem_header))
#       print(repr(new_problems))
        if separator:
            problem_list.extend(separator)
        if problem_header:
            problem_list.append(problem_header)
            if underline_with:
                problem_list.append(underline_with[0] *
                    len(problem_header))
                problem_list.extend(underline_with[1:])
        problem_list.extend(new_problems)


def remove_unwanted_items(dictionary, list_of_keys,
                            ignore_keyerror=True):
    """
    Rids the dictionary of listed keys.
    Key errors are ignored.
    """
    for key in list_of_keys:
        if ignore_keyerror:
            try:
                del dictionary[key]
            except KeyError:
                pass
        else:
            del dictionary[key]


def first_parts_only(sequence):
    return [item.split(' ')[0] for item in sequence]


def ck_applicants(club, # provides data from memlist and gmail
           applicants): # gather_applicant_data(SPoT, "applicants")
    """
    The 'club' parameter assumes gather_membership_data
    and gather_contacts_data functions have been run in order to
    populate the following club attributes:
        club.ms_by_status
        club.m_by_group
    and also that the client has run the gather_applicant_data
    function to provide the 'applicants' parameter.
    """
    m_applicants = club.ms_by_status
    a_applicants = applicants
    g_applicants = club.m_by_group["applicant"]


def ck_applicants_cmd():
    """
    Driver for ck_applicants function.
    """
    club = Club()
    gather_contacts_data(club)
    gather_membership_data(club)
    a_by_status = gather_applicant_data(
            club.APPLICANT_SPoT)['applicants']
    ret = []
    g_set = club.g_by_group[club.APPLICANT_GROUP]
    m_set = set()  # applicants per the membership db
    a_set = set()  # applicants per the applicant SPoT

    if club.ms_by_status == a_by_status:
        ret.append("\n Club records match applicant SPoT")

    for key in club.ms_by_status:
        if 'a' in key:
            m_set = m_set.union(club.ms_by_status[key])
    for key in a_by_status:
        if 'a' in key:
            a_set = a_set.union(a_by_status[key])
    if g_set == m_set:
        ret.append("\nContacts match Club records.")
    else:
        ret.append("\nContacts do NOT match Club records.")
    if g_set == a_set:
        ret.append("\nContacts match applicant file.")
    else:
        ret.append("\nContacts do NOT match applicant file.")

    ck_applicants(club, a_by_status)




def ck_data(club,
            report_status=True,
            raw=False,
            formfeed=False):
    """
    Check integrity/consistency of of the Club's data bases:
        MEMBERSHIP_SPoT  # the main club data base
        CONTACTS_SPoT    # csv downloaded from gmail
        APPLICANT_SPoT   #
        EXTRA_FEES_SPoT  #
        ...
    The first 3 of the above all contain applicant data
    and must be checked for consistency.
    Data in each of the 2nd and 4th are compared with
    the first and checked.
    Returns a report in the form of an array of lines.
    """
    club = Club()
    ret = ['']
    first_line = "Report Regarding Data Integrity"
    if not (raw or formfeed):
        ret.append(first_line)
        ret.append("#" * len(first_line))
        ret.append('')
    ok = []

    # Collect data from csv files ==> club attributes
    gather_membership_data(club)
    gather_contacts_data(club)

    # Collect data from custom files ==> local variables
    extra_fees_info = gather_extra_fees_data(club.EXTRA_FEES_SPoT,
                    without_fees=True)
    a_applicants = gather_applicant_data(
                                club.APPLICANT_SPoT)["applicants"]

    # Deal with MEMBERSHIP data-
    # First check for malformed records:
    if not club.malformed:
        ok.append("No malformed records found.")
    else:
        print("Found Malformed Records.")
        add2problems("Malformed Records", club.malformed, ret)
    
    # Catch problem cases & change from set to one name for each email.
    dangling_m_emails = []   # email without a name
                             # can't imagine how that could happen
    shared_m_emails = []  # email owned by more than one person
    for m_email in club.ms_by_email:
        n_emails = len(club.ms_by_email[m_email])
        if n_emails == 0:
            print(
            "Adding a dangling (no associated member name) email.")
            dangling_m_emails.append(m_email)
        elif n_emails ==1:
            club.ms_by_email[m_email] = club.ms_by_email[m_email].pop()
        else:
            names = "; ".join(sorted(
                [name for name in club.ms_by_email[m_email]]))
            shared_m_emails.append("{} <== [{}]"
                .format(m_email, names))
    if dangling_m_emails:
        print("Found Dangling Member Emails")
        add2problems("Dangling Member Email(s)",
                        dangling_m_emails, ret)
        remove_unwanted_items(club.ms_by_email, dangling_m_emails,
            ignore_keyerror=False)
    if shared_m_emails:
        print("Found Shared Member Emails")
        add2problems("Shared Member Email(s)", shared_m_emails, ret)
        remove_unwanted_items(club.ms_by_email,
                    first_parts_only(shared_m_emails),
                        ignore_keyerror=False)

    # Deal with (gmail) CONTACTS data
    # Catch problem cases & set ==> one name for each email.
    #### NOTE: Seems to not be picking up contacts  ####
    #### entered twice with differing emails.       ####
    dangling_g_emails = []
    shared_g_emails = []
    for g_email in club.g_by_email:
        n_emails = len(club.g_by_email[g_email])
        if n_emails == 0:
            dangling_g_emails.append(g_email)
        elif n_emails ==1:
            club.g_by_email[g_email] = club.g_by_email[g_email].pop()
        else:
            names = "; ".join(sorted(
                [name for name in club.g_by_email[g_email]]))
            shared_g_emails.append("{} <== [{}]"
                .format(g_email, names))
    if dangling_g_emails:
        print("Found Dangling Contact Emails")
        add2problems("Dangling Contact Email(s)",
                        dangling_g_emails, ret)
        remove_unwanted_items(club.g_by_email,dangling_g_emails,
            ignore_keyerror=False)
    if shared_g_emails:
        print("Found Shared Contact Emails")
        add2problems("Shared Contact Email(s)", shared_g_emails, ret)
        remove_unwanted_items(club.g_by_email, 
                        first_parts_only(shared_g_emails),
                            ignore_keyerror=False)

    # Provide listing of those with 'stati':
    if report_status:
        if formfeed:
            ret.append('')
        if not raw:
            ret.extend(["",
                        "Members /w 'status' Content",
                        '==========================='])
        members_w_status = sorted(club.ms_by_status.keys())
#       print("Members w status: {}".format(repr(members_w_status)))
        for key in members_w_status:
#           print("Adding members by stati")
            add2problems(key, 
                sorted([member for member in club.ms_by_status[key]]),
                ret,
                underline_with=["-"])


    # Compare gmail vs memlist emails and then memlist vs gmail
    # now that both listings have names rather than sets of names:
    email_problems = []
    missing_emails = []
    non_member_contacts = []
    emails_missing_from_contacts = []
    common_emails = []

    for m_email in club.ms_by_email:
        m_name = club.ms_by_email[m_email]  # member name
        try:
            g = club.g_by_email[m_email]  # contact name
        except KeyError:
            emails_missing_from_contacts.append(
                "{} ({})".format(m_email, m_name))

    if emails_missing_from_contacts:
        add2problems("Emails Missing from Google Contacts",
                emails_missing_from_contacts, ret)
    else:
        ok.append("No emails missing from gmail contacts.")

    for g_email in club.g_by_email:
        g = club.g_by_email[g_email]  # contact name
        try:
            m = club.ms_by_email[g_email]  # member name
        except KeyError:
            non_member_contacts.append("{} ({})"
                    .format(g_email, g))
     
    # Compare results gleened from  files:
    # 'extra_fees_info' and 'a_applicants
#   for key in a_applicants:
#       print(key)
#       for entry in a_applicants[key]:
#           print(repr(entry))
    
    # Check that gmail contacts' "groups" match membership data:
######  Following code could be refactored, perhaps /w Walrus!!#####
    m_applicants = set()
    for key in club.ms_by_status:
#       print(key)
        if 'a' in key:
#           print("key chosen")
            for member in club.ms_by_status[key]:
                m_applicants.add(member)
### The following should be checked for equivalence and    ###
### if different, they need to be reported in the output-  ###
### left here for time being until Data can be corrected.  ###
    if m_applicants == set(
            club.g_by_group[club.APPLICANT_GROUP]):
        ok.append("Gmail groups match Club data")
    else:
        ret.append("\nMismatch: Gmail groups vs Club data")
        ret.append(  "===================================")
        ret.append('')
        ret.append("Gmail groups")
        ret.append("------------")
        ret.extend(sorted(list(
            club.g_by_group[club.APPLICANT_GROUP])))
        ret.append('')
        ret.append("Club status")
        ret.append("-----------")
        ret.extend(sorted(list(m_applicants)))
#       print(
#       "The following two (sorted) sets should be the same- They're NOT!")
#       print(sorted(list(m_applicants)))
#       print(sorted(list(club.g_by_group[APPLICANT_GROUP])))
#       print()

    g_members = club.g_by_group[club.MEMBER_GROUP]
    g_applicants = club.g_by_group[club.APPLICANT_GROUP] 
    keys = [key for key in club.ms_by_status.keys()]
#   temp_ret = []
    for key in keys:
        if not 'a' in key:
            val = (club.ms_by_status.pop(key))
#           temp_ret.append(key)
#   if temp_ret:
#       ret.append("\nNon Applicant Stati: {}"
#           .format(','.join(temp_ret)))
    if a_applicants != club.ms_by_status:
        ret.append("\nApplicant problem:")
        ret.append("The following-")
        ret.extend(helpers.show_dict(a_applicants))
        ret.append("- is not the same as what follows-")
        ret.extend(helpers.show_dict(club.ms_by_status))
        ret.append("- End of comparison -")
    else:
        ok.append("No applicant problem.")

    if non_member_contacts:
        add2problems("\nContacts that are Not Members",
                non_member_contacts, ret)
    else:
        ok.append('No contacts that are not members.')
            
    if ((extra_fees_info[club.CATEGORY_KEY] !=
            club.ms_by_fee_category)
    or (extra_fees_info[club.NAME_KEY] !=
            club.fee_category_by_m)):
        ret.append("\nFees problem:")
        ret.append(repr(extra_fees_info[club.CATEGORY_KEY]))
        ret.append(repr(club.ms_by_fee_category))
    else:
        ok.append("No fees problem.")

    if ok:
        add2problems("No Problems with the Following", ok, ret)
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
    ret.extend(data_listed(data1, underline_char, inline))
    ret.append("\nListing2...")
    ret.extend(data_listed(data2, underline_char, inline))
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
    gather_membership_data(club)
    data = club.fee_by_category
#   print("\n".join(data_listed(data)))
    return data_listed(data)

#   return
    extra_fees_data = gather_extra_fees_data(
        EXTRA_FEES_SPoT, without_fees=True)
    ret.append("\nmemlist compared to extra_fees file by Category:")
    ret.extend(compare(club.fee_by_category,
            extra_fees_data[Club.CATEGORY_KEY]))
    ret.append("\nmemlist compared to extra_fees file by Name:")
    ret.extend(compare(club.fee_by_name,
            extra_fees_data[Club.NAME_KEY], inline=True))


def test_ck_data():
    club = Club
    return ck_data(club)
#   print("Call to ck_integrity has returned...")
#   print(res)
#   return res


def list_mooring_data(extra_fees_spot):
    extra_fees_data = gather_extra_fees_data(
        extra_fees_spot, without_fees=False)
#   data = extra_fees_data[Club.CATEGORY_KEY]
#   print(repr(data["Mooring"]))
    mooring_data = extra_fees_data[Club.CATEGORY_KEY]["Mooring"]
    return sorted(
#       ["{} - {}".format(datum[0], datum[1]) for datum in mooring_data])
        ["{0} - {1}".format(*datum) for datum in mooring_data])

    
def test_list_mooring():
    return list_mooring_data(Club.EXTRA_FEES_SPoT )


def test_fees_by():
    ret = []
    data = gather_extra_fees_data(Club.EXTRA_FEES_SPoT)
    by_name0= present_fees_by_name(data)
    by_category0= present_fees_by_category(data)
    by_name1= present_fees_by_name(data[Club.NAME_KEY])
    by_category1= present_fees_by_category(data[Club.CATEGORY_KEY])
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
    data = gather_applicant_data(Club.APPLICANT_SPoT)
    ret.extend(present_applicants(data["applicants"]))
    ret.append("\n\n")
    ret.extend(present_expired(data["expired"]))
    return ret


def test_applicants_incl_expired():
    expired = present_expired(
        gather_applicant_data(Club.APPLICANT_SPoT)["expired"])
    applicants = present_applicants(
        gather_applicant_data(Club.APPLICANT_SPoT)["applicants"])
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

    ck_all()
#   club = Club()
    
#   test_applicant_presentations()
#   test_applicants_incl_expired()
#   test_extras()
#   test_fees_by()
#   test_list_mooring()    
#   applicants = gather_applicant_data(APPLICANT_SPoT)
#   print(repr(applicants))

#   test_ck_data("2check")
   

