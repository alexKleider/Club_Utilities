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
  ./utils.py ck_data [-O -d -P -r -s -i <infile> -N <app_spot> -X <fees_spot> -C <contacts_spot> -o <outfile>]
  ./utils.py show [-O -i <infile> -o <outfile> ]
  ./utils.py report [-O -i <infile> -N <applicant_spot> -o <outfile> ]
  ./utils.py stati [-O -A -i <infile> -o <outfile>]
  ./utils.py zeros [-O -i <infile> -o <outfile]
  ./utils.py usps [-O -i <infile> -o <outfile>]
  ./utils.py extra_charges [-O -r -w <width> -f <format> -i <infile> -o <outfile> -j <jsonfile>]
  ./utils.py payables [-O -T -w <width> -i <infile>] -o <outfile>
  ./utils.py show_mailing_categories [-O -o <outfile>]
  ./utils.py prepare_mailing --which <letter> [-O -E --oo --lpr <printer> -i <infile> -j <json_file> --dir <dir4letters> ATTACHMENTS...]
  ./utils.py display_emails -j <json_file> [-O -E -o <txt_file>]
  ./utils.py send_emails [-O -E] -j <json_file>
  ./utils.py print_letters --dir <dir4letters> [-O -S <separator> -e error_file]
  ./utils.py emailing [-O -i <infile> -F <muttrc>] --subject <subject> -c <content> [ATTACHMENTS...]
  ./utils.py restore_fees [-O -i <membership_file> -j <json_fees_file> -t <temp_membership_file> -e <error_file>]
  ./utils.py fee_intake_totals [-O -i <infile> -o <outfile> -e <error_file>]
  ./utils.py (labels | envelopes) [-O -i <infile> -p <params> -o <outfile> -x <file>]

