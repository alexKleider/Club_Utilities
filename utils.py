#!/usr/bin/env python3

# File: utils.py

"""
"utils.py" is an utility providing functionality for usage and
maintanance of the Bolinas Rod and Boat Club membership records.
Most commands deal with a csv file named "./Data/memlist.csv" so for
these it is the default input file.
Labels and Envelopes (along with the '-P <params>' option) have
been deprecated but the code left in place incase anyone ever
wishes to revive them.  Current usage replaces them with emails and
letters (which can be prepared using the 'prepare_mailing' command.)
Consult the README file for further info.

Usage:
  ./utils.py [-O -w <width> -r <rows> ] [ -? | --help | --version]
  ./utils.py ck_data [-O -d -i <infile> -A <app_spot> -S <sponsors_spot> -X <fees_spot> -C <contacts_spot> -o <outfile>]
  ./utils.py show [-O -i <infile> -A <applicant_spot> -S <sponsors_spot> -o <outfile> ]
  ./utils.py report [-O -i <infile> -A <applicant_spot> -S <sponsors_spot> -o <outfile> ]
  ./utils.py stati [-O -D -M -B -m -s stati -i <infile> -A <applicant_spot> -S <sponsors_spot> -o <outfile>]
  ./utils.py create_applicant_csv [-O -i <infile> -A <applicant_spot> -S <sponsors_spot> -o <outfile>]
  ./utils.py zeros [-O -i <infile> -o <outfile]
  ./utils.py usps [-O -i <infile> -o <outfile>]
  ./utils.py extra_charges [-O -w <width> -f <format> -X <fees_spot> -o <outfile> -j <jsonfile>]
  ./utils.py payables [-O -T -w <width> -i <infile> -o <outfile>]
  ./utils.py show_mailing_categories [-O -T -w <width> -o <outfile>]
  ./utils.py prepare_mailing --which <letter> [-O --oo -p <printer> -i <infile> -j <json_file> --dir <mail_dir> --cc <cc> --bcc <bcc> ATTACHMENTS...]
  ./utils.py thank [-t <2thank> -O -p <printer> -j <json_file> --dir <mail_dir> -o <temp_membership_file> -e <error_file>]
  ./utils.py display_emails [-O] -j <json_file> [-o <txt_file>]
  ./utils.py send_emails [-O --mta <mta> --emailer <emailer>] -j <json_file>
  ./utils.py emailing [-O -i <infile> -F <muttrc>] --subject <subject> -c <content> [ATTACHMENTS...]
  ./utils.py restore_fees [-O -i <membership_file> -X <fees_spot> -o <temp_membership_file> -e <error_file>]
  ./utils.py fee_intake_totals [-O -i <infile> -o <outfile> -e <error_file>]
  ./utils.py (labels | envelopes) [-O -i <infile> -P <params> -o <outfile> -x <file>]
  ./utils.py wip [-O -o <outfile>]
  ./utils.py new_db -F function [-O -i <membership_file> -o <new_membership_file> -e <error_file>]

Options:
  -h --help  Print this docstring. Best piped through pager.
  -?  Print allowed commands and their options.
  --version  Print version.
  -a <app_csv>  csv version of applicant data file.
  -A <app_spot>   Applicant data file.
  --bcc <bcc>   Comma separated listing of blind copy recipients
  --cc <cc>   Comma separated listing of cc recipients
        If a single string "sponsors" is specified, then one assumes
        the recipient is an appliacant and copies will be sent to
        sponsors. Implementation of this feature is still underway-
        implementation within the "--which" option vs the command line level.
  -c <content>   The name of a file containing the body of an email.
  -C <contacts_spot>   Contacts data file.
  -d   Include details: fee inconsistency for ck_data,
  --dir <mail_dir>   The directory (to be created and/or read)
                     containing letters for batch printing.
  -e <error_file>   Specify name of a file to which an
            error report can be written.  [default: stdout]
  --emailer <emailer>  Use bash (via smtp or mutt) or python
                    to send emails.  [default: python]
  -f <format>  Specify output format of 'extra_charges' command.
        Possible choices are:
            'table' listing of names /w fees tabulated (=> 2 columns.)
            'listing' same format as Data/extra_fees.txt
            'listings' side by side lists (best use landscape mode.)
        [default: listings]
  -F <function>  Name of function to apply. (new_db command)
  -i <infile>  Specify file used as input. Usually defaults to
                the MEMBERSHIP_SPoT attribute of the Club class.
  -I <included>  Specify what's to be included by specifying the key
          of the f-string to use. (See members.fstrings)
          ## Still needs to be implemented to replace '-l' option
          ## Note: not used anywhere that I can currently see!! ##
          ##    Tue 07 Sep 2021 06:14:43 PM PDT                 ##
  -D   include demographic data  (see also -I & -l options)
  -M   include meeting dates- pertains to applicant report(s)
  -B   include backers/sponsors- pertains to applicant report(s)
  -j <json>  Specify a json formated file
              Used mainly but not exclusively for emails.
              (whether for input or output depends on context.)
  -l  Long format for demographics (phone & email as well as address)
  -m  Maximum data  Same as including -DMB. See also -I
  --mta <mta>  Specify mail transfer agent to use. Choices are:
                clubg     club's gmail account  [default: clubg]
                akg       my gmail account
                easy      my easydns account
  -O  Show Options/commands/arguments.  Used for debugging.
  -o <outfile>  Specify destination.
            Choices are stdout, printer, or the name of a file.
            NOTE: the create_applicant_csv command only accepts
            a file name which must end in ".csv".
  --oo   Owing_Only: Only consider members with dues/fees outstanding.
            (Sets owing_only attribute of instance of Club.)
  -P <params>  This option will probably be redacted
            since old methods of mailing are no longer used.
            Defaults are A5160 for labels & E000 for envelopes.
  -p <printer>  Deals with printer variablility; ensures correct
        alignment of text when printing letters. [default: X6505_e1]
  -r <rows>   Maximum number ot rows (screen height)  [default: 35]
  -s <stati>   Used with stati command; specifies stati to show.
        (<stati>: the desired stati separated by <glbs.SEPARATOR>.)
            If not specified, all stati are reported.
            Stati may include:
                <any string beginning with 'appl'>:
                    all applicants are included
                <any string beginning with 'exec'>:
                    all members of exec committee are included
        NOTE: if using the <gbls.SEPARATOR> , must wrap the
        whole argument in quotes (like so: -s "ar1|arg2|arg3")
        to prevent shell from treating each one as a pipe!!
  -S <sponsor_SPoL>  Specify file from which to retrieve sponsors.
  --subject <subject>  The subject line of an email.
  -t <2thank>   Input for thank_cmd. It must be a csv file in same
        format as memlist.csv showing recent payments.
  -T  Present data in columns (a Table) rather than a long list.
        Used with the 'payables' and 'show_mailing_categories'
        commands. May not have much effect if the -w option value
        is not a high number.
  -w <width>  Maximum number of characters (columns) per line.
            Screen widwh.  [default: 140]
  --which <letter>  Specifies type/subject of mailing.
  -x <file>  Used by commands not in use. (Expect redaction)
  -X <fees_spot>  Extra Fees data file.

Commands:
    When run without a command, suggests ways of getting help.
    ck_data: Checks all the club's data bases for consistency.
        Assumes (user must assert) a fresh export of the gmail
        contacts list. Options:
        | -d  Include fee inconsistencies (which are expected
        when some have paid.)
    show: Returns membership demographics a copy of which can then
        be sent to the web master for display on the web site.
    report: Prepares a 'Membership Report".
    stati: Returns a listing of stati (entries in 'status' field.)
        <mode> if set can be 'applicants' (Applicants only will be
            shown) or a glbs.SEPARATOR separated set of stati
            (indicating which stati to show.)
        May also include any combination of -D, -M, -S to
        include adress/demographics, meeting dates &/or sponsors
        for applicants.
    create_applicant_csv:  Output is a csv file containing data
        relevant to current applicants: first & last names, status,
        up to three meeting dates and the two sponsors. If -o outfile
        is explicitly specified it must end in ".csv".
    usps: Creates a csv file containing names and addresses of
        members without an email address who therefore receive Club
        minutes by post. Also includes any one with a 'be' or an 's'
        status (... a mechanism for sending a copy to the secretary.)
    extra_charges: Reports on members paying extra charges (for
        kayak storage, mooring &/or dock usage.)
        | -f <format>  -specify listing, listings or table format.
                (Has a default: see -f option description.)
        | -w <width>  -specify maxm # of chars per line in output.
        | -j <json_file>  -creat a json file. (This was
        but is no longer required by the restore_fees_cmd.)
    payables: Reports on non zero money fields.
        | -T  Present as a table rather than a listing.
        | -w <width>  Maximum number of characters per line if -T.
    show_mailing_categories: Sends a list of possible entries for the
        '--which' parameter required by the prepare_mailings command.
        (See the 'content_types' dict in content.py.)
    prepare_mailing:  Demands a <--which> argument to specify the
        content and the custom function(s) to be used.  Try the
        'show_mailing_categories' command for a list of choices.
        The command line arguments may end with zero or more names
        of files which are to be added as attachments to the emails.
        Other parameters have defaults set.
        '--oo'  Send request for fee payment only to those with an
        outstanding balance.  This is relevant only to mailings
        relating to dues and fees. Without this option mailings go
        to all members (including those with credit or 0 balance.
        '-p <printer>' specifies printer to be used for letters.
        '-i <infile>' membership data csv file.
        '-j <json_file>' where to dump prepared emails.
        '--dir <mail_dir>' where to file letters.
    thank:  Reads the file specified by -t <thank>, applies payments
        specified there in to the -i <infile> and prepares thank you
        letter/email acknowledging receipt of payment and showing
        current balance(s.) See prepare_mailing command for further
        details.
    display_emails: Provides an opportunity to proof read the emails.
    send_emails: Sends out the emails found in the -j <json_file>.
        Each mta has its own security requirements and each emailer
        has its own way of implementing them. Check the
        Notes/emailREADME for details.  Note that not all
        combinations of mta and emailer are working but the following
        does: "--mta clubg --emailer python". (./Notes/Mail/msmtprc.)
    restore_fees: Use this command to populate each member's record
        with what they will owe for the next club year. Respects any
        existing credits. Best done after all dues and fees have been
        paid. (Will abort if any dues or fees are still outstanding.)
        Results are *[either placed into a file specified by the '-o'
        option (if provided) or]* placed into a file named as a
        concatination of "new_" and the input file. One can then
        mannually check the new file and rename it if all is well.
        *[]* Since a new data base is created, the name of the
        output file is fixed and the '-o' option is ignored!!!
    emailing: Initially developed to allow sending of attachments.
        Since attachments are now possible using the send_mailing
        command (at least with emailer python) this command will
        most likely be redacted.
    fee_intake_totals: Input file should be a 'receipts' file with a
        specific format. It defaults to 'Data/receipts-YYYY.txt'
        where YYYY is the current year.  Output yields subtotals and
        the grand total which can be copy/pasted into the 'receipts'
        file.
    labels: print labels.       | default: -P A5160  | Both
    envelopes: print envelopes. | default: -P E000   | redacted.
    wip: "work in progress" Used for development/testing.
"""

