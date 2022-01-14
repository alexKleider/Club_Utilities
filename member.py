#!/usr/bin/env python3

# File: member.py

"""
Applies to records of members of 'the club' which
is further defined in another module (rbc.py).
Many methods of Membership class are essentially
independant of Membership but pertain to each record.
Hence makes sense to separate them out.
A many need to store data so those will get an extra
(named) parameter: 'club=None'.
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
    "a" : "Application complete but not yet acknowledged",  # not yet welcomed
    "a0": "Applicant (no meetings yet)",  # welcomed
    "a1": "Attended one meeting",
    "a2": "Attended two meetings",
    "a3": "Attended three (or more) meetings",
    "ai": "Inducted, needs to be notified",
    "ad": "Inducted & notified, membership pending payment of dues",
    "aw": "Inducted, awaiting vacancy and then payment", #7 > #8
    "am": "New Member",  # temporary until congratulatory letter.
    "be": "Email on record being rejected",   # => special notice
    "ba": "Postal address => mail returned",  # => special notice
    "h" : "Honorary Member",                             #10 > #12
    'm' : "Inactive member (continuing to receive minutes)",
    'r' : "Retiring/Giving up Club Membership",
    't' : "Membership terminated (probably none payment of fees)",
    "w" : "Fees being waived",  # a rarely applied special status
    'z1_pres': "President",
    'z2_vp': "VicePresident",
    'z3_sec': "Secretary of the Club",  # not used under Rafferty
    'z4_treasurer': "Treasurer",
    'z5_d_odd': "Director- term ends next odd year",
    'z6_d_even': "Director- term ends next even year",
    'zae': "Application expired or withdrawn",
    }
STATI = sorted([key for key in STATUS_KEY_VALUES.keys()])
SPECIAL_NOTICE_STATI = set(                        # 'b' for bad!
    [status for status in STATI if status.startswith('b')])
APPLICANT_STATI = [                               # 'a' for bad!
    status for status in STATI if status.startswith('a')]
APPLICANT_SET = set(APPLICANT_STATI)
EXEC_STATI = [ status for status in STATI if (
                   status.startswith('z') and (status != 'zae'))]
EXEC_SET = set(EXEC_STATI)
MISCELANEOUS_STATI = "m|w|be"
NON_MEMBER_SET = APPLICANT_SET | {"h", "m", 't', 'zae'}  # bitwise OR
NON_FEE_PAYING_STATI = {"w", "t", "r", "h"}

N_FIELDS = 14  # Only when unable to use len(dict_reader.fieldnames).
MONEY_KEYS = ("dues", "dock", "kayak", "mooring")
MONEY_KEYS_CAPPED = [item.capitalize() for item in MONEY_KEYS]
FEES_KEYS = MONEY_KEYS[1:]
MONEY_HEADERS = {
    "dues":    "Dues..........",
    "mooring": "Mooring.......",
    "dock":    "Dock Usage....",
    "kayak":   "Kayak Storage.",
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
fstrings = {
        'first_last': "{first} {last}",
        "last_first": "{last}, {first}",
        'first_last_w_address_only': demographic_f, 
        'first_last_w_all_data': demographic_f_w_phone_and_email,
        'last_first_w_address_only': demographic_f_last_first,
        'last_first_w_all_data':
                    demographic_f_last_first_w_phone_and_email,
    }

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

func_dict = {}


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
    new_listing = []
    for item in set(l):
#       print("got '{}', ".format(item), end='')
        if s in item:
#           print("found '{}', ".format(s), end='')
            new_listing.extend(rl)
        else:
            new_listing.append(item)
#       print("now listing is '{}'".format(sorted(set(new_listing))))
    return sorted(set(new_listing))


def names_reversed(name):
    """
    Changes first last to last, first
    and last, first to first last.
    """
#   print("got {}".format(name))
    if ', ' in name:
        parts = name.split(', ')
        return '{} {}'.format(parts[1].strip(), parts[0].strip())
    else:
        parts = name.split()
        return '{}, {}'.format(parts[1].strip(), parts[0].strip())


def traverse_records(infile, custom_funcs, club):
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
        print("DictReading {}...".format(file_object.name))
        dict_reader = csv.DictReader(file_object)
        # fieldnames is used by get_usps and restore_fees cmds.
        club.fieldnames = dict_reader.fieldnames
        club.n_fields = len(club.fieldnames)  # to check db integrity
        for record in dict_reader:
#           record = helpers.Rec(record)
#           Not needed because not doing any string formatting.
            for custom_func in custom_funcs:
                custom_func(record, club)

redacted = '''
## following is not yet used but should be!!
def format_record(record, f_str=fstrings['last_first']):
    """
    Retrieves a string representation of a record.
    Default is to return the name in last, first format.
    """
    return f_str.format(**record)

#### Expect to redact the following 3 functions: ####

def member_name(record, club):
    """
   Returns a string formated as defined by club.PATTERN.
    Default <PATTERN> is "{last}, {first}"...
    (see Club.__init__() in rbc.py)
    !! Plan to replace the above with functions  !!
    !! get_first_last() and get_last_first().    !!
    Or better still: pass a formatting string to the function
    """
    return club.PATTERN.format(**record)


def get_last_first(record):
    return "{last}, {first}".format(**record)


def get_first_last(record):
    return "{first} {last}".format(**record)
'''

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
        return set(record['status'].split(glbs.SEPARATOR))
        # above returns set of one empty string if status is empty
    else: return set()


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
    Hasn't yet attended any meetings
    """
    stati = get_status_set(record)
    if stati & {'a'}:
        return True
    else: return False


