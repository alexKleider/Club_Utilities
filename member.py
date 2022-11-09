#!/usr/bin/env python3

# File: member.py

"""
Applies to records of members of 'the club' which
is further defined in another module (rbc.py).
(Most?) functions in this module pertain to member records and many
(so called 'collector' functions) store data in one or more attributes
of instances of rbc.Club so hence the extra (named) parameter set to
'club=None' when it's not needed.
"""

import os
import csv
import json
import helpers
import sys_globals as glbs
from rbc import Club
import data

NO_EMAIL_KEY = 'no_email'

STATUS_KEY_VALUES = {
    "a-": "Application received without fee", #0
    "a" : "Application complete but not yet acknowledged",
                # temporary until letter of welcome is sent
    "a0": "Applicant (no meetings yet)",  # welcomed
    "a1": "Attended one meeting",
    "a2": "Attended two meetings",
    "a3": "Attended three (or more) meetings",
    "ai": "Inducted, needs to be notified",  # temporary until letter
    "ad": "Inducted & notified, membership pending payment of dues",
    "av": "Vacancy ready to be filled pending payment of dues",
    "aw": "Inducted & notified, awaiting vacancy", #7 > #8
    "am": "New Member",  # temporary until congratulatory letter.
    "be": "Email on record being rejected",   # => special notice
    "ba": "Postal address => mail returned",  # => special notice
    "h" : "Honorary Member",                             #10 > #12
    'm' : "Inactive (continuing to receive minutes)",
    'r' : "Retiring/Giving up Club Membership",
    't' : "Membership terminated (probably non payment of fees)",
            # a not yet implemented temporary
            # status to trigger a regret letter
    "w" : "Fees being waived",  # a rarely applied special status
    'z1_pres': "President",
    'z2_vp': "VicePresident",
    'z3_sec': "Secretary of the Club",  # not used under Rafferty
    'z4_treasurer': "Treasurer",
    'z5_d_odd': "Director- term ends next odd year",
    'z6_d_even': "Director- term ends next even year",
    'zae': "Application expired or withdrawn",
    'zzz': "No longer a member"
    }
STATI = sorted([key for key in STATUS_KEY_VALUES.keys()])
SPECIAL_NOTICE_STATI = set(      # 'b' for bad!
    [status for status in STATI if status.startswith('b')])
APPLICANT_STATI = [              # 'a' for applicant!
    status for status in STATI if status.startswith('a')]
APPLICANT_SET = set(APPLICANT_STATI)
EXEC_STATI = [ status for status in STATI if (
                   status.startswith('z') and (status != 'zae'))]
EXEC_SET = set(EXEC_STATI)
MISCELANEOUS_STATI = "m|w|be"
NON_MEMBER_SET = APPLICANT_SET | {
        "h", "m", 't', 'zae', 'zzz'}  # bitwise OR
NON_FEE_PAYING_STATI = {"w", "t", "r", "h"}

N_FIELDS = 14  # Only when unable to use len(dict_reader.fieldnames).
MONEY_KEYS = ("dues", "dock", "kayak", "mooring")
MONEY_KEYS_CAPPED = [item.capitalize() for item in MONEY_KEYS]
FEES_KEYS = MONEY_KEYS[1:]
MONEY_HEADERS = {
    "dues":    "Dues..........",
    "dock":    "Dock Usage....",
    "kayak":   "Kayak Storage.",
    "mooring": "Mooring.......",
    "total":   "    TOTAL.........",
    }
demographic_f = (
    "{first} {last}  {address}, {town}, {state} {postal_code}")
demographic_f_w_phone_and_email = (
    "{first} {last} [{phone}] {address}, {town}, {state} " +
    "{postal_code} [{email}]")
demographic_f_last_first = (
    "{last}, {first}  {address}, {town}, {state} {postal_code}")
demographic_f_last_first_w_phone_and_email = (
    "{last}, {first} [{phone}] {address}, {town}, {state} " +
    "{postal_code} [{email}]")
demographic_f_last_first_w_staggered_data = '\n'.join((
    "{last}, {first} [{phone}]",
    "\t{address}, {town}, {state} {postal_code}",
    "\t[{email}]"))
demographic_f_first_last_w_staggered_data = '\n'.join((
    "{first}, {last} [{phone}]",
    "\t{address}, {town}, {state} {postal_code}",
    "\t[{email}]"))
fstrings = {
        'key': "{last},{first}",
        'first_last': "{first} {last}",
        "last_first": "{last}, {first}",
        'first_last_w_address_only': demographic_f, 
        'first_last_w_all_data': demographic_f_w_phone_and_email,
        'last_first_w_address_only': demographic_f_last_first,
        'last_first_w_all_data':
                    demographic_f_last_first_w_phone_and_email,
        'first_last_w_all_staggered':
                    demographic_f_last_first_w_staggered_data,
        'last_first_w_all_staggered': 
                    demographic_f_first_last_w_staggered_data,
    }


def format_record(record, f_str):
    """
    Retrieves a string representation of a record.
    """
    return f_str.format(**record)