import os
import shutil
import csv
import codecs
import sys
import platform
import time
import random
import json
import subprocess
import logging
from docopt import docopt
import sys_globals as glbs
import member
import helpers
import content
import data
import Pymail.send
import Bashmail.send
from rbc import Club

TEXT = ".txt"  # } Used by <extra_charges_cmd>
CSV = ".csv"   # } command.

TEMP_FILE = "2print.temp"  # see <output> function

args = docopt(__doc__, version=glbs.VERSION)
# allow for use of '=' when specifying param value:
for arg in args.keys():
    if type(args[arg]) == str:
        if args[arg] and (args[arg][0] == '='):
            args[arg] = args[arg][1:]
try:
    max_width = int(args['-w'])
except ValueError:
    print(
        "Value of '-w' command line argument must be an integer.")
    sys.exit()
if args["-p"] not in content.printers.keys():
    print("Invalid '-p' parameter! '{}'".format(args['-p']))
    sys.exit()


def set_default_args_4curses(args):
    """
    Run when utils is driven by curses interface.
    """
    SPONSORS_SPoT = "Data/sponsors.txt"
    EXTRA_FEES_SPoT = 'Data/extra_fees.txt'
    CONTACTS_SPoT = os.path.expanduser(      # } File to which google
                '~/Downloads/contacts.csv')  # } exports the data.
    RECEIPTS_FILE = 'Data/receipts-{}.txt'.format(helpers.this_year)
    THANK_FILE = 'Info/2thank.csv'
    args['-a'] = Club.APPLICANT_CSV
    args['-A'] = Club.APPLICANT_SPoT
    args['-C'] = Club.CONTACTS_SPoT
    args['--dir'] = Club.MAILING_DIR
    args['-e'] = Club.ERRORS_FILE
    args['-f'] = Club.DEFAULT_FORMAT
    args['-i'] = Club.MEMBERSHIP_SPoT
    args['-I'] = member.fstrings['first_last_w_all_data']
    args['-D'] = True
    args['-M'] = True
    args['-B'] = True
    args['-j'] = Club.JSON_FILE_NAME4EMAILS
    args['-l'] = True
    args['-m'] = True
