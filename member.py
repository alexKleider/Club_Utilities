#!/usr/bin/env python3

# File: member.py

"""
Many methods of Membership class are essentially
independant of Membership but pertain to each record.
Hence makes sense to separate them out.
A few/some need to store data so those will get an extra
(named) parameter: 'club=None'.
"""

import os
import csv
import json
import helpers
# import content

STATUS_SEPARATOR = ':'
WAIVED = "w"
status_key_values = {
    "a0": "Application received.",
    "a1": "Attended one meeting.",
    "a2": "Attended two meetings.",
    "a3": "Attended three (or more) meetings.",
    "ai": "Inducted, membership fee pending.",
    "m": "Member in good standing.",
    WAIVED: "Fees being waived.",
    "be": "Email on record doesn't work.",
    }
STATI = sorted([key for key in status_key_values.keys()])
NON_MEMBER_STATI = STATI[:5]
APPLICANT_SET = set(STATI[:5])

n_fields = 15
money_keys = ("dues", "mooring", "dock", "kayak") 
fees_keys = money_keys[1:]
money_headers = {
    "dues":    "Dues..........",
    "mooring": "Mooring.......",
    "dock":    "Dock Usage....",
    "kayak":   "Kayak Storage.",
    "total":   "TOTAL.........",
    }

n_fields_per_record = 15

def traverse_records(infile, custom_funcs, club):
    """
    Traverses <infile> and applies <custom_funcs> to each
    record.  <custom_funcs> can be a single function or a
    list of functions. These functions typically require a
    named parameter "club" which will be an instance of the
    'Membership' (this) class.
    Generally each <custom_func> will leave its results in
    one of the "club" attributes (similarly named.)  These
    custom funcs are mostly found in the this ('member.py')
    module although initially they were methods of the
    Membership class in the 'utils.py' module (and some may
    still be.) Their names often begin with 'get_'.
    (Also used for mailings.)
    """
    if callable(custom_funcs):
        custom_funcs = [custom_funcs]
    with open(infile, 'r') as file_object:
        print("Opening {}".format(infile))
        dict_reader = csv.DictReader(file_object, restkey='status')
# Do we need the next two lines??
#       club.fieldnames = dict_reader.fieldnames
#       club.n_fields = len(self.fieldnames)
        for record in dict_reader:
            for custom_func in custom_funcs:
                custom_func(record, club)

def is_applicant(record, club=None):
    stati = record['status'].split(STATUS_SEPARATOR)
    for status in stati:
        if status in APPLICANT_SET: 
            return True
    return False

def is_member(record, club=None):
    """
    Tries to determine if record is that of a member (based on
    status field.)
    If there is a problem, will either append notice to
    club.errors (if it exists) or print out a warning.
    """
    stati = record['status'].split(STATUS_SEPARATOR)
    for status in NON_MEMBER_STATI:
        if status in stati:
            return False
    if (
        stati == [''] or  # blank for most members
        "m" in stati or  # member
        stati == ['be'] or  # bad email
        #    Notice the '==', not '"be" in ..'
        "w" in stati   # fees waved
        ):
        return True
    error = ("Problem in 'is_member' with {}."
        .format("{last}, {first}".format(**record)))
    try:
        club.errors.append(error)
    except AttributeError:
        print(error)


#   def is_member(self, record):
#       """
#       Anyone who is not an applicant.
#       """
#       return not self.is_applicant(record)

def is_fee_paying_member(record, club=None):
    """
    """
    if WAIVED in record['status'].split(STATUS_SEPARATOR):
        return False
    if self.is_member(record):
        return True

def add2stati_by_status(record, club=None):
    """
    Prerequisite: club.stati_dict
    Populates club.stati_dict (which must be set up by
    client) with lists of member names (last, first) keyed
    by status.
    """
    stati = record["status"].split(STATUS_SEPARATOR)
    for status in stati:
        _ = self.stati_dict.setdefault(status, [])
        club.stati_dict[status].append(
                    "{last}, {first}".format(**record))

def not_paid_up(record, club=None):
    """
    Checks if there is a positive balance in any of the money fields.
    """
    for key in money_keys:
      if record[key] and int(record[key]) > 0:
        return True
    return False

def get_owing(record, club):
    """
    Calculates debit/credit for member represented by 'record'
    and stores the resulting dict as an 'owing' attribute of
    'club' (which provides a _temporary_ value for another
    function to use if need be.)
    """
    owing = dict()
    for key in money_keys:
        if record["key"]:
            owing["key"] = int(record["key"])
        else:
            owing["key"] = 0
    club.owing = owing

def append2Dr(record, club):
    """
    """
    pass