# The following is no longer used...
# we get around the problem in a different way..
# see "To avoid gmails nasty warning ..." in append_email.
gmail_warning = """
NOTE: If yours is a gmail account this email will be accompanied
by an alarming warning which it is safe for you to ignore.
Although sent on behalf of, it was not sent by, the
rodandboatclub@gmail.com email account; rather it was sent
via a different mail transfer agent (easydns.com) and hence gmail
feels compelled to issue this warning.
All is well.  "Trust me!"
"""


def replace_with_in(s, rl, l):
    """
    <s> is a string
    <rl> & <l> are iterables containing strings
    A list is returned.
    Each item of l is examined and
        if it contains <s>
            <rl> is added to the returned list
        else the item itself is added to the returned list
    which is returned sorted with no duplicates.
    Used in utils to expand 'appl' and 'exec' into included stati.
    ## TO DO: Might be better to bring the detail from where it's
    ## used back to here.
    """
    ret = []
    for item in set(l):
        if s in item:
            ret.extend(rl)
        else:
            ret.append(item)
    return sorted(set(ret))


def names_reversed(name):
    """
    Changes first last to last, first
    and last, first to first last.
    """
    if ', ' in name:
        parts = name.split(', ')
        return '{} {}'.format(parts[1].strip(), parts[0].strip())
    else:
        parts = name.rsplit(maxsplit=1)
        return '{}, {}'.format(parts[1].strip(), parts[0].strip())


def traverse_records(infile, custom_funcs, club):
    # Fundamentally different from <modify_data>/<modified_data>!
    # This function is to collect specific data, not change it.
    """
    Opens <infile> for dict_reading (and in the process
    assigns club.fieldnames.
    Applies <custom_funcs> to each record.
    <custom_funcs> can be a single function or a
    list of functions. These functions typically populate
    attributes of club, an instance of the rbc.Club class.
    Required club attributes are set up using the
    setup_required_attributes function (see end of module.)
    Also assigns club.fieldnames and club.n_fields which are
    sometimes useful.
    """
    if callable(custom_funcs):  # If only one function provided
        custom_funcs = [custom_funcs]  # place it into a list.
    setup_required_attributes(custom_funcs, club)
    with open(infile, 'r', newline='') as file_object:
        if not club.quiet:
            print("DictReading {}...".format(file_object.name))
        dict_reader = csv.DictReader(file_object)
        # fieldnames is used by get_usps and restore_fees cmds.
        club.fieldnames = dict_reader.fieldnames
        club.n_fields = len(club.fieldnames)  # to check db integrity
        for record in dict_reader:
            for custom_func in custom_funcs:
                custom_func(record, club)


def report_error(report, club):
    try:
        club.errors.append(report)
    except AttributeError:
        print(report)


def ck_number_of_fields(record, club=None):
    """
    Checks that there are the correct number of fields in "record".
    If "club" is specified, errors are appended to club.errors
    which must be set up by client;
    if not: error is reported by printing to stdout.
    """
    n_fields = len(record)
    possible_error = ("{last} {first} has {N_FIELDS}".format(
                                                    **record))
    if ((club and (n_fields != club.n_fields))
            or n_fields != N_FIELDS):
        report_error(possible_error, club)


def get_status_set(record):
    if record['status']:
        stati =  set(record['status'].split(glbs.SEPARATOR))
        # above returns set of one empty string if status is empty
        stati = {item for item in stati if item}
    else: stati = set()
    return stati


def is_applicant(record):
    """
    Tests whether or not <record> is an applicant.
    """
    stati = get_status_set(record)
    if stati & APPLICANT_SET:
        return True
    return False


def is_new_applicant(record):
    """
    Application received with payment and needs to be acknowledged.
    """
    return 'a' in get_status_set(record)


def is_inductee(record):
    '''
    '''
    return 'ai' in get_status_set(record)


def vacancy_open(record):
    """
    """
    return 'av' in get_status_set(record)


def is_member(record):
    """
    Tries to determine if record is that of a member (based on
    status field.)
    """
    stati = get_status_set(record)
    if not stati: return True
    if stati.intersection(set(NON_MEMBER_SET)):
        return False
    return True


def is_non_fee_paying(record):
    """
    """
    if NON_FEE_PAYING_STATI & get_status_set(record):
        return True


def is_minutes_only(record):
    """
    """
    return 'm' in get_status_set(record)


def is_dues_paying(record):
    if is_non_fee_paying(record):
        return False
    if is_member(record):
        return True
    stati = get_status_set(record)
    if 'ai' in stati or 'ad' in stati:
        return True


def is_new_member(record):
    """
    a temporary status which triggers the
    welcome to full membership letter.
    """
    return 'am' in get_status_set(record)


def is_honorary_member(record):
    """
    """
    return 'h' in get_status_set(record)


def is_inactive_member(record):
    """
    minutes only
    """
    return 'm' in get_status_set(record)


def is_terminated(record):
    """
    a temporary status assumed for non payment of dues
    should which trigger a regret letter  (not yet implemented.)
    """
    return 't' in get_status_set(record)


def is_gmail_user(record):
    """
    Has a gmail address.
    """
    return record['email'].endswith('gmail.com')


def increment_napplicants(record, club):
    """
    """
    if is_applicant(record):
        club.napplicants += 1


def increment_nmembers(record, club):
    """
    Client must initiate club.nmembers(=0) attribute.
    If record is that of a member, nmembers is incremented.
    """
    if is_member(record):
        club.nmembers += 1