def is_inductee(record):
    '''
    '''
    stati = get_status_set(record)
    if stati & {'ai'}:
#       _ = input("{first} {last} is an inductee"
#           .format(**record))
        return True
    else:
        return False


def is_waiting(record):
    """
    """
    return 'aw' in get_status_set(record)


def is_member(record):
    """
    Tries to determine if record is that of a member (based on
    status field.)
    If there is a problem, will either append notice to
    club.errors (if it exists) or print out a warning.
    """
    if not record['status']:
        return True
    stati = get_status_set(record)
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
    """
    return 'am' in get_status_set(record)


def is_honorary_member(record):
    """
    """
    return 'h' in get_status_set(record)


def is_inactive_member(record):
    """
    """
    return 'm' in get_status_set(record)


def is_terminated(record):
    """
    """
    return 't' in get_status_set(record)


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
    if record["email"]:
        return True
    else:
        return False


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
        club.usps_only.append(demographic_f.format(**record))


def get_bad_emails(record, club):
    if 'be' in get_status_set(record):
        club.bad_emails.append(demographic_f.format(**record))


def get_secretary(record, club):
    """
    If record is that of the club secretary,
    assigns secretary's demographics to club.secretary
    """
    if 's' in record['status']:
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
    name = member_name(record, club)
    email = record['email']
    if email:
        club.email_by_m[name] = email


def add2db_emails(record, club):
    """
    Populates club.db_emails
    'ex' for experimental
    db_emails is a dict with all members included but
    with a special key for those without email
    """
#   print("called add2db_emails")
    name = member_name(record, club)
    email = record['email']
    if not email:
        email = NO_EMAIL_KEY
    club.db_emails[name] = email


def add2ms_by_email(record, club):
    """
    Populates club.ms_by_email, a dict keyed by emails one of which
    is NO_EMAIL_KEY to capture members without an email address.
    """
    name = member_name(record, club)
    email = record['email']
    if not email:
        email = NO_EMAIL_KEY
    _ = club.ms_by_email.setdefault(email, [])
    club.ms_by_email[email].append(name)


def add2stati_by_m(record, club):
    if record["status"]:
        record = helpers.Rec(record)
        club.stati_by_m[record(fstrings['first_last'])] = (
            get_status_set(record)  )


def add2ms_by_status(record, club):
    """
    Appends a record to club.ms_by_status:
        Each key is a status
        Each value is a list of strings:
            member names in last_first format
            of those having that status.
    """
    if record['status']:
        stati = get_status_set(record)
        for status in stati:
            _ = club.ms_by_status.setdefault(status, [])
            record = helpers.Rec(record)
            club.ms_by_status[status].append(
                    record(fstrings['last_first']))


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


def add2member_with_email_set(record, club):
    """
    Appends a record to club.member_with_email_set if record
    is that of a member and the member has an email address.
    ## Proposal: rename 'add2has_email_set' and store in 
                        'club.has_email_set'.
    """
    record = helpers.Rec(record)
    entry = record(fstrings['last_first'])
    if record['email']:
    # No reason to exclude non members!
        club.member_with_email_set.add(entry)
    else:
        club.no_email_set.add(entry)



def add2applicant_with_email_set(record, club):
    if is_applicant(record) and record['email']:
        club.applicant_with_email_set.add(
                record(fstrings['last_first']))


def add2fee_data(record, club):
    """
    Populates club.fee_category_by_m  and
    club.ms_by_fee_category if these attributes exist.
    """
    name = member_name(record, club)
    # print(repr(FEES_KEYS))
    for key in FEES_KEYS:
        # print("Checking key '{}' for {}".format(key, name))
        try:
            fee = int(record[key])
        except ValueError:
            # print("'{}' => ValueError".format(record[key]))
            continue
        capped = key.capitalize()
        # print("'{}' <=> {}".format(name, capped))
        if hasattr(club, 'ms_by_fee_category'):
            _ = club.ms_by_fee_category.setdefault(capped, [])
            club.ms_by_fee_category[capped].append((name, fee))
        if hasattr(club, 'fee_category_by_m'):
            _ = club.fee_category_by_m.setdefault(name, [])
            club.fee_category_by_m[name].append((capped, fee))


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
    name = member_name(record, club)
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
    for key in credit.keys():
        try:
            statement[key] -= credit[key]
        except KeyError:
            print('credit key is "{}"'.format(key))
            raise


def apply_credit2record(statement, record):
    """
    <statement> is a dict with (money key): (dollar amnt)
    money keys include "total"
    <record> is modified accordingly (ignoring the 'total' key
    """
    for key in [key for key in statement.keys() if key != 'total']:
        record[key] = int(record[key]) - statement[key]


def thank_func(record, club):
    """
    Must assign "payment" and extra" to record.
    """
    name = member_name(record, club)
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


#  update_db_re_payment_func(record, club):
notused = '''
def db_credit_payment(record, club):
    """
    Checks if record is in the club.statement_data dict and if so
    credits payment(s).  In either case data is moved to new
    db specified by club.dict_writer.
    """
    new_record = {}
    for key in record.keys():
        new_record[key] = record[key]
    name = member_name(record, club)
    if name in club.statement_data_keys:
        apply_credit2record(club.statement_data[name], new_record)
    club.dict_writer.writerow(new_record)
'''

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


def credit_payment_func(record, club):
    """
    Returns the <record>, modified by crediting payment(s)
    specified in club.statement_data
    """
    name = member_name(record, club)
    if name in club.statement_data.keys():
        apply_credit2record(club.statement_data[name], record)
    return record


def modify_data(csv_in_file_name, func, club):
    """
    A generator: yields the return value of
    <func>(record) for each record read from the
    csv file named <csv_in_file_name>.
    <club> provides a method of passing values prn.
    """
    with open(csv_in_file_name, 'r', newline='') as file_obj:
        reader = csv.DictReader(file_obj)
        for rec in reader:
#           record = helpers.Rec(record)
#           Not needed because not doing any string formatting.
            yield func(rec, club)


def get_name_key_from_line(line):
    """
    """
    parts = line.split()
    return "{1}, {0}".format(*parts)


def show_by_status(by_status,
                   stati2show=STATI,
                   club=None):
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
            for line in by_status[status]:
                ret.append(line)
                if hasattr(club, 'applicant_data'):
                    key = get_name_key_from_line(line)
                    if key in club.applicant_data_keys:
                        # create a line of dates
                        dates_attended = data.line_of_meeting_dates(
                                        club.applicant_data[key])
                        if dates_attended:
                            ret.append("\tDate(s) attended: {}"
                                    .format(dates_attended))
                        else:
                            ret.append("\tNo meetings attended.")
#                       print("Applicant data: {}".format(
#                           club.applicant_data[key].__repr__()))
                        sponsors = club.applicant_data[key]['sponsors']
                    else:
                        pass
#                       print("{} has no dates!!".format(key))
                    if sponsors:
                        print(sponsors)
                        sponsor_line = ', '.join(
                                [helpers.tofro_first_last(sponsor)
                                for sponsor in sponsors])
#                       print(sponsors)
                        ret.append("\tSponsors: {}"
                                        .format(sponsor_line))
                    else:
                        pass
#                       print("{} has no sponsors!!".format(key))
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
    ret = dict()
    ret['total'] = 0
    for key in MONEY_KEYS:
        if record[key]:
            ret[key] = int(record[key])
            ret['total'] += ret[key]


    return ret


def add2statement_data(record, club):
    club.statement_data[
        member_name(record, club)] = get_statement_dict(record)


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


notused = '''
def get_statement_data(statement_data, club=None):
    """
    Returns an array of strings:  a statement for each record/member.
    """
    ret = []
    for name in statemenet_data_keys.keys():
        line = "{: <21}".format(name)
        statement = get_statement(statement_data[name], club)
        if club and club.inline:
            ret.append(line + statement)
        else:
            ret.append(line)
            ret.append(statement)
    return '\n'.join(ret)
'''

def assign_statement2extra_func(record, club=None):
    """
    Sets up record['extra'] to contain a statement with
    appropriate suffix for dues & fees notice.
    """
    d = get_statement_dict(record)
    extra = ['Statement of account:', ]
    if d['total'] == 0:
        extra.append("You are all paid up. Thank you.")
    else:
        extra.append(get_statement(d))
    if d['total'] < 0:
        extra.extend(["You have a credit balance.",
                      "Thank you for your advanced payment."])
    record['extra'] = '\n'.join(extra)


def get_payables(record, club):
    """
    Populates club.still_owing and club.advance_payments
    which are lists that must be set up by the client.

    Checks record for dues &/or fees. If found,
    positives are added to club.still_owing,
    negatives to club.advance_payments.
    """
    if 'r' in get_status_set(record):
        return
    name = "{last}, {first}: ".format(**record)
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
              club.inductees, club.by_n_meetings and
####### Change "by_n_meetings" to "by_applicant_status"
              club.errors (initially empty lists)
    and increments club.nmembers,
                   club.napplicants and
                   club.ninductees (initially set to 0.)
    <club> is an instance of rbc.Club.
    """
#   line = name_w_demographics(record, club)
    line = fstrings['first_last_w_all_data'].format(**record)
    if is_member(record):
        first_letter = record['last'][:1]
        if club.for_web:
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
    if is_applicant(record):
        stati = get_status_set(record)
        status = stati & APPLICANT_SET
        assert len(status) == 1
#       if 'a0' in status:
#           print("{} found".format(member_name(record, club)))
        club.napplicants += 1
        s = status.pop()
        _ = club.by_n_meetings.setdefault(s, [])
        club.by_n_meetings[s].append(line)
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
    name = member_name(record, club)
    for key in MONEY_KEYS:
        try:
            money = int(record[key])
        except ValueError:
            money = 0
        if money:
            _ = club.non0balance.setdefault(name, {})
            club.non0balance[name][key] = money


def populate_name_set_func(record, club):
    club.name_set.add(member_name(record, club))


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
        name = get_last_first(record)
        if name in club.extra_fee_names:
            for (category, amount) in club.by_name[name]:
                category = category.lower()
                new_record[category] = helpers.str_add(
                    amount,
                    new_record[category])
    club.new_db.append(new_record)


# #### Next group of methods deal with sending out mailings. #######
# Clients must set up the following attributes of the 'club' parameter
# typically an instance of the Membership class:
#    email, letter, json_data,


def append_email(record, club):
    """
    club.which has already been assigned to one of the values
    of content.content_types
    Returns a list of dicts.
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
    if club.cc_sponsors:
        record = helpers.Rec(record)
        name_key = record(fstrings['last_first'])
        if name_key in club.applicant_set:
            sponsors = club.sponsors_by_applicant[name_key]
            # Use list comprehension for the following:
            sponsor_email_addresses = []
            for sponsor in club.sponsors_by_applicant[name_key]:
                print('{} sponsor: {}'.format(name_key, sponsor))
                print('appending: {}'.format(
                                club.sponsor_emails[sponsor]))
                addr = club.sponsor_emails[sponsor]
                if addr:
                    sponsor_email_addresses.append(addr)
            sponsor_email_addresses = ','.join(
                    sponsor_email_addresses)
        else: sponsor_email_addresses = ''
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
    Checks on desired type of mailing and
    deals with mailing as appropriate.
    Decides wich (if any or both) of the following to call:
    file_letter   or
    append_email
    """
    record["subject"] = club.which["subject"]
    if (record['status'] and 'be' in record['status']
            and not club.which["e_and_or_p"] == "email"):
        # If only sending emails...
        # don't want to send a letter (even if known bad email.)
        file_letter(record, club)
    elif club.which["e_and_or_p"] == "email":
        append_email(record, club)
    elif club.which["e_and_or_p"] == "both":
        if record['email']:
            append_email(record, club)
        file_letter(record, club)
    elif club.which["e_and_or_p"] == 'one_only':
        if record['email']:
            append_email(record, club)
        else:
            file_letter(record, club)
    elif club.which["e_and_or_p"] == 'usps':
        file_letter(record, club)
    else:
        print("Problem in q_mailing re {}".format(
                    "{last}, {first}".format(**record)))
        assert False


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
    # No point in creating a json file if no emails:
    if club.json_data:
        print("There is email to send.")
        with open(club.json_file, 'w') as file_obj:
            print('Dumping JSON to "{}".'.format(file_obj.name))
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
        if club.cc_sponsors:
            pass
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


redactyesno = '''
def test_func(record, club=None):
    """
    Can be used as a prototype or can be used for testing.
    Populates record["extra"]
    """
    pass
'''

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
    add2db_emails: [
        "club.db_emails = {}",
        ],
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
    add2demographics: [
        'club.demographics = {}',
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
        'club.by_n_meetings = {}',
        'club.napplicants = 0',
        'club.errors = []',
        ],
    get_payables: [
        'club.still_owing = []',
        'club.advance_payments = []',
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
    db_apply_charges: [
        "club.new_db = {}",
        ],
    add2statement_data: [
        'club.statement_data = {}',
        ],
    #   add2status_data: [
    #       'club.ms_by_status = {}',
    #       ],
    add_dues_fees2new_db_func: [
        'club.new_db = []',
        ]
    }


func_dict['rm_email_only_field'] = (
    rm_email_only_field,
    ("first", "last", "phone", "address", "town", "state",
     "postal_code", "country", "email", "dues", "dock",
     "kayak", "mooring", "status",
     )
    )


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


if __name__ == "__main__":
    print("member.py compiles OK.")
    
    temporarilyredacted = '''
else:
    def print(*args, **kwargs):
        pass
'''