#   args['--mta'] = 'clubg'  # default set by docopt
    args['-o'] = '2check.txt'
#   args['-O'] = False   # Not used by curses interface
    args['--oo'] = False
#   args['-p'] = 'X6505_e1'  # default set by docopt
#   args['-s'] = ''
    args['-S'] = Club.SPONSORS_SPoT
#   args['--subject'] = ''  # subject line of an email
    args['-t'] = Club.THANK_FILE
    args['-T'] = True
#   args['-w'] = 140  # default set by docopt
#   args['--which'] = ''  # a mandatory option
    args['-X'] = Club.EXTRA_FEES_SPoT


def confirm_file_present_and_up2date(file_name):
    """
    Asks user to confirm that the file is current.
    Aborts the program if file_name doesn't exist.
    Used for the gmail contacts.csv file.
    """
    if not os.path.exists(file_name):
        print("File '{}' expected but not found.".format(file_name))
        sys.exit()
    response = input("Is file '{}' present and up to date? "
                     .format(file_name))
    if response and response[0] in "Yy":
        return True
    else:
        print("Update the file before rerunning utility.")
        sys.exit()


def output(data, destination=Club.STDOUT, announce_write=True):
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
            if announce_write:
                print('Data written to temp file "{}".'.format(fileobj.name))
            subprocess.run(["lpr", TEMP_FILE])
            subprocess.run(["rm", TEMP_FILE])
            if announce_write:
                print('Temp file "{}" deleted after printing.'
                      .format(fileobj.name))
    else:
        with open(destination, "w") as fileobj:
            fileobj.write(data)
            if announce_write:
                print('...data written to "{}".'.format(fileobj.name))


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

    left_formatter = (" " * separation[0] +
                      "{{:<{}}}".format(n_chars_per_field))
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

    left_formatter = ("{{:<{}}}".format(n_chars_per_field))
    right_formatter = ("{{:>{}}}".format(n_chars_per_field))
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
             e000=E0000,
             a5160=A5160,
             )


def ck_data_cmd(args=args):
    print("Checking for data consistency...")
    club = Club(args)
    if confirm:
        confirm_file_present_and_up2date(club.CONTACTS_SPoT)
    output("\n".join(data.ck_data(club, fee_details=args['-d'])),
           club.outfile)


