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
from rbc import Club

SEPARATOR = '|'  ### Note: NOT the same as rvc.SEPARATOR
WAIVED = "w"     #   \ although its value happens to be the same.
STATUS_KEY_VALUES = {
    "a0": "Application received",
    "a1": "Attended one meeting",
    "a2": "Attended two meetings",
    "a3": "Attended three (or more) meetings",
    "ai": "Inducted, membership pending payment of dues",
    "aw": "Inducted, awaiting vacancy and then payment",
    "be": "Email on record being rejected",
    "ba": "Postal address => mail returned",
    "h": "Honorary Member",
    "m": "New Member",  # temporary until congratulatory letter.
    'r': "Retiring/Giving up Club Membership",
    's': "Secretary of the Club",  # not used under Rafferty
    "w": "Fees being waived",  # a rarely applied special status
    }
STATI = sorted([key for key in STATUS_KEY_VALUES.keys()])
APPLICANT_STATI = STATI[:6]
APPLICANT_SET = set(STATI[:6])
MISCELANEOUS_STATI = "m|w|be"
NON_MEMBER_SET = APPLICANT_SET | set("h")

N_FIELDS = 15  # Only when unable to use len(dict_reader.fieldnames).
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

N_FIELDS_PER_RECORD = 15

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

def setup_required_attributes(custom_funcs, club):
    """
    Ensures that club has necessary attributes
    required by all the custom_funcs to be called.
    """
    set_of_funcs = set(prerequisites.keys())
    for func in custom_funcs:
#       print("func is '{}'".format(func))
        if func in set_of_funcs:
            for code in prerequisites[func]:
                exec(code)


def traverse_records(infile, custom_funcs, club):
    """
    Traverses <infile> and applies <custom_funcs> to each
    record.  <custom_funcs> can be a single function or a
    list of functions. These functions typically require a
    <club> parameter, an instance of the "Club" class which
    for the Bolinas Rod and Boat Club is found in the
    module rbc.py.
    Generally each <custom_func> will leave its results in
    one of the "club" attributes (similarly named.)  These
    custom funcs are mostly found in this ('member.py')
    module.
    """
    if callable(custom_funcs): # If only one function provided
        custom_funcs = [custom_funcs] # place it into a list.
    setup_required_attributes(custom_funcs, club)
    with open(infile, 'r', newline='') as file_object:
        print("DictReading {}".format(file_object.name))
        dict_reader = csv.DictReader(file_object, restkey='extra')
        # fieldnames is used by get_usps and restore_fees cmds.
        club.fieldnames = dict_reader.fieldnames  # used by get_usps
        club.n_fields = len(club.fieldnames)  # to check db integrity
        for record in dict_reader:
            for custom_func in custom_funcs:
                custom_func(record, club)


def member_name(record, club):
    """
    Returns a string formated as defined by club.pattern.
    Default <pattern> is "{last}, {first}"...
    (see Club.__init__() in rbc.py)
    """
    return club.pattern.format(**record)


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
    record.n_fields = len(record)
    possible_error = ("{last} {first} has {N_FIELDS}"
        .format(**record))
    if ((club and (record.n_fields != club.n_fields))
    or record.n_fields != N_FIELDS):
        report_error(possible_error, club)


def get_status_set(record):
    if record['status']:
        return set(record['status'].split(SEPARATOR))
    return set()


def is_applicant(record):
    """
    Tests whether or not <record> is an applicant.
    """
    stati = get_status_set(record)
    if stati & APPLICANT_SET:
        return True
    return False


def is_member(record):
    """
    Tries to determine if record is that of a member (based on
    status field.)
    If there is a problem, will either append notice to
    club.errors (if it exists) or print out a warning.
    """
    if not record['status']: return True
    stati = get_status_set(record)
    if stati.intersection(set(NON_MEMBER_SET)): return False 
    if 'm' in stati: return True
    return True


def is_honorary_member(record):
    """
    """
    return 'h' in get_status_set(record)


def increment_napplicants(record, club):
    """
    """
    if is_applicant(record):
        print("{} => n_applicants".format(member_name(record, club)))
        club.napplicants += 1


def increment_nmembers(record, club):
    """
    Client must initiate club.nmembers(=0) attribute.
    If record is that of a member, nmembers is incremented.
    """
    if is_member(record):
        club.nmembers += 1

def is_member_or_applicant(record, club=None):
    return is_member(record) or is_applicant(record)