def increment_nminutes_only(record, club):
    """
    """
    if is_minutes_only(record):
        club.nminutes_only += 1


def is_member_or_applicant(record, club=None):
    return is_member(record) or is_applicant(record)


def has_valid_email(record, club=None):
    if 'be' in get_status_set(record):
        return False
    return record["email"]


def letter_returned(record, club=None):
    return 'ba' in get_status_set(record)


def get_usps(record, club):
    """
    Selects members who get their copy of meeting minutes by US
    Postal Service. i.e. Those with no email.
    Populates club.usps_only with a line for each such member
    using csv format: first, last, address, town, state, and
    postal_code.
    """
    if not record['email']:
        rec = helpers.Rec(record)
        club.usps_only.append(rec)


def get_bad_emails(record, club):
    if 'be' in get_status_set(record):
        club.bad_emails.append(demographic_f.format(**record))
        if hasattr(club, 'usps_only') and club.be:
            rec = helpers.Rec(record)
            club.usps_only.append(rec)


def get_secretary(record, club):
    """
    If record is that of the club secretary,
    assigns secretary's demographics to club.secretary
    z3_sec
    """
    if 'z3_sec' in get_status_set(record):
        club.secretary = demographic_f.format(**record)


def get_zeros_and_nulls(record, club):
    """
    Populates club.zeros and club.nulls lists.
    """
    dues = record['dues']
    try:
        value = int(dues)
    except ValueError:
        club.nulls.append("{last}, {first}: {dues}".format(**record))
    else:
        if value == 0:
            club.zeros.append("{last}, {first}: {dues}".format(
                                                    **record))


# # Beginning of 'add2' functions:

def add2email_by_m(record, club):
    """
    Populates dict- club.email_by_name.
    """
    record = helpers.Rec(record)
    name = record(fstrings['last_first'])
    email = record['email']
    if email:
        club.email_by_m[name] = email


redacted = '''
def add2db_emails(record, club):  #?!unused
    """
    Populates club.db_emails
    'ex' for experimental
    db_emails is a dict with all members included but
    with a special key for those without email
    """
#   print("called add2db_emails")
    record = helpers.Rec(record)
    name = record(fstrings['last_first'])
    email = record['email']
    if not email:
        email = NO_EMAIL_KEY
    club.db_emails[name] = email
'''


def add2ms_by_email(record, club):
    """
    Populates club.ms_by_email, a dict keyed by emails one of which
    is NO_EMAIL_KEY to capture members without an email address.
    """
    record = helpers.Rec(record)
    name = record(fstrings['last_first'])
    email = record['email']
    if not email:
        email = NO_EMAIL_KEY
    _ = club.ms_by_email.setdefault(email, [])
    club.ms_by_email[email].append(name)


def add2applicant_with_email_set(record, club):
    """
    Populates club.applicant_with_email_set
    """
    if not is_applicant(record):
        return
    record = helpers.Rec(record)
    name = record(fstrings['key'])
    if record['email']:
        club.applicant_with_email_set.add(name)


def add2stati_by_m(record, club):
    if record["status"]:
        record = helpers.Rec(record)
        club.stati_by_m[record(fstrings['first_last'])] = (
            get_status_set(record)  )


def add2ms_by_status(record, club):
    """
    Appends a record to club.ms_by_status:
        Each key is a status
        Each value is a list of keys (member key format.)
    """
    if record['status']:
        entry = format_record(record, club.format)
        stati = get_status_set(record)
        key = format_record(record, fstrings['key'])
        for status in stati:
            _ = club.ms_by_status.setdefault(status, [])
            record = helpers.Rec(record)
#           print("appending", record(club.format), status)
            club.ms_by_status[status].append(
                    record(fstrings['key']))
            club.entries_w_status[key] = entry

def add2bad_demographics(record, club):  #?!unused
    record = helpers.Rec(record)
    stati = get_status_set(record)
    if 'ba' in stati:
        club.ba_stati[record(fstrings['last_first'])] = (
            record(fstrings['first_last_w_all_staggered']))
    if 'be' in stati:
        club.be_stati[record(fstrings['last_first'])] = (
            record(fstrings['first_last_w_all_staggered']))


redacted = '''
def add2demographics(record, club):
    """
    Appends a record to club.demographics:
        Each key is a member name in last_first format
        Each value is the record in format specified
            by club.format
    """
    record = helpers.Rec(record)
    club.demographics[record(fstrings['last_first'])] = (
          record(club.format)) 
'''


def add2member_with_email_set(record, club):
    """
    Appends a record to club.member_with_email_set if record
    is that of a member and the member has an email address.
    ## Proposal: rename 'add2has_email_set' and store in 
                        'club.has_email_set'.
    """
    record = helpers.Rec(record)
    entry = record(fstrings['key'])
#   entry = record(fstrings['last_first'])
    if record['email'] and is_member(record):
        club.member_with_email_set.add(entry)
    else:
        club.no_email_set.add(entry)