def show_cmd(args=args):
    print("Preparing membership listings...")
    club = Club(args)
    club.for_web = True
    club.format = member.fstrings['first_last_w_all_data']
    data.populate_sponsor_data(club)
    data.populate_applicant_data(club)
    err_code = member.traverse_records(
        club.infile,
        [member.add2lists,  # collects data into attributes of <club>
         member.add2ms_by_status
        ],
        club)

    ret = ["""FOR MEMBER USE ONLY

THE TELEPHONE NUMBERS, ADDRESSES AND EMAIL ADDRESSES OF THE BOLINAS ROD &
BOAT CLUB MEMBERSHIP CONTAINED HEREIN ARE NOT TO BE REPRODUCED OR DISTRIBUTED
FOR ANY PURPOSE WITHOUT THE EXPRESS PERMISSION OF THE BOARD OF THE BRBC.

Data maintained by the Membership Chair and posted here by Secretary {}.
""".format(club.SECRETARY)]

    keys = [key for key in sorted(
                    member.STATUS_KEY_VALUES.keys())
                    if (key.startswith('z')
                    and key!='zae')]
    if keys:
        helpers.add_header2list(
                "Executive Committee Members", ret,
                underline_char='=', extra_line=True)
        for key in keys:
            helpers.add_header2list(
                    "{}".format(member.STATUS_KEY_VALUES[key]),
                    ret, underline_char='-', extra_line=True)
            for exec_member in club.ms_by_status[key]:
                ret.append(member.names_reversed(exec_member))
            
    if club.members:
        helpers.add_header2list("Club Members ({} in number as of {})"
                                .format(club.nmembers, helpers.date),
                                ret, underline_char='=',
                                extra_line=True)
        ret.extend(club.members)
    if club.honorary:
        helpers.add_header2list(
            "Honorary Club Members", ret,
            underline_char='=', extra_line=True)
        ret.extend(club.honorary)
    if club.inactive:
        helpers.add_header2list(
            "Inactive Club Member(s)", ret,
            underline_char='=', extra_line=True)
        ret.extend(club.inactive)
    if club.by_n_meetings:  # change to "by_applicant_status"
        header = ("Applicants ({} in number)"
                  .format(club.napplicants))
        helpers.add_header2list(header, ret, underline_char='=')

        ret.extend(member.show_by_status(
                                club.by_n_meetings, # name change
                                club=club))

    output("\n".join(ret), club.outfile)


def get_meeting_dates(applicant_data):
    """
    <applicant_data> is a record with APPLICANT_DATA_FIELD_NAMES as
    keys. Returns a string consisting of a comma separated listing of
    meeting dates if available, else "no meetings yet".
    """
    dates = [applicant_data[key] for key in
            Club.APPLICANT_DATA_FIELD_NAMES[5:8]
            if applicant_data[key]]
    if dates: return ', '.join(dates)
    else: return "no meetings yet"


def show_stati(club, include_headers=True):
    """
    Returns a list of strings (that can be '\n'.join(ed))
    Assumes existance of following club attributes:
        ms_by_status
            +/- stati2show
        +/- napplicants
        +/- demographics
        +/- applicant_data 
        +/- special_notices_by_m
    See clients: stati_cmd, show_cmd, (+/- others?)
    If command line option -s arg has not been set, all stati will be
    listed. See description of the '-s' option. (This option (if used)
    allows clients to set the club.stati2show attribute.)
    Also: can exclude publication of headers
    by resetting <include_headers>
    """

    if (not club.ms_by_status) and include_headers:
        return ["Found No Entries with 'Status' Content."]
    ret = []
    applicant_header_written = False
    if hasattr(club, 'special_notices_by_m'):
        special_notice_members = set(club.special_notices_by_m.keys())
    else:
        special_notice_members = None
#   print('club.stati2show= {}'.format(club.stati2show))
    stati2show = [status for status in club.stati2show
            if status in club.ms_by_status.keys()]
    for status in stati2show:
        if hasattr(club, 'napplicants'):
            applicant_header = ("Applicants ({} in number)"
                                .format(club.napplicants))
        else:
            applicant_header = "Applicants"
        if status.startswith('a'):
            # Doing stuff here only for applicants but much of it
            # needs to be done for everyone who is a status holder.
            # Probably need to move some of the code out of the if
            # clause.                   DEBUG
            if (not applicant_header_written) and include_headers:
                helpers.add_header2list(
                    applicant_header,
                    ret, underline_char='=')
                applicant_header_written = True
            helpers.add_header2list(member.STATUS_KEY_VALUES[status],
                                    ret, underline_char='-')
            for applicant in sorted(club.ms_by_status[status]):
#               applicant = member.names_reversed(applicant)
                if (hasattr(club, 'demographics')
                        and club.include_addresses):
                    with open("errorfile.txt", 'w') as stream:
                        stream.write(repr(club.demographics))
                    ret.append(club.demographics[applicant])
                else:
                    ret.append(applicant)
                ## DEBUG ##
                if club.include_dates or club.include_sponsors:
                    if applicant in club.applicant_data_keys:
                        ret.append('\tDates(s) attended: {}'.
                           format(get_meeting_dates(
                               club.applicant_data[applicant])))
                        if club.include_sponsors:
#                           print(club.applicant_data[applicant])
                            ret.append('\tSponsors: {sponsor1}, {sponsor2}'.
                                       format(**club.applicant_data[applicant]))
                        else:
                            print("club.include_sponsors segment skipped")
                    else:
                        print("applicant not in applicant_data_keys")
        else:
            if include_headers:
                helpers.add_header2list(member.STATUS_KEY_VALUES[status],
                                    ret, underline_char='=')
            for status_holder in sorted(club.ms_by_status[status]):
                if hasattr(club, 'demographics'):
                    try:
                        ret.append(club.demographics[status_holder])
                    except KeyError:
                        logging.error(
                                "No entry for %s!"%status_holder)
#                   line = (club.demographics[status_holder])
#                   if (special_notice_members and
#                       status_holder in special_notice_members
#                       ):
#                       line = ('{} {}'.format(
#                           line,
#                           club.special_notices_by_m[status_holder]))
#                   ret.append(line)
                else:
                    ret.append(status_holder)
    return ret