def has_valid_email(record, club=None):
    if (record["status"]
    and 'be' in record['status'].split(SEPARATOR)):
        return False
    if record["email"]:
        return True
    else:
        return False


def letter_returned(record, club=None):
    return 'ba' in get_status_set(record)
#   if (record["status"]
#   and 'ba' in record['status'].split(SEPARATOR)):
#       return True
#   else:
#       return False


def is_fee_paying_member(record, club=None):
    """
    """
    return (is_member(record)
            and get_status_set(record).isdisjoint(
                set(('h', 'r', 'w'))
                )
            )


def get_usps(record, club):
    """
    Selects members who get their copy of meeting minutes by US
    Postal Service. i.e. Those with no email.
    Populates self.usps_only with a line for each such member
    using csv format: first, last, address, town, state, and
    postal_code.
    """
    if not record['email']:
        club.usps_only.append(
            "{first},{last},{address},{town},{state},{postal_code}"
            .format(**record))


def get_bad_emails(record, club):
    if 'be' in get_status_set(record):
        club.bad_emails.append(
            "{first},{last},{address},{town},{state},{postal_code}"
            .format(**record))


def get_secretary(record, club):
    """
    If record is that of the club secretary,
    assigns secretary's demographics to club.secretary
    """
    if 's' in record['status']:
        club.secretary = (
            "{first},{last},{address},{town},{state},{postal_code}"
            .format(**record))

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
            club.zeros.append("{last}, {first}: {dues}"
                                                .format(**record))


## Beginning of 'add2' functions:


def add2m_by_name(record, club):
    """
    REDACT! use add2email_by_m
            and add2stati_by_m
    Adds to already existing dict club.m_by_name which is
    keyed by "name" with value also a dict with keys:
    ["email"] => email as a string
    ["stati"] => stati as a set
    """
    club.m_by_name[member_name(record, club)] = dict(
        email= record['email'],
        stati= {status for status in record["status"].split(
        SEPARATOR)})


def add2email_data(record, club):
    """
    Populates club.email_by_m  and (if it
    exists)   club.ms_by_email.
    """
    name = member_name(record, club)
    email = record['email']
    if email:
        club.email_by_m[name] = email
        if hasattr(club, 'ms_by_email'):
            _ = club.ms_by_email.setdefault(email, [])
            club.ms_by_email[email].append(name)
    else:
        if hasattr(club, "without_email"):
            club.without_email.append(name)


def add2status_data(record, club):
    """
    Populates club.ms_by_status: lists of members keyed by status.
    Also populates club.stati_my_m if attribute exists...
    and increments club.napplicants if attribute exists.
    """
    if not record["status"]:
        return
#   if is_applicant(record) and hasattr(club, "napplicants"):
#       club.napplicants += 1
    name = club.pattern.format(**record)
    for status in get_status_set(record):
        _ = club.ms_by_status.setdefault(status, [])
        if status == 'be':
            club.ms_by_status[status].append(name + 
                " ({})".format(record['email']))
        else:
            club.ms_by_status[status].append(name)
        if hasattr(club, 'stati_by_m'):
            _ = club.stati_by_m.setdefault(name, set())
            club.stati_by_m[name].add(status)


def add2fee_data(record, club):
    """
    Populates club.fee_category_by_m  and
    club.ms_by_fee_category if these attributes exist.
    """
    name = member_name(record, club)
#   print(repr(FEES_KEYS))
    for key in FEES_KEYS:
#       print("Checking key '{}' for {}".format(key, name))
        try:
            fee = int(record[key])
        except ValueError:
#           print("'{}' => ValueError".format(record[key]))
            continue
        capped = key.capitalize()
#       print("'{}' <=> {}".format(name, capped))
        if hasattr(club, 'ms_by_fee_category'):
            _ = club.ms_by_fee_category.setdefault(capped, [])
            club.ms_by_fee_category[capped].append((name,fee))
        if hasattr(club, 'fee_category_by_m'):
            _ = club.fee_category_by_m.setdefault(name, [])
            club.fee_category_by_m[name].append((capped, fee))