Options:
  -h --help  Print this docstring.
  --version  Print version.
  -A  re 'stati' comand: show only applicants.
  -c <content>  The name of a file containing the body of an email.
  -C <contacts_spot>  Contacts data file.
  -d   Include details: fee inconsistency for ck_data.
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
  -O  Show Options/commands/arguments.  Used for debuging.
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
  -s    Report status in ck_data command.
  -S <separator>   ?? not sure that this is used.
  --subject <subject>  The subject line of an email.
  -t <temp_file>  An option provided for when one does not want to
        risk corruption of an important input file which is to be
        modified, thus providing an opportunity for proof reading
        the 'modified' file before renaming it to the original.
        (Typically named '2proof_read.txt'.)
  -T  Present data in columns rather than a long list.
  -w <width>  Maximum number of characters per line in output.
                                    [default: 95]
  --which <letter>  Specifies type/subject of mailing.
  -x <file>  Used by commands not in use. (Expect redaction)
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
    prepare_mailing:  Demands a <--which> argument to specify the
        content and the custom function(s) to be used.  Try the
        'show_mailing_categories' command for a list of choices.
        Other parameters have defaults set:
        '-E'  use easydns.com as mta (vs the default gmail account.)
        The format of the <json_file> content differs depending on
        whether using gmail or easydns.com.
        'ATTACHMENTS...'  Must be a list of file names.  Applies
        only when -E is set to specify using easydns since gmail
        doesn't support this functionality (to my knowledge.)
        '--oo'  Send request for fee payment only to those with an
        outstanding balance.  This is relevant only to letters
        relating to dues and fees.
        '--lpr <printer>' specifies printer to be used for letters.
        '-i <infile>' membership data csv file.
        '-j <json_file>' where to dump prepared emails.
        '---dir <dir4letters>' where to put letters.
    display_emails: Provides an opportunity to proof read the emails.
        If the -E option was used to prepare the emails, it must
        also be provided to this command.
    send_emails: Sends out the emails found in the -j <json_file>.
        If the latter is prepared using the -E option, this option
        must also be provided to this command since the json formats
        are different.
        If not using -E, then gmail is used and account security
        must first be lowered:
        https://myaccount.google.com/lesssecureapps
        Also the content of each email must be in proper format
        (as provided by the prepare_mailing_command)
        with "From:", "To:" & "Subject:" lines (no leading spaces!)
        followed by a blank line and then the body of the email.
        The "From:" line should read as follows:
        "From: rodandboatclub@gmail.com"
    print_letters: Sends the files contained in the directory
        specified by the --dir parameter.  Depricated in favour of
        simply using the lpr utility: $ lpr ./Data/MailDir/*
    restore_fees: Use this command after all dues and fees have been
        paid- will abort if any are outstanding. Will place the
        results into a file named as a concatination of "new_" and the
        specified membership csv file. One can then mannually check
        the new file and move it if all is well.
        NOTE: check out 'rewrite_db.py'.
    emailing: provides ability to send emails with attachments.
        Uses a different mechanism than the prepare_mailing and
        send_emails commands. Sends the same to all in the input file.
    fee_intake_totals: Input file should be a 'receipts' file with a
        specific format. It defaults to 'Data/receipts-YYYY.txt'.
        Output yields subtotals and the grand total.
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
BLANK_LINE_ABOVE_OPTIONS = 41   #} 'utils.py ?' command.

MSMTP_ACCOUNT = "gmail"
MIN_TIME_TO_SLEEP = 1   #} Seconds between
MAX_TIME_TO_SLEEP = 5   #} email postings.


TEXT = ".txt"  #} Used by <extra_charges_cmd>
CSV = ".csv"   #} command.

TEMP_FILE = "2print.temp"  # see <output> function
DEFAULT_ADDENDUM2REPORT_FILE = "Info/addendum2report.txt"

args = docopt(__doc__, version="1.1")
if args['-w'][0] == '=':
    args['-w'] = args['-w'][1:]
try:
    max_width = int(args['-w'])
except ValueError:
    print(
"Value of '-w' command line argument must be an integer.")
    sys.exit()
if args['-O']:
    print("Arguments are...")
    res = sorted(["{}: {}".format(key, args[key]) for key in args])
    ret = helpers.tabulate(res, max_width=max_width, separator='   ')
    print('\n'.join(ret))
    print("...end of arguments.")

lpr = args["--lpr"]
if lpr and lpr not in content.printers.keys():
    print("Invalid '--lpr' parameter! '{}'".
        format(lpr))
    sys.exit()


def confirm_file_present(file_name):
    """
    Aborts the program if file_name doesn't exist.
    """
    if not os.path.exists(file_name):
        print("File '{}' expected but not found."
                    .format(file_name))
        sys.exit()


def confirm_file_up_to_date(file_name):
    """
    Asks user to confirm that the file is current.
    Used for the gmail contacts.csv file.
    """
    response = input("Is file '{}' current? "
                .format(file_name))
    if response and response[0] in "Yy":
        return True
    else:
        print("Update the file before rerunning utility.")
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
    confirm_file_present(club.CONTACTS_SPoT)
    confirm_file_up_to_date(club.CONTACTS_SPoT)
    ret = data.ck_data(club,
                    report_status=args['-s'],
                    fee_details=args['-d'],
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
        header = "Applicants ({} in number)".format(club.napplicants)
        helpers.add_header2list(header, ret, underline_char='=')
        ret.extend(member.show_by_status(club.by_n_meetings))
    output("\n".join(ret))
    print("...results sent to {}.".format(args['-o']))



def report():
    """
    Prepare a "Membership Report"
    Automatically Dateed, reports:
    Number of members & Number of applicants and provides an
    applicant role call (/w dates of meetings attended.)
    Checks both the applicant SPoT and the main data base.
    """
    club = Club()
    club.ms_by_status = {}
    club.nmembers = 0
    infile = args["-i"]
    applicant_spot = args['-N']
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    if not applicant_spot:
        applicant_spot = Club.APPLICANT_SPoT
    print("Preparing Membership Report ...")

    err_code = member.traverse_records(infile,
            [member.add2status_data,
            member.increment_nmembers,
            ], club)
    ap_set_w_dates_by_status = (
        data.gather_applicant_data(
                applicant_spot, include_dates=True)["applicants"])

    ap_listing = club.ms_by_status # } This segment is for
    for key in ap_listing:      # } error checking only;
      if 'a' in key:            # } not required if data match.
        # Only deal with applicants.
        if len(ap_listing[key]) != len(ap_set_w_dates_by_status[key]):
            print("!!! {} != {} !!!"
              .format(ap_listing[key], ap_set_w_dates_by_status[key]))

    report = []
    helpers.add_header2list("Membership Report (prepared {})"
                                    .format(helpers.date),
                    report, underline_char='=')
    report.append('')
    report.append('Club membership currently stands at {}.'
                    .format(club.nmembers))

    if ap_set_w_dates_by_status:
        report.extend(["\nApplicants",
                         "=========="])
        report.extend(member.show_by_status(ap_set_w_dates_by_status))
    if 'r' in club.ms_by_status:
        header = ('Members ({} in number) retiring from the Club:'
                .format(len(club.ms_by_status['r'])))
        report.append('')
        helpers.add_header2list(header, report, underline_char='=')
        for name in club.ms_by_status['r']:
            report.append(name)

    misc_stati = member.show_by_status(club.ms_by_status,
                                        stati2show="m|w|be".split('|'))
    if misc_stati:
        header = "Miscelaneous Info"
        helpers.add_header2list(header, report, underline_char='=')
        report.extend(misc_stati)

    try:
        with open(DEFAULT_ADDENDUM2REPORT_FILE, 'r') as fobj:
            print('Opening file: {}'.format(fobj.name))
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
    output('\n'.join(report()))

def stati_cmd():
    club = Club()
    club.infile = args["-i"]
    if not club.infile:
        club.infile = Club.MEMBERSHIP_SPoT
    if args['-A']:
        club.mode = 'applicants_only'
    else:
        club.mode = 'all'
    output('\n'.join(member.show_stati(club)))


def zeros_cmd():
    """
    Reports those with zero vs NIL in fees field.
    """
    infile = args['-i']
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    club = Club()
    club.zeros = []
    club.nulls = []
    err_code = member.traverse_records(infile, 
                [member.get_zeros_and_nulls,],
                club)
    res = ["Nulls:",
           "======",]
    res.extend(club.nulls)
    res.extend(["\nZeros:",
                  "======",])
    res.extend(club.zeros)
    output('\n'.join(res))


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
    if not args['-f']:
        args['-f'] = 'table'
    if infile.endswith(TEXT):
        print('<infile> ends in "{}"; reading from SPoL'.
                                        format(TEXT))
        if args['-f'] == 'listing':  # No processing needed..
            # Just return file content:
            with open(infile, 'r') as f_object:
                output(f_object.read())
        else:
            if args['-j']:
                json_file = args['-j']
            else:
                json_file = False
            extra_fees = data.gather_extra_fees_data(infile,
                                                json_file=json_file)
            by_name = extra_fees[Club.NAME_KEY]
            by_category = extra_fees[Club.CATEGORY_KEY]
            if args['-f'] == 'table':  # Names /w fees in columns:
                res = data.present_fees_by_name(by_name, raw=True)
                ret = helpers.tabulate(res, down=True,
                            max_width=max_width, separator=' ')
                if not args['-r']:
                    header = ["Extra fees by member:",
                              "=====================",  ]
                    ret = header + ret
                output('\n'.join(ret))
            elif args['-f'] == 'listings':
                output('\n'.join(data.present_fees_by_category(
                                        extra_fees, raw=args['-r'])))
#               output('\n'.join(data.show_fee_listings(extra_fees,
#                                                           args['-r'])))
            else:
                print("""Bad argument for '-f' option...
        Choose one of the following:        [default: table]
                'table' listing of names /w fees tabulated (=> 2 columns.)
                'listing' same format as Data/extra_fees.txt
                'listings' side by side lists (best use landscape mode.)
    """)
    elif infile.endswith(CSV):
        print('Not set up to deal with csv file yet.')
        assert(False)
    else:
        print('<infile> must end in ".txt" or ".csv"')
        assert(False)


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
        if args['-T']:
            tabulated = helpers.tabulate(club.still_owing,
                                    max_width=max_width,
                                    separator = '')
            output.extend(tabulated)
        else:
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
    See description under 'Commands' heading in the docstring.
    Sets up an instance of rbc.Club with necessary attributes and
    then calls member.prepare_mailing() method.
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
    # *** Check that we don't overwright previous mailings:
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
    print("""prepare_mailing completed..
    ..next step might be the following:
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
        .format(n_emails))
    return "\n".join(all_emails)


def send_emails_cmd():
    """
    Package msmtp is a dependency: # apt install msmtp
    There must be a ~/.msmtprc configuration file. See an example
    within the ./Notes directory (./Notes/msmtprc.)
    (I think this applies only if using gmail.)
    (With easydns I believe Pymail.send.send does everything.)

    The format of the <json_file> ("-j" parameter) varies depending
    on whether or not easydns.com is used (as specified by the -E
    option.) See docstring for member.append_email.

    If using gmail the gmail account security setting must be lowered:
    https://myaccount.google.com/lesssecureapps
    """
    j_file = args["-j"]
    message = None
    with open(j_file, 'r') as f_obj:
        data = json.load(f_obj)
        print('Loading JSON from "{}"'.format(f_obj.name))
    counter = 0
    if args['-E']:  # using easydns
        Pymail.send.send(data, service='easy', include_wait=False)
    else:  # using gmail
        response = input( # Check lesssecureapps setting:
'Has "https://myaccount.google.com/lesssecureapps" been set?')
        if ((not response) or
        not (response[0] in 'Yy')):
            print("Please do that then begin again.")
            sys(exit)
        for datum in data:
            try:
                recipients = datum[0]
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
    Uses mutt (in member.send_attachment.)
    Sends emails with an attachment.
    Sets up an instance of Club and traverses
    the input file calling member.send_attachment
    on each record.
    """
    club = Club()
    club.mutt_send = mutt_send
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
    If '-t <temp_membership_file>' is specified, the original
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

def fee_intake_totals_cmd():
    infile = args['-i']
    outfile = args['-o']
    errorfile = args['-e']
    club = Club()
    if infile:
        fees_taken_in = club.fee_totals(infile)
    else:
        fees_taken_in = club.fee_totals()
    fees_taken_in.append(" ")
    res = '\n'.join(fees_taken_in)
    output(res)
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
    Does the mass e-mailings with attachment(s) which, if
    provided, must be in the form of a list of files.
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
    elif args["zeros"]:
        zeros_cmd()
    elif args["usps"]:
        print("Preparing a csv file listing showing members who")
        print("receive meeting minutes by mail. i.e. don't have (or")
        print("haven't provided) an email address (to the Club.)")
        output(usps_cmd())
    elif args["extra_charges"]:
        print("Selecting members with extra charges:")
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
    elif args['fee_intake_totals']:
        fee_intake_totals_cmd()
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
