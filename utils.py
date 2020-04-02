#!/usr/bin/env python3

# File: utils.py

# After any changes to the docstring, 
# the following contstants may need to be changed:
#     TOP_QUOTE_LINE_NUMBER     } These facilitate preparing
#     BLANK_LINE_ABOVE_USAGE    } a response to the
#     BLANK_LINE_ABOVE_OPTIONS  } 'utils.py ?' command.

"""
"utils.py" is an utility providing functionality for usage and
maintanance of the Bolinas Rod and Boat Club membership records.
Most commands deal with a csv file named "./Data/memlist.csv" so for
these it is the default input file.
Labels and Envelopes (along with the '-p <params>' option) have
been deprecated but the code left in place incase anyone ever
wishes to revive them.  Current usage replaces them with emails and
letters (which can be prepared using the 'prepare_mailing' command.)
Consult the README file for further info.

Usage:
  ./utils.py [ ? | --help | --version]
  ./utils.py ck_data [-O -r -P -s -i <infile> -N <app_spot> -X <fees_spot> -C <contacts_spot> -o <outfile>]
  ./utils.py show [-O -r -i <infile> -o <outfile> ]
  ./utils.py report [-O -i <infile> -N <applicant_spot> -o <outfile> ]
  ./utils.py stati [-O -A -i <infile> -o <outfile>]
  ./utils.py usps [-O -i <infile> -o <outfile>]
  ./utils.py extra_charges [-O -r -f <format> -i <infile> -o <outfile> -j <jsonfile>]
  ./utils.py payables [-O -i <infile>] -o <outfile>
  ./utils.py show_mailing_categories [-O -o <outfile>]
  ./utils.py prepare_mailing --which <letter> [-O -E --oo --lpr <printer> -i <infile> -j <json_file> --dir <dir4letters> ATTACHMENTS...]
  ./utils.py display_emails -j <json_file> [-O -E -o <txt_file>]
  ./utils.py send_emails [-O <content> -E] -j <json_file>
  ./utils.py print_letters --dir <dir4letters> [-O -s <sep> -e error_file]
  ./utils.py emailing [-O -i <infile> -F <muttrc>] --subject <subject> -c <content> [ATTACHMENTS...]
  ./utils.py restore_fees [-O <membership_file> -j <json_fees_file> -t <temp_membership_file> -e <error_file>]
  ./utils.py fees_intake [-O -i <infile> -o <outfile> -e <error_file>]
  ./utils.py (labels | envelopes) [-O -i <infile> -p <params> -o <outfile> -x <file>]

Options:
  -h --help  Print this docstring.
  --version  Print version.
  -A  re 'stati' comand: show only applicants.
  -c <content>  The name of a file containing the body of an email.
  -C <contacts_spot>  Contacts data file.
  --dir <dir4letters>  The directory to be created and/or read
                      containing letters for batch printing.
  -e <error_file>  Specify name of a file to which an error report
                    can be written.  If not specified, errors are
                    generally reported to stdout.
  -E   Use easydns.com as mail transfer agent. gmail is the default.
  -f <format>  Format to be used for output of the extra_charges
        command; possibilities are:
            'table' listing of names /w fees tabulated (=> 2 columns.)
            'listing' same format as Data/extra_fees.txt
            'listings' side by side lists (best use landscape mode.)
        [default: table]
  -F <muttrc>  The name of a muttrc file to be used.
                        [default: muttrc_rbc]
  -i <infile>  Specify file used as input. Usually defaults to
                the MEMBERSHIP_SPoT attribute of the Club class.
  -j <json>  Specify a json formated file (whether for input or output
              depends on context.)
  --lpr <printer>  The postal_header must be specific to the printer
            used. This provides a method of specifying which to use
            if content.which.["postal_header"] isn't already
            specified.  [default: X6505]
  -N <app_spot>  Applicant data file.
  -O  Show arguments/Options.
  -o <outfile>  Specify destination. Choices are stdout, printer, or
                the name of a file. [default: stdout]
  --oo   Owing_Only: Only send notices if fees are outstanding.
  -p <params>  If not specified, the default is
              A5160 for labels & E000 for envelopes.
  -P    Some commands may have more than one component to
        their output.  This ('-P') option makes each component appear
        on a separate page. (i.e. Separated by form feeds.)
  -r    ...for 'raw': Supress headers (to make the output suitable as
        input for creating tables.)
  -s    Report status
  --subject <subject>  The subject line of an email.
  -t <temp_file>  An option provided for when one does not want to risk
                  corruption of an important input file which is to be
                  modified, thus providing an opportunity for proof
                  reading the 'modified' file before renaming it to
                  the original. (Typically named '2proof_read.txt'.)
  --which <letter>  Specifies type/subject of mailing.
  -X <fees_spot>  Extra Fees data file. 

Commands:
    When run without a command, suggests ways of getting help.
    ck_data: Checks all the club's data bases for consistency.
        Assumes (user must assertain) a fresh export of the
        contacts list.  If the -j option is specified, it names the
        file to which to send emails (in JSON format) to members with
        differing emails. (After proof reading, use 'send_emails'.)
    show: Returns membership demographics. A copy is sent to the web
        master for display on the web site.
    report: Prepares a 'Membership Report".
    stati: Returns a listing of stati.  Applicants plus ..
        Depends on acurate entries in 'status' field.
    usps: Creates a csv file containing names and addresses of
        members without an email address who therefore receive their
        Club minutes by post. Includes the secretary.
    extra_charges: Reports on members paying extra charges (for
        kayak storage, mooring &/or dock usage.)
        Output format can be specified by the -f <format> option.
        If the <infile> name ends in '.csv' then the/membership main
        data base file is assumed and output will be charges
        outstanding (i.e. owed but still not payed.) If it ends in
        '.txt' then it is assumed to be in the format of the
        "extra_feess.txt" file and output will include all who are
        paying for one or more of the Club's three special privileges.
        There is also the option of creating a json file needed by
        the restore_fees_cmd. (See the README file re SPoL.)
    payables: reports on content of the member data money fields
        providing a listing of those who owe and those who have paid
        in advance.
    show_mailing_categories: Sends a list of possible entries for the
        '--which' parameter required by the prepare_mailings command.
        See the 'content_types' dict in content.py.)
    prepare_mailing: A general form of the billing command (above.)
        This command demands a <--which> argument to specify the
        mailing: more specifically, it specifies the content and the
        custom function(s) to be used.  Try the
        'show_mailing_categories' command for a list of choices.
        Other parameters have defaults set:
        '-E'  use easydns.com as mta (vs gmail account.)
        'ATTACHMENTS...'  Applies only when -E is set to specify
        using easydns.  Must be a list of file names.
        '--oo'  Only send request for fee payment to those with an
        outstanding balance.
        '--lpr <printer>' specifies printer to be used for letters.
        '-i <infile>' membership data csv file.
        '-j <json_file>' where to dump prepared emails.
        '---dir <dir4letters>' where to put letters.
    prepare4easy: A version of the prepare_mailing command (above)
        modified to produce a json file that can be used to send
        emails via easydns.com rather than the club gmail account.
    display_emails: Provides an opportunity to proof read the emails.
    send_emails: If <content> is NOT provided, the JSON file is expected
        to consist of an iterable of iterables: the first item of each
        second level iterable consists of an iterable of one or more
        recipient(s) and and the second item is the email message to
        be sent to the recipients.  If <content> is provided, the
        content of the so specified file will form the body of the
        email and the JSON file must again be an iterable of iterables
        but in this case the lower level iterable is simply an
        iterable of recipients (email addresses) to which the content
        is to be send.  Note: the content of each email regardless of
        how it is provided, must be in proper format with "From:",
        "To:" & "Subject:" lines (no leading spaces!) followed by a
        blank line and then the body of the email. The "From:" line
        should read as follows: "From: rodandboatclub@gmail.com"
        Note: Must first lower br&bc's account security at:
        https://myaccount.google.com/lesssecureapps
    print_letters: Sends the files contained in the directory
        specified by the --dir parameter.  Depricated in favour of
        simply using the lpr utility: $ lpr ./Data/MailDir/*
    restore_fees: Use this command after all dues and fees have been
        paid- will abort if any are outstanding. Will place the
        results into a file named as a concatination of "new_" and the
        specified membership csv file. One can then mannually check
        the new file and move it if all is well.
    emailing: provides ability to send emails with attachments.
        Uses a different mechanism than the prepare_mailing and
        send_emails commands. Sends the same to all in the input file.
    fees_intake: Input file should be a 'receipts' file (which has a
        specific format,) output yields subtotals and the grand total.
        This simply automates totaling the numbers.
    labels: print labels.       | default: -p A5160  | Both
    envelopes: print envelopes. | default: -p E000   | redacted.
"""