def add2malformed(record, club=None):
    """
    Populates club.malformed (which must be set up by client.)
    Checks that that for each record:
    1. there are N_FIELDS_PER_RECORD
    2. the money fields are blank or evaluate to an integer.
    3. the email field contains "@"
    club.__init__ sets club.previous_name to "".
    (... used for comparison re correct ordering.)
    Client must set up a club.malformed[] empty list to be populated.
    """
    name = member_name(record, club)
    if len(record) != N_FIELDS:
        club.malformed.append("{}: Wrong # of fields."
            .format(name))
    for key in MONEY_KEYS:
        value = record[key]
        if value:
            try:
                res = int(value)
            except ValueError:
#                   if value == 'w':
#                       continue
                club.malformed.append("{}, {}:{}"
                    .format(name, key, value))
    if record["email"] and not '@' in record["email"]:
#       for key in record.keys():
#           print("{}: {}".format(key, record[key]))
        club.malformed.append("{}: {} Problem /w email."
            .format(name, record['email']))
    if name < club.previous_name:
        club.malformed.append("Record out of order: {}"
            .format(name))
    club.previous_name = name

# End of 'add2...' functions


def apply_credit2statement(statement, credit):
    """
    credit is used to modify statement- both are dicts
    """
    for key in credit.keys():
        statement[key] -= credit[key]


def apply_credit2record(statement, record):
    """
    """
    keys = [key for key in statement.keys() if key != 'total']
    print("Keys are {}".format(keys))
    for key in keys:
#   for key in [key for key in statement.keys() if key != 'total']:
        record[key] = int(record[key]) - statement[key]


def thank_func(record, club):
    """
    Must assign "payment" and extra" to record.
    """
    name = member_name(record, club)
    if name in club.statement_data_keys:
#       print(get_statement(club.statement_data[name]))
        payment = club.statement_data[name]['total']
        statement_dict = get_statement_dict(record)
        apply_credit2statement(statement_dict, club.statement_data[name])
        record['extra'] = get_statement(statement_dict)
        record['payment'] = payment
        q_mailing(record, club)
    # Still need to move record to new db

# The next two functions add entries to club.new_db 

def update_db_re_payment_func(record, club):
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


def update_db_apply_charges_func(record, club):
    pass

# .. above two functions write to new db with updated information.


def show_stati(club):
    """
    Returns a list of strings (that can be '\n'.join(ed))
    The default is to include every status found.
    <mode> parameter must be one of the following:
        'all'                   }  both self
        'applicants_only'       } explanatory
        a SEPARATOR separated listing of all stati to be included
    See client: utils.stati_cmd().
    """
    print("Debug: mode is set to '{}'.".format(club.mode))
    print("Preparing listing of stati.")
    err_code = traverse_records(club.infile,
                                    add2status_data,
                                    club)
    if not club.ms_by_status:
        return ["Found No Entries with 'Status' Content." ]
    ret = []
    if club.mode == 'all':
        stati2show = STATI
    elif club.mode == 'applicants_only':
        stati2show = APPLICANT_STATI
    else:
        try:
            stati2sshow = club.mode.split(SEPARATOR)
        except AttributeError:
            print(
            'Bad "mode" parameter ({}) provided to stati function.'
                .format(mode))
            print('Must exit!')
            raise
            sys.exit()
    keys = [k for k in club.ms_by_status.keys()]
    keys.sort()
#   print(keys)

    do_it_once = True
    for key in keys:
        if key in stati2show:
            sub_header = STATUS_KEY_VALUES[key]
            values = sorted(club.ms_by_status[key])
            if key.startswith('a'):
                if do_it_once:
                    helpers.add_header2list("Applicants", ret,
                                        underline_char='=')
                    do_it_once = False
                helpers.add_header2list(sub_header, ret,
                                        underline_char='-')
            else:
                helpers.add_header2list(sub_header, ret,
                                        underline_char='=')
            for value in values:
                ret.append("    {}".format(value))
    return ret


def show_by_status(by_status, stati2show=STATI):
    """
    Returns a list of strings (which can be '\n'.join(ed))
    Each 'status' is a header followed by the list of members.
    """
    ret = []
    stati = by_status.keys()
    for status in sorted(stati):
        if status in stati2show:
            helpers.add_header2list(STATUS_KEY_VALUES[status],
                                        ret, underline_char='-')
            for line in by_status[status]:
                ret.append(line)
    return ret


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
    Returns an array of strings making up a
    statement of dues and fees.
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