def create_applicant_csv_cmd(args=args):


    def filtered_data(a_dict_w_dict_values,
                   test_key, excluded):
        for key in sorted(a_dict_w_dict_values.keys()):
            if not a_dict_w_dict_values[key][test_key] in excluded:
                yield a_dict_w_dict_values[key]


    EXCLUDED_STATI = {'m', 'zae'}

    club = Club(args)
    if args['-o'] in {"stdout", "printer"}:
        args['-o'] = None
    club.applicant_csv = args['-o']
    if not club.applicant_csv:
        club.applicant_csv = club.APPLICANT_CSV
    if not club.applicant_csv.endswith('.csv'):
        print("Applicant csv file name must end in '.csv'!")
        print("'{}' doesn't qualify!".format(club.applicant_csv))
        sys.exit()
    applicant_data = data.get_applicant_data(club.applicant_spot,
                                             club.sponsor_spot)
    applicant_keys = sorted(applicant_data.keys())  # sort names

    helpers.save_db(filtered_data(applicant_data,
                                  'status',
                                  EXCLUDED_STATI,
                                  ),
                    club.APPLICANT_CSV,
                    club. APPLICANT_DATA_FIELD_NAMES,  #
                    report='applicants in csv format')
    


def report_cmd(args=args):
    print("Preparing Membership Report ...")
    club = Club(args=args)
    data.populate_sponsor_data(club)
    data.populate_applicant_data(club)
    club.format = member.fstrings['first_last_w_all_data']
    club.for_web = False
    err_code = member.traverse_records(
        club.infile,
        [member.add2lists,
         member.add2ms_by_status,
        ],
        club)
    report = []
    helpers.add_header2list("Membership Report (prepared {})"
                            .format(helpers.date),
                            report, underline_char='=')
    report.append('')
    report.append('Club membership currently stands at {}.'
                  .format(club.nmembers))

#   for line in report:
#       print(line)
    if club.by_n_meetings:
        header = ("Applicants ({} in number, "
                  .format(club.napplicants) +
                  "with meeting dates & sponsors listed)")
        helpers.add_header2list(header, report, underline_char='=')
        # ####  collect applicant data:
        report.extend(member.show_by_status(club.by_n_meetings, club=club))
    if 'r' in club.ms_by_status:
        header = ('Members ({} in number) retiring from the Club:'
                  .format(len(club.ms_by_status['r'])))
        report.append('')
        helpers.add_header2list(header, report, underline_char='=')
        for name in club.ms_by_status['r']:
            report.append(name)

    misc_stati = member.show_by_status(
        club.ms_by_status, stati2show="m|w|be|ba".split('|'))
    if misc_stati:
        header = "Miscelaneous Info"
        helpers.add_header2list(header, report, underline_char='=')
        report.extend(misc_stati)

    try:
        with open(glbs.DEFAULT_ADDENDUM2REPORT_FILE, 'r') as fobj:
            addendum = fobj.read()
            if addendum:
                print('Opening file: {}'.format(fobj.name))
                report.append("\n\n")
                report.append(addendum)
    except FileNotFoundError:
        print('report.addendum not found')
    report.extend(
        ['',
         "Respectfully submitted by...\n\n",
         "Alex Kleider, Membership Chair,",
         "for presentation {}\n".format(
             helpers.next_first_friday(exclude=True))+
         "(or next board meeting, which ever comes first.)"
,
         ])
    report.extend(
        ['',
         'PS Zoom ID: 527 109 8273; Password: 999620',
        ])
    output("\n".join(report), club.outfile)


def setup4stati(club):
    club.include_addresses = args['-D'] or args['-m']  # Demographics
    if club.include_addresses:
        club.format = member.fstrings['first_last_w_all_data']
    else:
        club.format = member.fstrings['first_last']
    club.include_dates = args['-M'] or args['-m']  # Meetings
    club.include_sponsors = args['-B'] or args['-m']  # Backers
    if club.include_sponsors or club.include_dates:
        data.populate_sponsor_data(club)
        data.populate_applicant_data(club)
    if args['-s']:
        which2show = args['-s'].split(glbs.SEPARATOR)
#   if which2show:
        for s, rl in (
                ('appl', member.APPLICANT_SET),
                ('exec', member.EXEC_SET),
                ):
#               print("{}, {}".format(s, rl))
            which2show = member.replace_with_in(s, rl, which2show)
        res = sorted(set(which2show))
        club.stati2show = res
    else:  # show all stati
        club.stati2show = sorted(set(member.STATI))
#   print("stati2show: {}".format(repr(club.stati2show)))
    if not set(club.stati2show).issubset(set(member.STATI)):
        for item in club.stati2show:
            if not item in member.STATI:
                print("Invalid status: '{}'".format(item))
        print('Invalid <-s> parameter provided.')
        print(club.stati2show)
        print(member.STATI)
        sys.exit()


def stati_cmd(args=args):
    print("Preparing listings by status...")
    club = Club(args)
    club.for_web = False
    setup4stati(club)
    funcs2execute = [
        member.add2lists,
        member.add2stati_by_m,
        member.add2ms_by_status,
#       member.increment_napplicants,  # done by add2lists
        ]
    if club.include_addresses:
        funcs2execute.append(member.add2demographics)
    else: print("addresses not included!!")
    print("about to traverse '{}'".format(club.infile))
    err_code = member.traverse_records(
        club.infile,
        funcs2execute,
        club)
    print("Preparing 'Stati' Report ...")
    output('\n'.join(
        show_stati(club)
#       member.show_by_status(
#       club.ms_by_status,
#       club.stati2show,
#       club)  # to collect dates +/ sponsors
            ), club.outfile)
#   output('\n'.join(show_stati(club)), club.outfile)


def zeros_cmd(args=args):
    """
    Reports those with zero vs NIL in fees field.
    """
    club = Club(args)
    err_code = member.traverse_records(
        infile, [member.get_zeros_and_nulls, ], club)
    res = ["Nulls:",
           "======", ]
    res.extend(club.nulls)
    res.extend(["\nZeros:",
               "======", ])
    res.extend(club.zeros)
    output('\n'.join(res), club.outfile)