def add2fee_data(record, club):
    """
    Populates club.fee_category_by_m  and
    club.ms_by_fee_category.
    Note: this gathers from main data base,
    _not_ from extra fees SPoTs. See
    data.populate_extra_fees(club) which populates
    club.by_name & club.by_category.
    Both produce dicts in the same formats respectively.
    Tested by Tests.xtra_fees.py
    """
    record = helpers.Rec(record)
    name = record(fstrings['last_first'])
    # print(repr(FEES_KEYS))
    for f_key in FEES_KEYS:
        try:
            fee = int(record[f_key])
        except ValueError:
            continue
        _ = club.ms_by_fee_category.setdefault(f_key, {})
        club.ms_by_fee_category[f_key][name] = fee
        _ = club.fee_category_by_m.setdefault(name, {})
        club.fee_category_by_m[name][f_key] = fee


def add2malformed(record, club=None):
    """
    Populates club.malformed (which must be set up by client.)
    Checks that that for each record:
    1. there are N_FIELDS per record.
    2. the money fields are blank or evaluate to an integer.
    3. the email field contains "@"
    club.__init__ sets club.previous_name to "".
    (... used for comparison re correct ordering.)
    Client must set up a club.malformed[] empty list to be populated.
    """
    record = helpers.Rec(record)
    name = record(fstrings['last_first'])
    if len(record) != N_FIELDS:
        club.malformed.append("{}: Wrong # of fields.".format(name))
    for key in MONEY_KEYS:
        value = record[key]
        if value:
            try:
                res = int(value)
            except ValueError:
                club.malformed.append("{}, {}:{}".format(
                                        name, key, value))
    if record["email"] and '@' not in record["email"]:
        club.malformed.append("{}: {} Problem /w email.".format(
                                            name, record['email']))
    if name < club.previous_name:
        club.malformed.append("Record out of order: {}".format(name))
    club.previous_name = name

# End of 'add2...' functions


def apply_credit2statement(statement, credit):
    """
    credit is used to modify statement- both are dicts
    """
    for key in set(credit.keys()) - {'extra'}:
        try:
            statement[key] -= credit[key]
        except TypeError:
            print('statement key/value is {}: {}'
                    .format(key, statement[key]))
            print('credit key/value is {}: {}'
                    .format(key, credit[key]))
            raise
        except KeyError:
            print('credit key is "{}"'.format(key))
            raise


def apply_credit2record(statement, record):
    """
    <statement> is a dict with (money key): (dollar amnt)
    money keys include "total"
    <record> is modified accordingly (ignoring the 'total' key
    """
    for key in [key for key in statement.keys()
            if not key in {'total', 'extra'}]:
        record[key] = int(record[key]) - statement[key]


def thank_func(record, club):
    """
    Must assign "payment" and extra" to record.
    """
    record = helpers.Rec(record)
    name = record(fstrings['last_first'])
    if name in club.statement_data_keys:
        payment = club.statement_data[name]['total']
        statement_dict = get_statement_dict(record)
        try:
            apply_credit2statement(statement_dict, club.statement_data[name])
        except KeyError:
            print("error processing {}"
                .format(record['first'] + record['last']))
            raise
        record['extra'] = get_statement(statement_dict)
        record['payment'] = payment
        q_mailing(record, club)
    # Still need to move record to new db

# The next two functions add entries to club.new_db

def db_credit_payment(record, club):
    """
    !?UNUSED?!  Redact?!
    Checks if record is in the club.statement_data dict and if so
    credits payment(s).  In either case data is moved to new
    db specified by club.dict_writer.
    """
    new_record = {}
    for key in record.keys():
        new_record[key] = record[key]
    record = helpers.Rec(record)
    name = record(fstrings['last_first'])
    if name in club.statement_data_keys:
        apply_credit2record(club.statement_data[name], new_record)
    club.dict_writer.writerow(new_record)


def db_apply_charges(record, club):
    pass

# .. above two functions write to new db with updated information.
# The next two function change the db!!


def rm_email_only_field(record, club):
    """
    A one time use function:
    removes the "email_only" field of the record.
    This field no longer exists in the data base-
    it's implied by the presence of something in the 'email' field.
    It was used to modify the data base to its present form and will
    never be used again- should be redacted.
    """
    new_record = {}
    for key in club.new_fieldnames:
        new_record[key] = record[key]
    return new_record


def set_kayak_fee(record, club):
    """
    Returns a modified record:
        Assumes club.kayak_fees is a dict keyed by last,first names.
        If record owner is not in this dict, her kayak field is set
        to blank, othewise it is set to the value.
    """
    new_record = {}
    for key in club.fieldnames:
        new_record[key] = record[key]
    name = format_record(record, 'last_first' )
    if name in club.kayak_keys:
        new_record['kayak'] = club.kayak_fees[name]
    else:
        new_record['kayak'] = ''
    return new_record


def credit_payment_func(record, club):
    """
    Returns the <record>, modified by crediting payment(s)
    specified in club.statement_data
    """
    record = helpers.Rec(record)
    name = record(fstrings['last_first'])
    if name in club.statement_data.keys():
        apply_credit2record(club.statement_data[name], record)
    return record


def modify_data(csv_in_file_name, func, club=None):
    # Rename?: 'traverse_csv', 'modified_data'
    # Note: 'traverse_records' collects data, this
    # returns (a possibly modified version of) each record
    # in the csv file.
    """
    A generator: reads a csv file and for each entry, yields a record
    modified by func (or, if func==None, the record unchanged.)
    <club> is provided to be used as a parameter of <func> (if
    additional data is needed.)
    """
    with open(csv_in_file_name, 'r', newline='') as file_obj:
        reader = csv.DictReader(file_obj)
        for rec in reader:
            if func == None:
                yield rec
            else:
                yield func(rec, club)