import os
import shutil
import csv
import codecs
import sys
import time
import random
import json
import subprocess
from docopt import docopt
import member
import helpers
import content
import data
import Pymail.send
from rbc import Club

# Constants required for correct rendering of "?" command:
TOP_QUOTE_LINE_NUMBER = 11      #} These facilitate preparing
BLANK_LINE_ABOVE_USAGE = 21     #} response to the
BLANK_LINE_ABOVE_OPTIONS = 40   #} 'utils.py ?' command.

MSMTP_ACCOUNT = "gmail"
MIN_TIME_TO_SLEEP = 1   #} Seconds between
MAX_TIME_TO_SLEEP = 5   #} email postings.


TEXT = ".txt"  #} Used by <extra_charges_cmd>
CSV = ".csv"   #} command.

TEMP_FILE = "2print.temp"  # see <output> function
DEFAULT_ADDENDUM2REPORT_FILE = "Info/addendum2report.txt"

args = docopt(__doc__, version="1.1")
if args['-O']:
    print("Arguments are...")
    res = sorted(["{}: {}".format(key, args[key]) for key in args])
    ret = helpers.tabulate(res, max_width=140, separator='   ')
    print('\n'.join(ret))
    print("...end of arguments.")

lpr = args["--lpr"]
if lpr and lpr not in content.printers.keys():
    print("Invalid '--lpr' parameter! '{}'".
        format(lpr))
    sys.exit()