def usps_cmd(args=args):
    """
    Generates a cvs file used by the Secretary to send out minutes.
        first,last,address,town,state,postal_code
    (Members who are NOT in the 'email only' category.)
    """
    infile = args['-i']
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    club = Club(args)
    club.usps_only = []
    err_code = member.traverse_records(infile, [
                member.get_usps,
                member.get_secretary,
                member.get_bad_emails,
                ], club)
    print("There are {} members without an email address."
          .format(len(club.usps_only)))
    res = []
    header = []
    for key in club.fieldnames:
        header.append(key)
        if key == "postal_code":
            break
    res.append(",".join(header))
    res.extend(club.usps_only)
    # The following 2 lines are commented out because new secretary
    # Michael Rafferty doesn't need/want to be on the list.
#   if hasattr(club, 'secretary'):
#       res.append(club.secretary)
    if club.bad_emails:
        print("... and {} more with a non functioning email."
              .format(len(club.bad_emails)))
        res.extend(club.bad_emails)
    return '\n'.join(res)


def club_setup4extra_charges(args=args):
    """
    Returns an instance of rbc.Club set up with what's needed
    to run the data.extra.charges function.
    ## Should probably not use -i as argument for extra fees file ##
    """
    club = Club(args)
    try:
        club.max_width = int(args['-w'])
    except TypeError:
        print("'-w' option must be an integer")
        sys.exit()
    club.presentation_format = args['-f']
    club.bad_format_warning = """Bad argument for '-f' option...
Choose one of the following:        [default: table]
        'table' listing of names /w fees tabulated (=> 2 columns.)
        'listing' same format as Data/extra_fees.txt
        'listings' side by side lists (best use landscape mode.) """
    return club



def extra_charges_cmd(args=args):
    """
    Returns a report of members with extra charges.
    It also can create a json file: specified by the -j option.
    """
    output('\n'.join(data.extra_charges(club_setup4extra_charges())),
            args['-o'])


def payables_cmd(args=args):
    """
    Sets up club attributes still_owing and advance_payments (both
    of which are lists) and then calls member.get_payables which
    traverses the db populating them.
    """
    infile = args['-i']
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    club = Club()
    club.still_owing = []
    club.advance_payments = []
    ret = []
    err_code = member.traverse_records(infile,
                                       member.get_payables,
                                       club)
    if club.still_owing:
        helpers.add_header2list(
            "Members owing ({} in number)"
            .format(len(club.still_owing)),
            ret, underline_char='=', extra_line=True)
        if args['-T']:
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
    print('\n'.join(ret))
    output('\n'.join(ret), args['-o'])


def show_mailing_categories_cmd(args=args):
    """
    Needs to be rewritten to take advantage of the -T and -w <width>
    options.
    """
    ret = ["Possible choices for the '--which' option are: ", ]
    ret.extend(
        helpers.tabulate(
            [key for key in content.content_types.keys()],
            separator='  '))
#   ret.extend((("\t" + key) for key in content.content_types.keys()))
    output('\n'.join(ret), args['-o'])


def prepare4mailing(club):
    """
    Set up configuration in an instance of rbc.Club.
    ## Need to implement sending of copies to       ##
    ## sponsors if "-cc sponsors" option is chosen. ##
    """
    club.cc_sponsors = False
    club.owing_only = False
    if args['--oo']:
        club.owing_only = True
    club.bcc = args['--bcc']
    # Note: sponsors may be specified either by including "sponsors"
    # as an argument (or possibly part of, comma separated) of the
    # "-cc" option  or by specifying it in the "--which" part (see the
    # content.py file.)
    if args['--cc']:
        (club.cc_sponsors, club.ccs) = helpers.clarify_cc(
                                args['--cc'], 'sponsors')
    else:
        (club.cc_sponsors, club.ccs) = (False, [])
    if not args['--which']:
        club.which = content.content_types["thank"]
    else:
        club.which = content.content_types[args["--which"]]
        if "cc" in club.which.keys():
            (cc_sponsors, cced) = helpers.clarify_cc(club.which['cc'])
            club.cc_sponsors = club.cc_sponsors or cc_sponsors
            club.ccs = set(club.ccs + cced)  # remove duplicates
    if club.cc_sponsors:  # collect applicant/sponsor data
        data.populate_sponsor_data(club)
        data.populate_applicant_data(club)
        # provides the following:
        #    club.sponsor_set (set)
        #    club.sponsor_emails (dict)
        #    club.sponsors_by_applicant (dict)
        #    club.applicant_data (dict with keys:
        #      first, last, status,  
        #      app_rcvd, fee_rcvd, 1st, 2nd, 3rd, inducted, dues_paid
        #      (un fulfilled meeting dates are entered as None)
    club.lpr = content.printers[args["-p"]]
    club.email = content.prepare_email_template(club.which)
    club.letter = content.prepare_letter_template(club.which,
                                                  club.lpr)
    # *** Check that we don't overwright previous mailings:
    if club.which["e_and_or_p"] in ("both", "usps", "one_only"):
        print("Checking for directory '{}'.".format(club.mail_dir))
        club.check_mail_dir(club.mail_dir)
    if club.which["e_and_or_p"] in ("both", "email", "one_only"):
        print("Checking for file '{}'.".format(club.json_file))
        club.check_json_file(club.json_file)
        club.json_data = []