def show_by_status(by_status,  # dict: key: status, value: name_keys
                   stati2show=STATI,
                   club=None):
    # clients: show_cmd & report_cmd in utils module
    # probably should be elsewhere rather in this module??
    """
    First parameter, <by_status>, is a dict keyed by status.
    Returns a list of strings (which can be '\n'.join(ed))
    consisting of Keys as headers with values listed beneath each key.
    Second parameter can be used to restrict which stati to display.
    If club is specified, its <applicant_data>  attribute is
    used to add dates and/or sponsors.
    """
    ret = []
    for status in sorted(by_status.keys()):
        if status in stati2show:
            helpers.add_header2list(STATUS_KEY_VALUES[status],
                                    ret, underline_char='-')
            for name_key in by_status[status]:
#               print('name_key:', name_key)
                ret.append(club.entries_w_status[name_key])
                if status in APPLICANT_STATI:
                    if hasattr(club, 'applicant_data'):
                        if name_key in club.applicant_data_keys:
                            # create a line of dates
                            dates_attended = data.line_of_meeting_dates(
                                            club.applicant_data[name_key])
                            if dates_attended:
                                ret.append("\tDate(s) attended: {}"
                                        .format(dates_attended))
                            else:
                                ret.append("\tNo meetings attended.")
                            sponsors = club.sponsors_by_applicant[name_key]
                        else:
                            sponsors = False
                            print("{} has no dates!!".format(name_key))
                        if sponsors:
                            sponsor_line = ', '.join(
                                    [helpers.tofro_first_last(sponsor)
                                    for sponsor in sponsors])
                            ret.append("\tSponsors: {}"
                                            .format(sponsor_line))
                        else:
                            pass
    #                       print("{} has no sponsors!!".format(name_key))
    return ret


def dues_owing(record, club=None):
    """
    Checks if there is a positive balance in the dues field.
    """
    if record["dues"] and int(record["dues"]) > 0:
        return True
    return False


def not_paid_up(record, club=None):
    """
    Checks if there is a positive balance in any of the money fields.
    """
    for key in MONEY_KEYS:
        if record[key] and int(record[key]) > 0:
            return True
    return False


def get_statement_dict(record):
    """
    Calculates debit/credit for member represented by 'record'
    and returns a dict keyed by the MONEY_KEYS and 'total'.
    Note: 'total' is always returned. Values for other keys are
    included only if are non zero.
    """
    ret = dict(extra='',
                total= 0)
    for key in MONEY_KEYS:
        if record[key]:
            ret[key] = int(record[key])
            ret['total'] += ret[key]
        if not ret['total']: ret['extra'] = '  still owing'
    return ret


def add2statement_data(record, club):
    rec = helpers.Rec(record)
    name = rec(fstrings['last_first'])
    club.statement_data_keys.append(name)
    club.statement_data[name] = get_statement_dict(rec)


def add2modified2thank_dict(record, club):
    rec = helpers.Rec(record)
    name = rec(fstrings['last_first'])
    rec['status'] = club.statement_data[name]["total"]
    club.modified2thank_dict[name] = rec


def rec_w_total_in_status(record, club):
    """
    Consults club.statement_data and returns a copy of the record
    with the appropriate total in its 'status' field.
    """
    rec = helpers.Rec(record)
    key = rec(fstrings['last_first'])
    if key in club.statement_data_keys:
        rec['status'] = club.statement_data[key]['total']
    else:
        print(
        "Warning: expected to find '{}' in club.statement_data_keys")
        rec['status'] = 'Payment not found'
    return rec


def get_statement(statement_dict, club=None):
    """
    Returns a string making up a statement of dues and fees.
    If club.inline then all is in one line; otherwise parts
    are separated by '/n' chars.
    """
    key_set = set([key for key in statement_dict.keys()])
    ret = []
    for key in MONEY_HEADERS.keys():
        if key in key_set:
            ret.append("{} {: >3}".format(
                        MONEY_HEADERS[key],
                        statement_dict[key]))
    if club and club.inline:
        return '; '.join(ret)
#   return '\n\t'.join(ret)
    return '\n'.join(ret)


def assign_statement2extra_func(record, club=None):
    """
    Sets up record['extra'] to contain a statement with
    appropriate suffix for dues & fees notice.
    """
    record["owing"] = False
    d = get_statement_dict(record)
    extra = ['Statement of account:', ]
    extra.append(get_statement(d))
    if d['total'] == 0:
        extra.append("You are all paid up. Thank you.")
    elif d['total'] < 0:
        extra.extend(["You have a credit balance.",
                      "Thank you for your advanced payment."])
    else:
        record["owing"] = True
    record['extra'] = '\n'.join(extra)


def get_payables_dict(record, club):
    """
    Populates club.owing_dict and club.credits_dict.

    Checks record for dues &/or fees. If found,
    positives are added to club.owing_dict,
    negatives to club.credits_dict.
    """
    if get_status_set(record).intersection({'h', 'm', 'r'}):
        return
    name_key = format_record(record, fstrings['key'])
    val = {}
    total = 0
    for key in MONEY_KEYS:
        if record[key]:
            amt = int(record[key])
            total += amt
            val[key] = amt
    val['total'] = total
    if total > 0:
        club.owing_dict[name_key] = val
    if total < 0:
        club.credits_dict[name_key] = val