def output(data, destination=args["-o"]):
    """
    Sends data (text) to destination as specified
    by the -o <outfile> command line parameter (which
    defaults to stdout.)
    Reports file manipulations to stdout.
    """
    if destination == 'stdout':
        print(data)
    elif destination == 'printer':
        with open(TEMP_FILE, "w") as fileobj:
            fileobj.write(data)
            print('Data written to temp file "{}".'
                .format(fileobj.name))
            subprocess.run(["lpr", TEMP_FILE])
            subprocess.run(["rm", TEMP_FILE])
            print('Temp file "{}" deleted after printing.'
                .format(fileobj.name))
    else:
        with open(destination, "w") as fileobj:
            fileobj.write(data)
            print('Data written to "{}".'.format(fileobj.name))

# Medium specific classes:
# e.g. labels, envelopes, ...
# These classes, one for each medium, need never be instantiated.
# They are used only to maintain a set of constants and
# are named beginning with a letter (A - Avery, E - Envelope, ...)
# followed by a 4 digit number: A5160, E0000, ... .
# Clients typically refer to these as <params>.

class Dummy(object):
    """ REDACTED
    a Dummy class for use when templates are not required"""
    formatter = ""
    @classmethod
    def self_check(cls):  # No need for the sanity check in this case
        pass

class E0000(object):
    """
    REDACTED.
    Custom envelopes used by the Bolinas Rod & Boat Club
    to send out requests for dues.
    """
    n_chars_wide = 60
    n_lines_long = 45
    n_labels_page = 1
    n_lines_per_label = 10

    n_chars_per_field = 25
    separation = (34, )
    top_margin = 32

    left_formatter = (" " * separation[0] + "{{:<{}}}"
        .format(n_chars_per_field))
    right_formatter = (" " * separation[0] + "{{:>{}}}"
        .format(n_chars_per_field))
    empty_line = ""

    @classmethod
    def self_check(cls):
        """
        No need for the sanity check in this case.
        """
        pass


class A5160(object):
    """
    Avery 5160 labels  3 x 10 grid
    zero based:
        1, 28, 56
        3, 9, 15, 21, 27, 33, 39, 45, 51, 57
        (max content 5 lines of 25 characters each)
    Uses "letter size" blanks.
    BUT: there was a complication- my printer "wraps" at 80 chars.
    So each line could not exceed 80 characters.
    """

    # The first two are restrictions imposed by my printer!
    n_chars_wide = 80  # The Avery labels are wider ?84 I think?
    n_lines_long = 64

    n_labels_per_page = 30
    n_labels_per_row = 3
    n_rows_per_page = n_labels_per_page // n_labels_per_row
    n_lines_per_label = 6   # Limits 'spill over' of long lines.

    # Because of the n_chars_wide restriction, can't use the full
    # width of the labels :
    n_chars_per_field = 23
    #             /------left_margin (spaces before 1st field in row)
    #             |  /----between 1st and 2nd 
    #             |  |  /--between 2nd & 3rd
    #             |  |  |   # These numbers refer to the room to be
    #             v  v  v   # left before and between the labels.
    separation = (2, 4, 5)
    line_length_needed = 0
    for n in separation:
        line_length_needed += n
    line_length_needed += n_labels_per_row * n_chars_per_field

    top_margin = 2  # The number of blank lines at top of each page.

    empty_label = [""] * n_lines_per_label

    left_formatter = ("{{:<{}}}"
        .format(n_chars_per_field))
    right_formatter = ("{{:>{}}}"
        .format(n_chars_per_field))
    empty_line = left_formatter.format(" ")

    def __init__(self):
        pass

    @classmethod
    def self_check(cls):
        """
        Provides a 'sanity check'.
        """
        if cls.line_length_needed > cls.n_chars_wide:
            print("Label designations are incompatable!")
            sys.exit()