def prepare_mailing_cmd(args=args):
    """
    See description under 'Commands' heading in the docstring.
    Sets up an instance of rbc.Club with necessary attributes and
    then calls member.prepare_mailing.
    ## Need to implement sending of copies to       ##
    ## sponsors if "-cc sponsors" option is chosen. ##
    """
    # ***** Set up configuration in an instance of # Club:
    club = Club(args)
    prepare4mailing(club)
    # ***** Done with configuration & checks ...
    member.prepare_mailing(club)  # Populates club.mail_dir
    #                               and moves json_data to file.
    print("""prepare_mailing completed..
    ..next step might be the following:
    $ zip -r 4Michael {}""".format(args["--dir"]))


def setup4new_db(club):
    """
    Clients are thank_cmd & restore_fees_cmd
    Over rides output file name and 
    """
    # over ride output file name:
    club.outfile = helpers.prepend2file_name('new_', club.infile)
#   print('club.outfile set to {}'.format(club.outfile))
    club.fieldnames = data.get_fieldnames(club.infile)


def dict_write(f, fieldnames, iterable):
    """
    Writes all records received from <iterable> into a new csv
    file named <f>.  <fieldnames> defines the record keys.
    Code writen in such a way that <iterable> could be
    a generator function. (See member.modify_data.)
    """
    with open(f, 'w',
              newline=''  # recommended option if file object
             ) as outfile_obj:
        print("Opening {} for output...".format(outfile_obj.name))
        dict_writer = csv.DictWriter(outfile_obj,
                                     fieldnames,
                                     lineterminator='\n'
#                                    dialect='unix'
                                    )
        dict_writer.writeheader()
        for record in iterable:
            dict_writer.writerow(record)


def thank_cmd(args=args):
    club = Club(args)
    member.traverse_records(club.thank_file,
                            [member.add2statement_data, ],
                            club)
    # To implememnt: maintain a record of those thanked...
    club.statement_data_keys = club.statement_data.keys()
    prepare4mailing(club)
    member.prepare_mailing(club)  # => thank_func
    # Done with thanking; Must now update DB.
    setup4new_db(club)  # over rides output file name
                        # & collects field names => club.fieldnames
    dict_write(club.outfile,
               club.fieldnames,
               member.modify_data(club.infile,
                                  member.credit_payment_func,
                                  club)
               )


def display_emails_cmd(args=args):
    records = helpers.get_json(args['-j'], report=True)
    all_emails = []
    n_emails = 0
    for record in records:
        email = []
        for field in record:
            email.append("{}: {}".format(field, record[field]))
        email.append('')
        all_emails.extend(email)
        n_emails += 1
    print("Processed {} emails...".format(n_emails))
    return "\n".join(all_emails)


def ck_lesssecureapps_setting():
    """
    Does nothing if not using a gmail account. (--mta ending in 'g')
    If using gmail the account security setting must be lowered:
    https://myaccount.google.com/lesssecureapps
    """
    if args['--mta'].endswith('g'):
        print(             # Check lesssecureapps setting:
            'Has "https://myaccount.google.com/lesssecureapps" been set')
        response = input(
            '.. and have you respoinded affirmatively to the warning? ')
        if ((not response) or not (response[0] in 'Yy')):
            print("Emailing won't work until that's done.")
            sys.exit()


def send_emails_cmd(args=args):
    """
    Sends emails prepared by prepare_mailing_cmd.
    See also content.authors_DOCSTRING.
    """
    if confirm:
        ck_lesssecureapps_setting()
    mta = args["--mta"]
    emailer = args["--emailer"]
    if emailer == "python":
        emailer = Pymail.send.send
        print("Using Python modules to dispatch emails.")
    elif emailer == "bash":
        emailer = Bashmail.send.send
        print("Using Bash to dispatch emails.")
    else:
        print('"{}" is an unrecognized "--emailer" option.'
              .format(emailer))
        sys.exit(1)
    wait = mta.endswith('g')
    message = None
    data = helpers.get_json(args['-j'], report=True)
    emailer(data, mta, include_wait=wait)


def emailing_cmd(args=args):
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


def restore_fees_cmd(args=args):
    """
    If records are found with balance still outstanding, these are
    reported to errors.  Also reported will be anyone listed as paying
    fees but not found amongst members.
    Repopulates the club's master list with the ANNUAL_DUES constant
    and any fees being charged as specified in the file specified by
    'args['<extra_fees.json>']'.
    The -i <membership_file> is not changed.
    If '-o <temp_membership_file>' is specified, output goes there,
    if not, output goes to a file named by concatenating 'new_' with
    the name of the input file.
    """
    # ## During implementation, be sure to ...                     ###
    # ## Take into consideration the possibility of credit values. ###
    club = Club()
    setup4new_db(club)
    data.restore_fees(club)  # Populates club.new_db & club.errors
    helpers.save_db(club.new_db, club.outfile, club.fieldnames,
                 report="New membership DB")
    if club.errors:
        output('\n'.join(
               ['Note the following irregularities:',
                '==================================', ]
               + club.errors), destination=args['-e'])

    if club.errors and args["-e"]:
        with open(args["-e"], 'w') as file_obj:
            file_obj.write('\n'.join(club.errors))
            print('Wrote errors to "{}".'.format(file_obj.name))


def fee_intake_totals_cmd(args=args):
    """
    This command deals with the manual method of entering receipts.
    Eventually this will be deprecated in favour of the thank_cmd
    """
    outfile = args['-o']
    errorfile = args['-e']
    club = Club()
    if args['-i']:
        fees_taken_in = club.fee_totals(infile=args['-i'])
    else:
        fees_taken_in = club.fee_totals()
    fees_taken_in.append(" ")
    res = '\n'.join(fees_taken_in)
    output(res, args['-o'])
    if club.invalid_lines and errorfile:
        print('Writing possible errors to "{}".'
              .format(errorfile))
        output('\n'.join(club.invalid_lines),
               errorfile, announce_write=False)