def get_payables(record, club=None):
    """
    Populates club.still_owing and club.advance_payments which
    must be set up by the client.

    Checks record for dues &/or fees. If found,
    positives are added to club.still_owing,
    negatives to club.advance_payments.
    """
    name = "{last}, {first}: ".format(**record)
    line_positive = []
    line_negative = []
    for key in money_keys:
        if record[key]:
            amount = int(record[key])
            if amount != 0:
                if amount > 0:
                    assert amount > 0
                    line_positive.append("{} {}".format(
                        money_headers[key], amount))
                elif amount < 0:
                    assert amount < 0
                    line_negative.append("{} {}".format(
                        money_headers[key], amount))
                else:
                    assert False
    if line_positive:
        line = (name + ', '.join(line_positive))
        club.still_owing.append(line)
    if line_negative:
        line = (name + ', '.join(line_negative))
        club.advance_payments.append(line)

def add2malformed(record, club=None):
    """
    Populates club.malformed (which must be set up by client.)
    Checks that that for each record:
    1. there are n_fields_per_record
    2. the money fields are blank or evaluate to an integer.
    3. the email field contains "@"
    club.__init__ sets club.previous_name_tuple to ("", "")
    (... used for comparison re correct ordering.)
    Client must set up a club.malformed[] empty list to be populated.
    """
    name_tuple = (record["last"], record["first"])
    if len(record) != n_fields:
        club.malformed.append("{}, {}: Wrong length."
            .format(record['last'], record['first']))
    for key in money_keys:
        value = record[key]
        if value:
            try:
                res = int(value)
            except ValueError:
#                   if value == 'w':
#                       continue
                club.malformed.append("{}, {}, {}:{}"
                    .format(record['last'], record['first'],
                    key, value))
    if record["email"] and not '@' in record["email"]:
        club.malformed.append("{}, {}: Problem /w email."
            .format(record['last'], record['first']))
    if name_tuple < club.previous_name_tuple:
        club.malformed.append("Record out of order: {0}, {1}"
            .format(*name_tuple))
    club.previous_name_tuple = name_tuple

def add2status_list(record, club=None):
    """
    Populates club.status_list (which must be set up by client.)
    """
    if record["status"]:
        club.status_list.append(("{last}, {first} - {status}"
            .format(**record)))

def is_member(record, club=None):
    """
    Tries to determine if record is that of a member (based on
    status field.)
    If there is a problem, will either append notice to
    club.errors if it exists, or cause program to fail.
    """
    if record['status']==None:
        return True
    stati = record['status'].split(STATUS_SEPARATOR)
    for status in NON_MEMBER_STATI:
        if status in stati:
            return False
    if (
        stati == [''] or  # blank for most members
        "m" in stati or  # member
        stati == ['be'] or  # bad email
        #    Notice the '==', not '"be" in ..'
        "w" in stati   # fees waved
        ):
        return True
    error = ("Problem in 'member.is_member' with {}."
        .format("{last}, {first}".format(**record)))
    print(error)

def add2stati_by_status(record, club=None):
    """
    Prerequisite: club.stati_dict
    Populates club.stati_dict (which must be set up by
    client) with lists of member names (last, first) keyed
    by status.
    """
    stati = record["status"].split(STATUS_SEPARATOR)
    for status in stati:
        _ = club.stati_dict.setdefault(status, [])
        club.stati_dict[status].append(
                    "{last}, {first}".format(**record))

def add2memlist4web(record, club=None):
    """
    Populates club.members, club.stati, club.applicants,
    club.inductees and club.errors (initially empty lists)
    and increments club.nmembers, club.napplicants
    and club.ninductees (initially set to 0.)
    All these attributes (of 'club', an instance of utils.membership
    class) must be set up by the client.
    """
    line = (
"{first} {last}  {phone}  {address}, {town}, {state} {postal_code}  {email}"
            .format(**record))
    if record["status"] and "be" in record["status"]:
        line = line + " (bad email!)"
    if is_member(record): 
        first_letter = record['last'][:1]
        if first_letter != club.first_letter:
#           print("changing first letter from {} to {}"
#               .format(club.first_letter, first_letter))
            club.first_letter = first_letter
            club.members.append("")
        club.nmembers += 1
        club.members.append(line)
    elif 'a' in record["status"]:
        club.applicants.append(line)
        club.napplicants += 1
    elif 'i' in record["status"]:
        club.inductees.append(line)
        club.ninductees += 1
    else:
        club.errors.append(line)

##### Next group of methods deal with sending out mailings. #######
# Clients must set up the following attributes of the 'club' parameter
# typically an instance of the Membership class:
#    email, letter, json_data, 

def append_email(record, club):
    entry = club.email.format(**record)
#   if 'gmail' in record['email']:
#       entry = '\n'.join([entry,
#                   content.post_scripts["gmail_warning"]])
    club.json_data.append([[record['email']],entry])

def file_letter(record, club):
    entry = club.letter.format(**record)
    path2write = os.path.join(club.dir4letters,
        "_".join((record["last"], record["first"])))
#   print("lpr['indent'] is set to {}"
#       .format(club.lpr['indent']))
    with open(path2write, 'w') as file_obj:
        file_obj.write(helpers.indent(entry,
        club.lpr["indent"]))