media = dict(  # keep the classes in a dict
        e000= E0000,
        a5160= A5160,
        )


def ck_data_cmd():
    print("Checking for data consistency...")
    club = Club()
    if args['-i']:
        club.MEMBERSHIP_SPoT = args['-i']
    if args['-N']:
        club.APPLICANT_SPoT = args['-N']
    if args['-X']:
        club.EXTRA_FEES_SPoT = args['-X']
    if args['-C']:
        club.CONTACTS_SPoT = args['-C']
    ret = data.ck_data(club,
                    report_status=args['-s'],
                    raw=args['-r'],
                    formfeed=args['-P'])
    output("\n".join(ret))


def show_cmd():
    club = Club()
    club.pattern = ("{first} {last}  [{phone}]  {address}, " +
                    "{town}, {state} {postal_code} [{email}]")
    club.members = []
    club.nmembers = 0
    club.napplicants = 0
    club.errors = []
    club.by_n_meetings = {}
    infile = args["-i"]
    if not infile:
        infile = club.infile
    print("Preparing membership listings...")
    err_code = member.traverse_records(infile,
        (member.add2list4web), club)

    ret = ["""FOR MEMBER USE ONLY

THE TELEPHONE NUMBERS, ADDRESSES AND EMAIL ADDRESSES OF THE BOLINAS
ROD & BOAT CLUB MEMBERSHIP CONTAINED HEREIN IS NOT TO BE REPRODUCED
OR DISTRIBUTED FOR ANY PURPOSE WITHOUT THE EXPRESS PERMISSION OF THE
BOARD OF THE BRBC.
    """]
    if club.members:
        ret.extend(("Club Members ({} in number as of {})"
                .format(club.nmembers, helpers.date),
                            "============"))
        ret.extend(club.members)
    if club.by_n_meetings:
        ret.append('')
        header = "Applicants ({} in number)".format(club.napplicants)
        ret.append(header)
        ret.append('=' * len(header))
        ret.extend(member.show_by_status(club.by_n_meetings))

    output("\n".join(ret))
    print("...results sent to {}.".format(args['-o']))



def stati():
    """
    Returns a list of strings (that can be '\n'.join(ed))
    """
    club = Club()
    infile = args["-i"]
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    print("Preparing listing of stati.")
    club.by_status = {}
    err_code = member.traverse_records(infile,
                                    member.add2status_data,
                                    club)
    if not club.by_status:
        return ["Found No Entries with 'Status' Content." ]

#   keys = [k for k in club.by_status.keys() if k]
    keys = [k for k in club.by_status.keys()]
    keys.sort()

    ret = []
#   if not args['-A']:
#       header = (
#           "Applicants (and other's with special status)")
#       ret.append(header)
#       ret.append('=' * len(header))
#       ret.append('')
    header = "Applicants"
    ret.append(header)
    ret.append('=' * len(header))
#   ret.append('')
    for key in keys:
        sub_header = member.status_key_values[key]
        values = sorted(club.by_status[key])
        if key.startswith('a'):
            ret.append('')
            ret.append(sub_header)
            ret.append('-' * len(sub_header))
        elif not args['-A']:
            ret.append('')
            ret.append(sub_header)
            ret.append('=' * len(sub_header))
        for value in values:
            ret.append("    {}".format(value))
    return ret