def get_payables(record, club):
    """
    Populates club.still_owing and club.advance_payments
    which are lists that must be set up by the client.

    Checks record for dues &/or fees. If found,
    positives are added to club.still_owing,
    negatives to club.advance_payments.
    """
    if get_status_set(record).intersection({'h', 'm', 'r'}):
        return
    if record['email']:
        no_email = False
        name = "{last}, {first}: ".format(**record)
    else:
        no_email = True
        if club.asterixUSPS:
            name = "{last}, {first}*: ".format(**record)
    line_positive = []
    line_negative = []
    for key in MONEY_KEYS:
        if record[key]:
            amount = int(record[key])
            if amount > 0:
                line_positive.append("{:<5}{:>4d}".format(
                    key, amount))
#                       MONEY_HEADERS[key], amount))
            elif amount < 0:
                line_negative.append("{:<5}{:>4d}".format(
                    key, amount))
    if line_positive:
        line = ("{:<30}".format(name)
                + ', '.join(line_positive))
        club.still_owing.append(line)
        if no_email: club.n_no_email += 1
    if line_negative:
        line = ("{:<30}".format(name)
                + ', '.join(line_negative))
        club.advance_payments.append(line)


def name_w_demographics(record, club):
    stati = get_status_set(record)
    if not record['email']:
        record['email'] = 'no email'
    if not record['phone']:
        record['phone'] = 'no phone'
    line = club.PATTERN4WEB.format(**record)
    if "be" in stati:
        line = line + " (bad email!)"
    if "ba" in stati:
        line = line + " (mail returned!)"
    return line


def add2lists(record, club):
    """
    Populates club.members, club.honorary, club.inactive, (if web=True)
              club.stati, club.applicants,
              club.inductees, club.by_applicant_status and
              club.errors (initially empty lists)
    and increments club.nmembers,
                   club.napplicants and
                   club.ninductees (initially set to 0.)
    <club> is an instance of rbc.Club; its 'format' attribute
    determines how the data is displayed.
    """
    line = club.format.format(**record)
    key = fstrings['key'].format(**record)
    stati = get_status_set(record)
    for status in stati:
        club.stati.setdefault(status, [])
        club.stati[status].append(key)
    club.entries_w_status[key] = line
    if is_member(record):
        # so we have a blank line between first letters:
        first_letter = record['last'][:1]
        if first_letter != club.first_letter:
            club.first_letter = first_letter
            club.members.append("")

        club.members.append(line)
        club.nmembers += 1
    if is_honorary_member(record):
        club.honorary.append(line)
        club.nhonorary += 1
    if is_inactive_member(record):
        club.inactive.append(line)
        club.ninactive +=1
    if is_inductee(record):
        club.inductees.append(line)
        club.ninductees += 1
        pass
    if is_applicant(record):
        club.applicants[key] = line
        stati = get_status_set(record)
        status = stati & APPLICANT_SET
        assert len(status) == 1
        club.napplicants += 1
        s = status.pop()
        _ = club.by_applicant_status.setdefault(s, [])
        club.by_applicant_status[s].append(key)
        # metadata (dates of meetings; sponsors)
        # being appended by utils.show_cmd as it is building the
        # output.


def populate_non0balance_func(record, club):
    """
    Reads the MONEY_KEYS fields and, if any are not zero,
    populates the club.non0balance dict keyed by member name
    with values keyed by MONEY_KEYS.
    """
    total = 0
    record = helpers.Rec(record)
    name = record(fstrings['last_first'])
    for key in MONEY_KEYS:
        try:
            money = int(record[key])
        except ValueError:
            money = 0
        if money:
            _ = club.non0balance.setdefault(name, {})
            club.non0balance[name][key] = money


def populate_name_set_func(record, club):
    record = helpers.Rec(record)
    name = record(fstrings['last_first'])
    club.name_set.add(name)


def add_dues_fees2new_db_func(record, club):
    """
    Prerequisites: 
        club.extra_fee_names: a dict-
            key: sting- "last, first" name
            value: list of tuples- (category, amount)
        club.extra_fee_names: set of keys of above dict.
        club.new_db: list of records, created by traverse_records
    Each record processed is duplicated, dues/fees added (if provided)
    and then added to club.new_db.
    """
    new_record = {}
    for key in record.keys():
        new_record[key] = record[key]
    if is_dues_paying(record):
        new_record['dues'] = helpers.str_add(
            club.YEARLY_DUES,
            new_record['dues'])
        name = fstrings['last_first'].format(**record)
        if name in club.extra_fee_names:
            for (category, amount) in club.by_name[name].items():
                category = category.lower()
                new_record[category] = helpers.str_add(
                    amount, new_record[category])
    club.new_db.append(new_record)


# #### Next group of methods deal with sending out mailings. #######
# Clients must set up the following attributes of the 'club' parameter
# typically an instance of the Membership class:
#    email, letter, json_data,


def append_email(record, club):
    """
    club.which has already been assigned to one of the values
    of content.content_types
    Appends an email to club.json_data
    """