def labels_cmd(args=args):
    if args["-P"]:
        medium = media[args["-P"]]
    else:
        medium = A5160
    club = Club(medium)
    club = args["-i"]
    return club.get_labels2print(source_file)


def envelopes_cmd(args=args):
    if args["-P"]:
        medium = media[args["-P"]]
    else:
        medium = E0000
    club = Club(medium)
    source_file = args["-i"]
    club.print_custom_envelopes(source_file)


def wip_cmd(args=args):
    """
    Code under development (work in progress) temporarily housed here.
    """
    applicants = data.get_applicant_data(Club.APPLICANT_SPoT,
                                         Club.SPONSORS_SPoT)
    ret = []
    for key in sorted(applicants.keys()):
        if applicants[key]['status'] in {'m', 'zae'}:
            continue
        dates = []
        for date_key in Club.MEETING_DATE_NAMES:
            if applicants[key][date_key]:
                dates.append(applicants[key][date_key])
        if dates:
            ret.append("{}: {}"
                       .format(key, ', '.join(dates)))
        else:
            ret.append("{}: no meetings to date".format(key))
    print("Meeting dates are:")
    print("==================")
    print("\n".join(ret))


# # Plan to redact the next two functions in favour of using
# # the Python mailing modules instead of msmtp and mutt.
# # For the time being the Python modules are being used
# # when sending via Easydns.com but msmtp is still being
# # used when gmail is the MTA.


notused = '''
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
    cmd_args = ["msmtp", "-a", glbs.MSMTP_ACCOUNT, ]
    for recipient in recipients:
        cmd_args.append(recipient)
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE,
                       input=message, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))
'''


def mutt_send(recipient, subject, body, attachments=None):
    """
    Does the mass e-mailings with attachment(s) which, if
    provided, must be in the form of a list of files.
    """
    cmd_args = ["mutt", "-F", args["-F"], ]
    cmd_args.extend(["-s", "{}".format(subject)])
    if attachments:
        list2attach = ['-a']
        for path2attach in attachments:
            list2attach.append(path2attach)
        cmd_args.extend(list2attach)
    cmd_args.extend(["--", recipient])
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE,
                       input=body, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))


if __name__ == "__main__":
    print("Architecture: {}  Platform: {}".
            format(platform.architecture(), sys.platform))
    using_curses = False
    confirm = True

#   print("About to call helpers.print_args...")
    helpers.print_args(args, '-O')
#   print(".. finished call to helpers.print_args.")
    if args['-?']:
        ## How much of this is in common with parsing docstring for
        ## the curses interface module?  ?refactoring is in order??
        ## See the parse4opt... functions in (curses) interface.py.
        ## Use docoptparser.py module??
        helpers.print_usage_and_options(__doc__)
        sys.exit()

    if args["ck_data"]:
        ck_data_cmd()
    elif args["show"]:
        show_cmd()
    elif args["report"]:
        report_cmd()
    elif args["stati"]:
        stati_cmd()
    elif args["create_applicant_csv"]:
        create_applicant_csv_cmd()
    elif args["zeros"]:
        zeros_cmd()
    elif args["usps"]:
        print("Preparing a csv file listing showing members who")
        print("receive meeting minutes by mail. i.e. don't have (or")
        print("haven't provided) an email address (to the Club.)")
        output(usps_cmd(), args['-o'])
    elif args["extra_charges"]:
        print("Selecting members with extra charges:")
        extra_charges_cmd()
    elif args["payables"]:
        print("Preparing listing of payables...")
        payables_cmd()
    elif args['show_mailing_categories']:
        show_mailing_categories_cmd()
    elif args["prepare_mailing"]:
        print("Preparing emails and letters...")
        prepare_mailing_cmd()
        print("...finished preparing emails and letters.")
    elif args["thank"]:
        print("Preparing thank you emails and/or letters...")
        thank_cmd()
#       print("...finished preparing thank you emails and/or letters.")
    elif args['display_emails']:
        # displaying emails does not involve rbc.Club so must 
        # deal with ouput file here:
        if not args['-o']: args['-o'] = Club.STDOUT
        output(display_emails_cmd(), args['-o'])
    elif args["send_emails"]:
        print("Sending emails...")
        send_emails_cmd()
        print("Done sending emails.")
    elif args['emailing']:
        emailing_cmd()
    elif args['restore_fees']:
        restore_fees_cmd()
    elif args['fee_intake_totals']:
        fee_intake_totals_cmd()
    elif args["labels"]:
#       print("Printing labels from '{}' to '{}'"
#             .format(args['-i'], args['-o']))
        output(labels_cmd(), args['-o'])
    elif args["envelopes"]:
        # destination is specified within Club
        # method print_custom_envelopes() which is called
        # by print_statement_envelopes()
        print("""Printing envelopes...
    addresses sourced from '{}'
    with output sent to '{}'"""
              .format(args['-i'], args['-o']))
        envelopes_cmd()
    elif args["wip"]:
        print("Work in progress command...")
        wip_cmd()
    elif args["new_db"]:
        print("Creating a modified data base...")
        new_db_cmd()
    else:
        print("You've failed to select a command.")
        print("Try ./utils.py ?           # brief!  or ...")
        print("    ./utils.py -h          # for more detail  or ...")
        print("    ./utils.py -h | pager  # to catch it all.")

else:  # Using curses interface.
    using_curses = True
    confirm = False
    set_default_args_4curses(args)
#   def print(*args, **kwargs):
#       pass

NOTE = """
emailing_cmd()
    uses Club.traverse_records(infile,
        club.send_attachment(args["-i"]))
"""