def report():
    """
    Prepare a "Membership Report"
    Automatically Dateed, repors:
    Number of members & Number of applicants and provides an
    applicant role call (/w dates of meetings attended.)
    """
    club = Club()
    club.by_status = {}
    club.nmembers = 0
    infile = args["-i"]
    applicant_spot = args['-N']
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    if not applicant_spot:
        applicant_spot = Club.APPLICANT_SPoT
    print("Preparing Membership Report ...")
    report = [
       "Membership Report (prepared {})".format(helpers.date), ]
    report.append('=' * len(report[0]))
    report.append('')

    err_code = member.traverse_records(infile,
            [member.add2status_data,
            member.increment_nmembers,
            ],
            club)
    ap_set_w_dates_by_status = (
        data.gather_applicant_data(
                applicant_spot, include_dates=True)["applicants"])
    
    report.append('Club membership currently stands at {}.'
                    .format(club.nmembers))

    ap_listing = club.by_status # } This segment is for
    for key in ap_listing:      # } error checking only;
      if 'a' in key:            # } not required if data match.
        # Only deal with applicants.
        if len(ap_listing[key]) != len(ap_set_w_dates_by_status[key]):
            print("!!! {} != {} !!!"
              .format(ap_listing[key], ap_set_w_dates_by_status[key]))

    if ap_set_w_dates_by_status:
        report.extend(["\nApplicants",
                         "=========="])
        report.extend(helpers.show_dict(ap_set_w_dates_by_status,
                                underline_char='-'))
    if 'r' in club.by_status:
        header = (
            'Members ({} in number) retiring from the Club:'
                .format(len(club.by_status['r'])))
        report.append('')
        report.append(header)
        report.append("=" * len(header))
        for name in club.by_status['r']:
            report.append(name)

    try:
        with open(DEFAULT_ADDENDUM2REPORT_FILE, 'r') as fobj:
            print('opening file')
            addendum = fobj.read()
            report.append(addendum)
    except FileNotFoundError:
        print('report.addendum not found')
        pass
    report.extend(['','',
        "Respectfully submitted by...\n\n",
        "Alex Kleider, Membership Chair,",
        "for presentation to the Executive Committee",
        "at the time of their next meeting to be held",
         "{}.".format(helpers.next_first_friday()),
        ])
    return report
 
def report_cmd():
    print("Test 'member' recognition: {}"
        .format(member.status_key_values['r']))
    output('\n'.join(report()))

def stati_cmd():
    output('\n'.join(stati()))


def usps_cmd():
    """
    Generates a cvs file used by the Secretary to send out minutes.
        first,last,address,town,state,postal_code
    (Members who are NOT in the 'email only' category.)
    """
    infile = args['-i']
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    club = Club()
    club.usps_only = []
    err_code = member.traverse_records(infile, 
                [member.get_usps, member.get_secretary],
                club)
    header = []
    for key in club.fieldnames:
        header.append(key)
        if key == "postal_code":
            break
    res = [",".join(header)]
    res.extend(club.usps_only)
    # The following 2 lines are commented out because new secretary
    # Michael Rafferty doesn't need/want to be on the list.
#   if hasattr(club, 'secretary'):
#       res.append(club.secretary)
    return '\n'.join(res)
        

def extra_charges_cmd():
    """
    Returns a report of members with extra charges.

    It also can create a json file: specified by the -j option.
    Such a json file is required by the restore_fees command.
    """
    infile = args["-i"]
    if not infile:
        infile = Club.EXTRA_FEES_SPoT
    print('<infile> set to "{}"'.format(infile))
    if infile.endswith(TEXT):
        print('<infile> ends in "{}"'.format(TEXT))
        extra_fees = data.gather_extra_fees_data(infile)
        by_name = extra_fees[Club.by_name]
        by_category = extra_fees[Club.by_category]
        if args['-f'] == 'listing':
            with open(infile, 'r') as f_object:
                output(f_object(read))
        elif args['-f'] == 'table':
            res = data.present_fees_by_name(by_name, raw=args['-r'])
            ret = helpers.tabulate(res, alignment='<', down=True)
            output('\n'.join(ret))
        elif args['-f'] == 'listings':
            output('\n'.join(data.show_fee_listings(extra_fees,
                                                        args['-r'])))
    elif infile.endswith(CSV):
        print('Not set up to deal with csv file yet.')
        return
    else:
        print('<infile> must end in ".txt" or ".csv"')
        assert(False)
    if args["-j"]:
        print('Not set up to provide json file yet.')


def payables_cmd():
    """
    Traverses the db populating 
    """
    infile = args['-i']
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    club = Club()
    club.still_owing = []
    club.advance_payments = []
    output = []
    err_code = member.traverse_records(infile,
                member.get_payables, club)
    if club.still_owing:
        output.extend(["Members owing",
                       "-------------"])
        output.extend(club.still_owing)
    if club.advance_payments:
        output.append("\n")
        output.extend(["Members Payed in Advance",
                       "------------------------"])
        output.extend(club.advance_payments)
    return '\n'.join(output)