#   print(club.email)
    body = club.email.format(**record)
    sender = club.which['from']['email']
    email = {
        'From': sender,    # Mandatory field.
        'Sender': sender,   # 0 or 1
        'Reply-To': club.which['from']['reply2'],  # 0 or 1
        'To': record['email'],  # at least one ',' separated address
        'Cc': '',             # O or 1 comma separated list.
        'Bcc': '',            # O or 1 comma separated list.
        'Subject': club.which['subject'],  # 0 or 1
        'attachments': [],
        'body': body,
    }
    sponsor_email_addresses = ''
    if club.cc_sponsors:
        record = helpers.Rec(record)
        name_key = record(fstrings['key'])
        if name_key in club.applicant_set:
            sponsors = club.sponsors_by_applicant[name_key]
            # Use list comprehension for the following:
            sponsor_email_addresses = []
            for sponsor in club.sponsors_by_applicant[name_key]:
                addr = club.sponsor_emails[sponsor]
                if addr:
                    sponsor_email_addresses.append(addr)
            sponsor_email_addresses = ','.join(
                    sponsor_email_addresses)
    if club.cc: ccs = club.cc
    else: ccs = ''
    email['Cc'] = helpers.join_email_listings(
                                    sponsor_email_addresses, ccs)
    if club.bcc:
        email['Bcc'] = club.bcc
    club.json_data.append(email)


def file_letter(record, club):
    entry = club.letter.format(**record)
    path2write = os.path.join(club.MAILING_DIR,
                              "_".join((record["last"],
                                        record["first"])))
    with open(path2write, 'w') as file_obj:
        file_obj.write(helpers.indent(entry,
                                      club.lpr["indent"]))


def q_mailing(record, club):
    """
    Dispatches email &/or letter to appropriate 'bin'.
    """
    record["subject"] = club.which["subject"]
    # ^ the above should be assigned elsewhere!!
    # check how to send:
    how = club.which["e_and_or_p"]
    if how == "email":
        append_email(record, club)
    elif how == "both":
        append_email(record, club)
        file_letter(record, club)
    elif how == 'one_only':
        if record['email']:
            append_email(record, club)
        else:
            file_letter(record, club)
    elif how == 'usps':
        file_letter(record, club)
    else:
        print("Problem in q_mailing: letter/email not sent to {}."
                .format(fstrings['first_last'].format(**record)))


def prepare_mailing(club):
    """
    Clients of this method: utils.prepare_mailing_cmd
                            utils.thank_cmd
    Both use utils.prepare4mailing to assign attributes to <club>
    (See Notes/call_flow.)
    """
    traverse_records(club.infile,
                     club.which["funcs"],
                     club)  # 'which' comes from content
#   listing = [func.__name__ for func in club.which["funcs"]]
#   print("Functions run by traverse_records: {}".format(listing))
    # No point in creating a json file if no emails:
    if hasattr(club, 'json_data') and club.json_data:
        with open(club.json_file, 'w') as file_obj:
            print('Dumping emails (JSON) to "{}".'
                    .format(file_obj.name))
            file_obj.write(json.dumps(club.json_data))
    else:
        print("There are no emails to send.")


# ## The following are functions used for mailing. ###
# # These are special functions suitable for the <func_dict>:
# # they provide necessary attributes to their 'record' parameter
# # in order to add custom content (to a letter &/or email.)


def std_mailing_func(record, club):
    """
    Assumes any prerequisite processing has been done and
    requisite values added to record.
    Mailing is sent if the "test" lambda => True.
    Otherwise the record is ignored.
    """
    if club.which["test"](record):
        record["subject"] = club.which["subject"]
        if club.owing_only:
            if record['owing']:
                q_mailing(record, club)
        else:
            q_mailing(record, club)


def bad_address_mailing_func(record, club):
    if club.which["test"](record):
        record["subject"] = club.which["subject"]
        record['extra'] = ("{address}\n{town}, {state} {postal_code}"
                           .format(**record))
        q_mailing(record, club)


def testing_func(record, club):
    """
    For mailings which require no special processing.
    Mailing is sent if the "test" lambda => True.
    Otherwise the record is ignored.
    """
    if club.which["test"](record):
        record["subject"] = club.which["subject"]
        record['extra'] = "Blah, Blah, Blah!"
        q_mailing(record, club)


def set_inductee_dues(record, club=None):
    """
    Provides processing regarding what fee to charge
    (depends on the time of year: $100 vs $50)
    and sets record["current_dues"].
    """
    if helpers.month in (1, 2, 3, 4):
        record["current_dues"] = 50
    else:
        record["current_dues"] = 100


def inductee_payment_f(record, club):
    """
    Contingent on the club.which["test"] lambda:
    (If the record's status field contains 'i' for 'inducted'.)
    Sets up record["current_dues"] (by calling set_inductee_dues)
    and record["subject"]  ?? should this be elsewhere??
    """
    if club.which["test"](record):
        set_inductee_dues(record)
        record["subject"] = club.which["subject"]
        q_mailing(record, club)


#  ### ... end of mailing functions.  ###