def q_mailing(record, club):
    """
    Checks on desired type of mailing and
    deals with mailing as appropriate.
    """
    record["subject"] = club.which["subject"]
    if record['status'] and 'be' in record['status']:
        file_letter(record, club)
    elif club.which["e_and_or_p"] == "both":
        append_email(record, club)
        file_letter(record, club)
    elif club.which["e_and_or_p"] == 'one_only':
        if record['email']:
            append_email(record, club)
        else:
            file_letter(record, club)
    elif club.which["e_and_or_p"] == 'usps':
            club.file_letter(record, club)
    else:
        print("Problem in q_mailing re {}"
            .format("{last}, {first}".format(**record)))
        assert False

def prepare_mailing(mem_csv_file, club):
    """
    Only client of this method is the prepare_mailing_cmd
    which must assign a number of instance attributes:
        club.which: one of the content.content_types which
            in turn provides values for the following keys:
                subject
                email_header
                body of letter
                func to be used on each record
                test a boolean lambda- consider record or not
                e_and_or_p: both, usps or one_only
        club.date (passed on to record.date)
        club.json_file_name
        club.json_data = []
        club.dir4letters
    """
#   print(
#       "Begin member.prepare_mailing which calls traverse_records.")
    traverse_records(mem_csv_file, 
        club.which["funcs"], club)
#   print("Still within 'prepare_mailing':")
#   print("    checking if there are emails...")
    # No point in creating a json file if no content:
    if club.json_data:
        print("There is email to send.")
        with open(club.json_file_name, 'w') as file_obj:
            file_obj.write(json.dumps(club.json_data))
    else:
        print("There are no emails to send.")

def std_mailing(self, record, club):
    """
    For mailings which require no special processing.
    Mailing is sent if the "test" lambda => True.
    Otherwise the record is ignored.
    """
    if club.which["test"](record):
        record["subject"] = club.which["subject"]
        q_mailing(record, club)

## Following are special functions that need to be in the
## <func_dict> : they provide necessary attributes to their
## 'record' parameter in order to add custom content (to a
## letter.

def set_owing(record, club):
    """
    Sets up record["extra"] for dues and fees notice,
    Client has option of setting club.owing_only => True
    in which case those with zero or negative balances
    are ignored; othewise, these are acknowledged
    (so every one gets a message.)
    Applies only to records that pass the "test" function.
    """
    if not club.which["test"](record):
#       print( "{first} {last} fails 'test' function/lambda."
#           .format(**record))
        return
    money = 0
    total = 0
    extra = []
    for key in money_keys:
        if record[key] and 'w' in record[key]:
            extra.append("{}.: waived."
            .format(money_headers[key]))
            continue
        if not record[key]:
            continue
        try:
            money = int(record[key])
#           except TypeError:
#               print("TypeError re '{}'.".format(record[key]))
#               continue
        except ValueError:
            print("ValueError re '{}'.".format(record[key]))
            continue
        if money:
            extra.append("{}.: ${}"
                .format(money_headers[key], money))
            total += money
    try:
        owing_only = club.owing_only
    except AttributeError:
        owing_only = False
    if total <= 0 and owing_only:
        return  # no notice sent
    if total <= 0:
        extra.append("Total is 0 or a credit."
            .format(total))
    extra = ["\n"] + extra
    extra.append("{}.: ${}"
        .format(money_headers["total"], total))
    if total < 0:
        extra.extend(
        ["Thank you for your advance payment.",
         "Your balance is a credit so there is nothing due."])
    if total == 0:
        extra.append("You are all paid up! Thank you.")
    record["extra"] = '\n'.join(extra)
    q_mailing(record, club)

def set_inductee_dues(record, club=None):
    """
    Provides processing regarding what fee to charge
    and sets record["current_dues"].
    """
    if month in (1, 2, 3, 4):
        record["current_dues"] = 50
    else:
        record["current_dues"] = 100


def request_inductee_payment(record, club):
    """
    Contingent on the club.which["test"] lambda:
    (If the record's status field contains 'i' for 'inducted'.)
    Sets up record["current_dues"] (by calling set_inductee_dues)
    and record["subject"]  ?? should this be elsewhere??
    """
    if club.which["test"](record):
        set_inductee_dues(record)
        record["subject"] = club.which["subject"]
        q_mailing(record)

func_dict = {
    """
    After refactoring, don't think this is necessary.
    """
#       "some_func": some_func,
    "std_mailing": std_mailing,
    "set_owing": set_owing,
    "request_inductee_payment": request_inductee_payment,
    }

def send_attachment(record, club):
    """
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
        mutt_send(email,
            args["--subject"],
            body,
            args["-a"],
            )

def test_func(record, club=None):
    """
    Can be used as a prototype or can be used for testing.
    Populates record["extra"]
    """
    pass

if __name__ == "__main__":
    print("member.py compiles OK.")