def show_mailing_categories_cmd():
    ret = ["Possible choices for the '--which' option are: ", ]
    ret.extend((("\t" + key) for key in content.content_types.keys()))
    output('\n'.join(ret))


def prepare_mailing_cmd():
    """
    '-E' changes the MTA to be easydns.com rather than gmail.
    Does initial set up of a Club instance then
    calls member.prepare_mailing(
    '--oo' Owing Only: applies only to requests for payment:
    if set, those with zero (or negative) balance do not get
    a message.
    """
    club = Club()
    if args['-E']:
        club.easy = True
    else:
        club.easy = False
    if args['--oo']:
        club.owing_only = True
    else:
        club.owing_only = False
    club.which = content.content_types[args["--which"]]
    club.lpr = content.printers[args["--lpr"]]
    club.email = content.prepare_email_template(
                    club.which, args['-E'])
    club.letter = content.letter_format(club.which, 
                                        args["--lpr"])
#   print("Preparing mailing: '{}'".format(club.which))
    if not args["-i"]:
        args["-i"] = club.MEMBERSHIP_SPoT
    club.input_file_name = args['-i']
    if not args["-j"]:
        args["-j"] = club.JSON_FILE_NAME4EMAILS
    club.json_file_name = args["-j"]
    if not args["--dir"]:
        args["--dir"] = club.MAILING_DIR
    club.dir4letters = args["--dir"]
    club.attachment = args['ATTACHMENTS']
    # *****...
    if club.which["e_and_or_p"] in ("both", "usps", "one_only"):
        print("Checking for directory '{}'."
            .format(args["--dir"]))
        club.check_dir4letters(club.dir4letters)
    if club.which["e_and_or_p"] in ("both", "email", "one_only"):
        print("Checking for file '{}'."
            .format(args["-j"]))
        club.json_file_name = args["-j"]
        club.check_json_file(club.json_file_name)
        club.json_data = []
    # *****...
    member.prepare_mailing(club)
    # need to move the json_data to the file
#   if club.json_data:
#       with open(club.json_file_name, 'w') as f_obj:
#           json.dump(club.json_data, f_obj)
#           print('JSON dumped to "{}".'.format(f_obj.name))
    print("""prepare_mailing completed..
    ..nest step might be the following:
    $ zip zip -r 4Michael.zip {}"""
        .format(args["--dir"]))


def display_emails_cmd(json_file):
    with open(json_file, 'r') as f_obj:
        print('Reading JSON file "{}".'.format(f_obj.name))
        records = json.load(f_obj)
    all_emails = []
    n_emails = 0
    print("...initializing 'all_emails' to empty list")
    for record in records:
        email = []
        if args['-E']:
            for field in record:
                email.append("{}: {}".format(field, record[field]))
            email.append('')
            all_emails.extend(email)
            n_emails += 1
        else:
            try:
                recipients = ', '.join(record[0])
            except KeyError:
                print("Perhaps you've forgotten the '-E' option?")
                sys.exit()
            email.append(">>: " + recipients)
            email.append(record[1])
#           print(record[1])
#           for mail in email: print(mail)
            email.append('')
            all_emails.extend(email)
            n_emails += 1
    print("Processed {} emails..."
        .format(len(n_emails)))
    return "\n".join(all_emails)


def send_emails_cmd():
    """
    If command line args supply a <content> parameter it is assumed
    to be the name of a file which will serve as the content of the
    email(s) to be sent. In this case, the json_file ("-i") parameter
    specifies a file that when dumped, results in an iterable of
    iterables; the lower level iterable will consist of one or more
    strings- each representing a recipient email address.
    If <content> is not specified, then the json_file is expected
    to dump into an array of tuples, each consisting of an iterable
    containing recipients as the first item and the email content
    as the second item.
    Note: Regardless of how content is provided, it must be in proper
    format with "From:", "To:" & "Subject:" lines (no leading
    spaces!), and then a blank line followed by the text of the email.
    The "From:" line should read as follows:
    "From: rodandboatclub@gmail.com"

    Note: The send_emails functionality depends on the
    presence of a ~/.msmtprc configuration file
    and (unless the -E option is selected for easydns.com rather
    than using gmail) lowering the gmail account security setting:
    https://myaccount.google.com/lesssecureapps
    """
    content = args["<content>"]
    j_file = args["-j"]
    message = None
    if content:
        with open(content, 'r') as f_obj:
            message = f_obj.read()
            print('Reading content from "{}".'
                .format(f_obj))
    with open(j_file, 'r') as f_obj:
        data = json.load(f_obj)
        print('Loading JSON from "{}"'.format(f_obj.name))
    counter = 0
    if args['-E']:
        Pymail.send.send(data)
    else:
        for datum in data:
            if message:
                recipients = datum
                content = message
            else:
                try:
                    recipients = datum[0]
                    recipients = ', '.join(record[0])
                except KeyError:
                    print("Perhaps you've forgotten the '-E' option?")
                    sys.exit()
                content = datum[1]
            counter += 1
            print("Sending email #{} to {}."
                .format(counter, ", ".join(recipients)))
            smtp_send(recipients, content)
            # Using random waits so as not to look like a 'bot'.
            time.sleep(random.randint(MIN_TIME_TO_SLEEP,
                                    MAX_TIME_TO_SLEEP))