def assign_statement2extra_func(record, club=None):
    """
    Sets up record['extra'] to contain a statement with
    appropriate suffix for dues & fees notice.
    """
    d = get_statement_dict(record)
    extra = ['Statement of account:',]
    if d['total'] == 0:
        extra.append("You are all paid up. Thank you.")
    else:
        extra.extend(get_statement(d))
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
                line_positive.append("{} {:>3d}".format(
                    key, amount))
#                       MONEY_HEADERS[key], amount))
            elif amount < 0:
                line_negative.append("{} {:>3d}".format(
                    key, amount))
    if line_positive:
        line = ("{:<26}".format(name)
                    + ', '.join(line_positive))
        club.still_owing.append(line)
    if line_negative:
        line = ("{:<26}".format(name)
                    + ', '.join(line_negative))
        club.advance_payments.append(line)



def add2list4web(record, club):
    """
    Client is expected to provide <club>, an instance of rbc.Club,
    with the following attributes in place:
        pattern
        members = []        &  nmembers = 0
        honorary = []      &  nhonorary = 0
        by_n_meetings = {}  &  napplicants = 0
        errors = []
    Populates club.members, club.stati, club.applicants,
    Club.inductees and club.errors (initially empty lists)
    and increments club.nmembers, club.napplicants
    and club.ninductees (initially set to 0.)
    All these attributes (of 'club', an instance of utils.membership
    class) must be set up by the client.
    """
    stati = get_status_set(record)
    if not record['email']: record['email'] = 'no email'
    if not record['phone']: record['phone'] = 'no phone'
    line = club.pattern.format(**record)
    if "be" in stati:
        line = line + " (bad email!)"
        club.errors.append(line)
    if is_member(record): 
        first_letter = record['last'][:1]
        if first_letter != club.first_letter:
#           print("changing first letter from {} to {}"
#               .format(club.first_letter, first_letter))
            club.first_letter = first_letter
            club.members.append("")
        club.nmembers += 1
        club.members.append(line)
    if is_applicant(record):
        status = stati & APPLICANT_SET
        assert len(status)==1
        club.napplicants += 1
        s = status.pop()
        _ = club.by_n_meetings.setdefault(s, [])
        club.by_n_meetings[s].append(line)
    if is_honorary_member(record):
        club.honorary.append(line)
        club.nhonorary += 1
                

def dues_and_fees(record, club):
    """
    ## A work in progress!! ##
    Populates following attributes of club:
        null_dues (if giving up membership should have 'r' in
                    status else probably an error condition!)
        members_owing
        members_zero_or_cr
        dues_balance
        fees_balance
        retiring
        applicants
        errors
    """
    name = member_name(record, club)
    entry = {}
    try:
        value = int(record['dues'])
    except ValueError:
        status_set = get_status_set(record)
        club.null_dues.append(name)
        if 'r' in status_set:
            club.retiring.append(name)
        elif status_set & APPLICANT_SET:
            club.applicants.append(name)
        else:
            report_error("{}: Unexplained null in dues field."
                        .format(name), club)
    else:
        formatted_value = helpers.format_dollar_value(value)
        if value > 0:
            club.members_owing.append("{}: {}"
                            .format(name, formatted_value))
        elif value <= 0:
            club.members_zero_or_cr.append("{}: {}"
                            .format(name, formatted_value))
        else:
            assert False
        club.dues_balance += value
    for key in FEES_KEYS:
        fees = []
        try:
            value = int(record[key])
        except ValueError:
            pass
        else:
            formatted_value = helpers.format_dollar_value(value)
            fees.append("{} {}"
                        .format( key.capitalize(), formatted_value))
    if fees:
        fees = ', '.join(fees)


def populate_non0balance_func(record, club):
    """
    Reads the MONEY_KEYS fields and, if any are not zero,
    populates the club.non0balance dict keyed by member name
    with values keyed by MONEY_KEYS.
    """
    total = 0
    name = record.name()
    for key in MONEY_KEYS:
        try:
            money = int(record[key])
        except ValueError:
            club.errors.append("{}: {} {} => ValueError."
                .format(member_name(record), key, record[key]))
            money = 0
        if money:
            _ = club.non0balance.get(name, {})
            club.non0balance[name][key] =  money


def populate_name_set(record, club):
    club.name_set.add(name(record))


def add_dues_fees2new_db_func(record, club):
    pass