def send_attachment(record, club):
    """
    ## Will probably be redacted. Client is utils.emailing_cmd.
    Uses 'mutt' (which in turns uses 'msmtp') to send emails
    with attachment: relies on <mutt_send> which in turn
    relies on command line args:
        "-F": which muttrc (to specify 'From: ')
        "-a": file name of the attachment
        "-c": name of file containing content of the email
        "-s": subject of the email
    """
    body = club.content.format(**record)
    email = record["email"]
    bad_email = "be" in record["status"]
    if email and not bad_email:
        club.mutt_send(email,
                       args["--subject"],
                       body,
                       args["-a"],
                       )


prerequisites = {   # collectors needed by the
                    # various traversing functions
#   add2db_emails: [  #?!unused
#       "club.db_emails = {}",
#       ],
    ck_number_of_fields: [
        "club.errors = []",
        ],
    increment_nmembers: [
        "club.nmembers = 0",
        ],
    increment_napplicants: [
        "club.napplicants = 0",
        ],
    increment_nminutes_only: [
        "club.nminutes_only = 0",
        ],
    get_usps: [
        'club.usps_only = []',
        'club.usps_csv = []',
        ],
    get_zeros_and_nulls: [
        'club.nulls = []',
        'club.zeros = []',
        ],
    add2email_by_m: [
        'club.email_by_m = {}',
        ],
    add2ms_by_email: [
        'club.ms_by_email = {}',
        ],
    add2stati_by_m: [
        'club.stati_by_m = {}',
        ],
    # Next one is ??? being redacted?
#   add2email_data: [
#       'club.email_by_m = {}',
#       'club.ms_by_email = {}',
#       'club.without_email = []',
#       ],
    add2ms_by_status: [
        'club.ms_by_status = {}',
        'club.entries_w_status = {}',
        ],
    #   add2status_data: [
    #       'club.ms_by_status = {}',
    #       'club.napplicants = 0',
    #       'club.stati_by_m = {}',
    #       ],
    add2member_with_email_set: [
        'club.member_with_email_set = set()',
        'club.no_email_set = set()',
        ],
    add2applicant_with_email_set: [
        'club.applicant_with_email_set = set()',
        ],
#   add2demographics: [
#       'club.demographics = {}',
#       ],
    add2bad_demographics: [  #?!unused
        'club.ba_stati = {}',
        'club.be_stati = {}',
        ],
    add2fee_data: [
        'club.fee_category_by_m = {}',
        'club.ms_by_fee_category = {}',
        ],
    add2malformed: [
        'club.malformed = []',
        ],
    add2lists: [
        # ACTION REQUIRED
        # 1st is redundant (duplicates club.format vs pattern;
        # the latter is assigned by utils.show_cmd().)
#       """club.pattern = ("{first} {last}  [{phone}]  {address}, " +
#                   "{town}, {state} {postal_code} [{email}]")""",
        'club.members = []',
        'club.nmembers = 0',
        'club.honorary = []',
        'club.nhonorary = 0',
        'club.inactive = []',
        'club.ninactive = 0',
        'club.applicants = {}',
        'club.by_applicant_status = {}',
        'club.napplicants = 0',
        'club.stati = {}',
        'club.errors = []',
        'club.entries_w_status = {}',
        ],
    get_payables: [
        'club.still_owing = []',
        'club.advance_payments = []',
        'club.n_no_email = 0',
        ],
    get_payables_dict: [
        'club.owing_dict = {}',
        'club.credits_dict = {}',
        ],
    get_secretary: [
        'club.secretary = ""',
        ],
    get_bad_emails: [
        'club.bad_emails = []',
        ],
    #   dues_and_fees: [
    #       'club.null_dues = []',
    #       'club.members_owing = []',
    #       'club.members_zero_or_cr = []',
    #       'club.dues_balance = 0',
    #       'club.fees_balance = 0',
    #       'club.retiring = []',
    #       'club.applicants = []',
    #       'club.errors = []',
    #       ],
    populate_non0balance_func: [
        "club.errors = []",
        "club.non0balance = {}",
        ],
    populate_name_set_func: [
        "club.name_set = set()",
        ],
    std_mailing_func: [
        "club.json_data = []",
        ],
#   db_apply_charges: [
#       "club.new_db = {}",
#       ],
    add2statement_data: [
        'club.statement_data = {}',
        'club.statement_data_keys = []',
        ],
    add2modified2thank_dict: [
        'club.modified2thank_dict = {}',
        ],
    #   add2status_data: [
    #       'club.ms_by_status = {}',
    #       ],
    add_dues_fees2new_db_func: [
        'club.new_db = []',
        ]
    }



def setup_required_attributes(custom_funcs, club):
    """
    Ensures that club has necessary attributes
    required by all the custom_funcs to be called.
    Relies on the above prerequisites dict.
    """
    set_of_funcs = set(prerequisites.keys())
    for func in custom_funcs:
        if func in set_of_funcs:
            for code in prerequisites[func]:
                exec(code)



func_dict = {}
func_dict['set_kayak_fee'] = set_kayak_fee
func_dict['rm_email_only_field'] = (
    rm_email_only_field,
    ("first", "last", "phone", "address", "town", "state",
     "postal_code", "country", "email", "dues", "dock",
     "kayak", "mooring", "status",
     )
    )

if __name__ == "__main__":
    print("member.py compiles OK.")
    
    temporarilyredacted = '''
else:
    def print(*args, **kwargs):
        pass
'''