def print_letters_cmd():
    successes = []
    failures = []
    for letter_name in os.listdir(args["--dir"]):
        path_name = os.path.join(dir4letters, letter_name)
        completed = subprocess.run(["lpr", path_name])
        if completed.returncode:
            failures.append("Problem ({}) printing '{}'."
                .format(completed.returncode, path_name))
        else:
            successes.append("{}".format(path_name))
    if successes:
        successes = ("Following letters printed successfully:\n"
            + successes)
    else:
        successes = ["No file was printed successfully."]
    if failures:
        failures = ("Following letters failed to print:\n"
            + failures)
    else:
        failures = ["All files printed successfully."]
    successes = '\n'.join(successes)
    failures = '\n'.join(failures)
    report = successes + args['-s'] + failures
    output(report)

def display_emails_cmd1(json_file, output_file=None):
    ret = []
    with open(json_file, 'r') as f_obj:
        print('Reading JSON file "{}".'.format(f_obj.name))
        data = f_obj.read()
        emails = json.loads(data)
        print("Type 'emails' is '{}'.".format(type(emails)))
    for recipients in emails:
        ret.append(recipients)
        for line in emails[recipients]:
            ret.append(line)
    out_put = "\n".join(ret)
    output(out_put)

def emailing_cmd():
    """
    Sends emails with an attachment.
    Sets up an instance of Club and traverses
    the input file calling the send_attachment method
    on each record.
    """
    club = Club()
    if not args["-i"]:
        args["-i"] = club.MEMBERSHIP_SPoT
    with open(args["-c"], "r") as content_file:
        club.content = content_file.read()
    err_code = member.traverse_records(args["-i"],
        member.send_attachment,
        club=club)

def restore_fees_cmd():
    """
    Assumes the dues paying season is over and all dues and fees
    fields have been zeroed out or contain a credit (over payment.)
    Repopulates the club's master list with the ANNUAL_DUES constant
    and information from args['<extra_fees.json>'].
    If '-t <new_membership_file>' is specified, the original
    membership file is not modified and output is to the new file,
    else the original file is changed.
    """
    ### Take into consideration the possibility of credit values. ###
    club = Club()
    if not args['<membership_file>']:
        args['<membership_file>'] = club.MEMBERSHIP_SPoT
    if not args['-j']:
        args['-j'] = club.EXTRA_FEES_JSON
    if not args['-t']:
        args['-t'] = club.TEMP_MEMBERSHIP_SPoT
    ret = club.restore_fees(
                args['<membership_file>'],
                club.YEARLY_DUES,
                args['-j'],
                args['-t']
            )
    if club.errors and args["-e"]:
        with open(args["-e"], 'w') as file_obj:
            file_obj.write(club.errors)
            print('Wrote errors to "{}".'.format(file_obj.name))
    if ret:
        sys.exit(ret)

def fees_intake_cmd():
    infile = args['-i']
    outfile = args['-o']
    errorfile = args['-e']
    club = Club()
    if infile:
        fees_taken_in = club.fees_intake(infile)
    else:
        fees_taken_in = club.fees_intake()
    fees_taken_in.append("\n")
    res = '\n'.join(fees_taken_in)
    ## REFACTOR: The following can be replaced by output(res)
    if not outfile or outfile == 'stdout':
        print(res)
    else:
        with open(outfile, 'w') as file_obj:
            print('Writing to "{}".'.format(file_obj.name))
            file_obj.write(res)
    ## End of refactoring
    if club.invalid_lines and errorfile:
        with open(errorfile, 'w') as file_obj:
            print('Writing to "{}".'.format(file_obj.name))
            file_obj.write('\n'.join(club.invalid_lines))