##### Next group of methods deal with sending out mailings. #######
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
    sender =  club.which['from']['email']
    email = {
        'From': sender,    # Mandatory field.
        'Sender': sender,   # 0 or 1
        'Reply-To': club.which['from']['reply2'],  # 0 or 1
        'To': record['email'],  # O or 1 comma separated list.
        'Cc': None,             # O or 1 comma separated list.
        'Bcc': None,            # O or 1 comma separated list.
        'Subject': club.which['subject'],  # 0 or 1
        'attachments': [],
        'body': body,
    }
    if club.cc:
        email['Cc'] = club.cc
    if club.bcc:
        email['Bcc'] = club.bcc
    club.json_data.append(email)

def file_letter(record, club):
    entry = club.letter.format(**record)
    path2write = os.path.join(club.dir4letters,
        "_".join((record["last"], record["first"])))
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
    if (record['status']
    and 'be' in record['status']
    and not club.which["e_and_or_p"] == "email"):
    # If only sending emails...
    # don't want to send a letter (even if known bad email.)
        file_letter(record, club)
    elif club.which["e_and_or_p"] == "email":
        append_email(record, club)
    elif club.which["e_and_or_p"] == "both":
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
        print("Problem in q_mailing re {}"
            .format("{last}, {first}".format(**record)))
        assert False

def prepare_mailing(club):
    """
    Only client of this method is the utils.prepare_mailing_cmd
    which uses command line args to assign attributes to club.
    (See Notes/call_flow.)
    """
    traverse_records(club.input_file_name, 
        club.which["funcs"], club)  # 'which' comes from content

    # No point in creating a json file if no emails:
    if club.json_data:
        print("There is email to send.")
        with open(club.json_file_name, 'w') as file_obj:
            print('Dumping JSON to "{}".'.format(file_obj.name))
            file_obj.write(json.dumps(club.json_data))
    else:
        print("There are no emails to send.")


### The following are functions used for mailing. ###
## These are special functions suitable for the <func_dict>:
## they provide necessary attributes to their 'record' parameter
## in order to add custom content (to a letter &/or email.)

def std_mailing_func(record, club):
    """
    Assumes any prerequisite processing has been done and
    requisite values added to record.
    Mailing is sent if the "test" lambda => True.
    Otherwise the record is ignored.
    """
    if club.which["test"](record):
        record["subject"] = club.which["subject"]
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


def request_inductee_payment_mailing_func(record, club):
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


def test_func(record, club=None):
    """
    Can be used as a prototype or can be used for testing.
    Populates record["extra"]
    """
    pass

### ... end of mailing functions.  ###


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

prerequisites = {
    increment_nmembers: [
        "club.nmembers = 0",
        ],
    increment_napplicants: [
        "club.napplicants = 0",
        ],
    get_usps: [
        'club.usps_only = []',
        ],
    get_zeros_and_nulls: [
        'club.nulls = []',
        'club.zeros = []',
        ],
    add2m_by_name: [
        'club.m_by_name = {}',
        ],
    add2email_data: [
        'club.email_by_m = {}',
        'club.ms_by_email = {}',
        ],
    add2status_data: [
        'club.ms_by_status = {}',
        'club.napplicants = 0',
        'club.stati_by_m = {}',
        ],
    add2fee_data: [
        'club.fee_category_by_m = {}',
        'club.ms_by_fee_category = {}',
        ],
    add2malformed: [
        'club.malformed = []',
        ],
    add2list4web: [
        """club.pattern = ("{first} {last}  [{phone}]  {address}, " +
                    "{town}, {state} {postal_code} [{email}]")""",
        'club.members = []',
        'club.nmembers = 0',
        'club.honorary = []',
        'club.nhonorary = 0',
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
    dues_and_fees: [
        'club.null_dues = []',
        'club.members_owing = []',
        'club.members_zero_or_cr = []',
        'club.dues_balance = 0',
        'club.fees_balance = 0',
        'club.retiring = []',
        'club.applicants = []',
        'club.errors = []',
        ],
    populate_non0balance_func: [
        "club.errors = []",
        "club.non0balance = []",
        ],
    populate_name_set: [
        "club.name_set = set()",
        ],
    append_email: [
        "club.json_data = []",
        ],
#   update_db_payment_func: [
#       "club.new_db = {}",
#       ],
    update_db_apply_charges_func: [
        "club.new_db = {}",
        ],
    add2statement_data: [
        'club.statement_data = {}',
        ],
    add2status_data: [
        'club.ms_by_status = {}',
        ],
    }

if __name__ == "__main__":
    print("member.py compiles OK.")