def labels_cmd():
    if args["--parameters"]:
        medium = media[args["--parameters"]]
    else:
        medium = A5160
    club = Club(medium)
    club = args["-i"]
    return club.get_labels2print(source_file)

def envelopes_cmd():
    if args["--parameters"]:
        medium = media[args["--parameters"]]
    else:
        medium = E0000
    club = Club(medium)
    source_file = args["-i"]
    club.print_custom_envelopes(source_file)

def smtp_send(recipients, message):
    """
    Send email, as defined in <message>,
    to the <recipients> who will receive this email
    from the Bolinas Rod and Boat Club.
    <recipients> must be an iterable of one or more email addresses.
    Note: Must first lower br&bc's account security at:
    https://myaccount.google.com/lesssecureapps
    Also Note: <message> must be in proper format with
    "From:", "To:" & "Subject:" lines (no leading spaces!) followed
    by a blank line and then the text of the email. The "From:" line
    should read as follows: "From: rodandboatclub@gmail.com"
    """
    cmd_args = ["msmtp", "-a", MSMTP_ACCOUNT, ]
    for recipient in recipients:
        cmd_args.append(recipient)
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE, 
        input=message, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))

def mutt_send(recipient, subject, body, attachments=None):
    """
    Does the mass e-mailings with attachment
    if one is provided.
    """
    cmd_args = [ "mutt", "-F", args["-F"], ]
    cmd_args.extend(["-s", "{}".format(subject)])
    if attachments:
        list2attach = ['-a']
        for path2attach in attachments:
            list2attach.append(path2attach)
        cmd_args.extend(list2attach)
    cmd_args.extend([ "--", recipient])
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE, 
        input=body, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))


if __name__ == "__main__":
#   print(args)

    if args["?"]:
        doc_lines = __doc__.split('\n') 
        print('\n'.join(doc_lines[
            (BLANK_LINE_ABOVE_USAGE - TOP_QUOTE_LINE_NUMBER)
            :
            (BLANK_LINE_ABOVE_OPTIONS - TOP_QUOTE_LINE_NUMBER + 1)
            ]))

    elif args["ck_data"]:
        ck_data_cmd()

    elif args["show"]:
        show_cmd()

    elif args["report"]:
        report_cmd()

    elif args["stati"]:
        stati_cmd()

    elif args["usps"]:
        print("Preparing a csv file listing showing members who")
        print("receive meeting minutes by mail. i.e. don't have (or")
        print("haven't provided) an email address (to the Club.)")
        output(usps_cmd())

    elif args["extra_charges"]:
        print("Selecting members with extra charges:")
#       print("...being sent to {}.".format(args['-o']))
        extra_charges_cmd()

    elif args["payables"]:
        print("Preparing listing of payables...")
        output(payables_cmd())

    elif args['show_mailing_categories']:
        show_mailing_categories_cmd()

    elif args["prepare_mailing"]:
        print("Preparing emails and letters...")
        prepare_mailing_cmd()
        print("...finished preparing emails and letters.")

    elif args['display_emails']:
        output(display_emails_cmd(args['-j']))

    elif args["send_emails"]:
        print("Sending emails...")
        send_emails_cmd()
        print("Done sending emails.")

    elif args["print_letters"]:
        print("Printing letters ...")
        print_letters_cmd()
        print("Done printing letters.")

    elif args['emailing']:
        emailing_cmd()
    
    elif args['restore_fees']:
        restore_fees_cmd()

    elif args['fees_intake']:
        fees_intake_cmd()

    elif args["labels"]:
        print("Printing labels from '{}' to '{}'"
            .format(args['-i'], args['-o']))
        output(labels_cmd())

    elif args["envelopes"]:
        # destination is specified within Club 
        # method print_custom_envelopes() which is called 
        # by print_statement_envelopes()
        print("""Printing envelopes...
    addresses sourced from '{}'
    with output sent to '{}'"""
            .format(args['-i'], args['-o']))
        envelopes_cmd()

    else:
        print("You've failed to select a command.")
        print("Try ./utils.py ? # brief!  or")
        print("    ./utils.py -h # for more detail")

NOTE = """
emailing_cmd()
    uses Club.traverse_records(infile,
        club.send_attachment(args["-i"]))
"""        
