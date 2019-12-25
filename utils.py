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
  ./utils.py [ ? | --help | --version ]
  ./utils.py ck_fields [-r -S -i <infile> -o <outfile>]
  ./utils.py compare_gmail [<gmail_contacts> -r -i <infile> -s <sep> -j <json> -o <outfile>]
  ./utils.py show [-r -i <infile> -o <outfile> ]
  ./utils.py stati [-A | -B | -W] [-i <infile> -o <outfile>]
  ./utils.py usps [-i <infile> -o <outfile>]
  ./utils.py extra_charges [--raw -i <infile> -o <outfile> -j <jsonfile>]
  ./utils.py payables [-i <infile>] -o <outfile>
  ./utils.py show_mailing_categories [-o <outfile>]
  ./utils.py prepare_mailing --which <letter> [--lpr <printer> -i <infile> -j <json_file> --dir <dir4letters>]
  ./utils.py display_emails -j <json_file> [-o <txt_file>]
  ./utils.py send_emails [<content>] -j <json_file>
  ./utils.py print_letters --dir <dir4letters> [-s <sep> -e error_file]
  ./utils.py emailing [-i <infile> -F <muttrc>] --subject <subject> -c <content> [-a <attachment>]
  ./utils.py restore_fees [<membership_file> -j <json_fees_file> -t <temp_membership_file> -e <error_file>]
  ./utils.py fees_intake [-i <infile> -o <outfile> -e <error_file>]
  ./utils.py (labels | envelopes) [-i <infile> -p <params> -o <outfile> -x <file>]

Options:
  -h --help  Print this docstring.
  --version  Print version.
  --dir <dir4letters>  The directory to be created and/or read
                      containing letters for batch printing.
  -e <error_file>  Specify name of a file to which an error report
                    can be written.  If not specified, errors are
                    generally reported to stdout.
  -i <infile>  Specify file used as input. Usually defaults to
                the MEMBERSHIP_SPoT attribute of the Club class.
  -j <json>  Specify a json formated file (whether for input or output
              depends on context.)
  -t <temp_file>  An option provided for when one does not want to risk
                  corruption of an important input file which is to be
                  modified, thus providing an opportunity for proof
                  reading the 'modified' file before renaming it to
                  the original. (Typically named '2proof_read.txt'.)
  --which <letter>  Specifies type/subject of mailing. (See
                  'content_types' dict in content.py.)
  -o <outfile>  Specify destination. Choices are stdout, printer, or
                the name of a file. [default: stdout]
  -p <params>  If not specified, the default is
              A5160 for labels & E000 for envelopes.
  --lpr <printer>  The postal_header must be specific to the printer
            used. This provides a method of specifying which to use
            if content.which.["postal_header"] isn't already
            specified.  [default: X6505]
  -r --raw  Supress headers (to make the output suitable as
            input for creating tables.)
  -s <separator>  Some commands may have more than one component to
          their output.  Such componentes can be seprated by either
          a line feed (LF) or a form feed (FF).  [default: FF]
  -S  ck_fields command also provides listing of members having
            content in their 'status' field.
  --subject <subject>  The subject line of an email.
  -c <content>  The name of a file containing the body of an email.
  -a <attachment>  The name of a file to use as an attachment.
  -F <muttrc>  The name of a muttrc file to be used.
                        [default: muttrc_rbc]
  <gmail_contacts>  [default: ~/Downloads/contacts.csv]
  -A  A 'stati' only option: show only applicants.
  -B  A 'stati' only option: show only bad emails.
  -W  A 'stati' only option: show only members whose fees are waived.

Commands:
    When run without a command, suggests ways of getting help.
    ck_fields: Check for integrety of the data base- not fool proof!
        Sends results to -o <outfile> only if there are bad records.
        Use of -r --raw option supresses the header line.
    compare_gmail: Checks the gmail contacts for incompatabilities
        with the membership list. Assumes a fresh export of the
        contacts list.  If the -j option is specified, it names the
        file to which to send emails (in JSON format) to members with
        differing emails. (After proof reading, use 'send_emails'.)
    show: Returns membership demographics. A copy is sent to the web
        master for display on the web site.
    stati: Returns a listing of stati.  Applicants plus ..
        Depends on acurate entries in 'status' field.
    usps: Creates a csv file containing names and addresses of
        members without an email address who therefore receive their
        Club minutes by post. 
    extra_charges: Provides lists of members with special charges.
        Both a list of members each with the charge(s) they pay and
        separate lists for each category of charge. (Dues not
        included.)
        If the <infile> name ends in '.csv' then the/membership main
        data base file is assumed and output will be charges
        outstanding (i.e. owed but still not payed.) If it ends in
        '.txt' then it is assumed to be in the format of the
        "extras.txt" file and output will include all who are paying
        for one or more of the Club's three special privileges. There
        is also the option of creating a json file needed by the
        restore_fees_cmd. (See the README file re SPoL.)
    payables: reports on content of the member data money fields
        providing a listing of those who owe and those who have paid
        in advance.
    show_mailing_categories: Sends a list of possible entries for the
        '--which' parameter required by the prepare_mailings command.
    prepare_mailing: A general form of the billing command (above.)
        This command demands a TYPE positional argument to specify the
        mailing: more specifically, it specifies the content and the
        custom function(s) to be used.  Try the
        'show_mailing_categories' command for a list of choices.
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

# Constants required for correct rendering of "?" command:
TOP_QUOTE_LINE_NUMBER = 11      #} These facilitate preparing
BLANK_LINE_ABOVE_USAGE = 21     #} response to the
BLANK_LINE_ABOVE_OPTIONS = 40   #} 'utils.py ?' command.

MSMTP_ACCOUNT = "gmail"
MIN_TIME_TO_SLEEP = 2   #} Seconds between
MAX_TIME_TO_SLEEP = 10  #} email postings.

CONTACTS = os.path.expanduser('~/Downloads/contacts.csv')

TEXT = ".txt"  #} Used by <extra_charges_cmd>
CSV = ".csv"   #} command.

TEMP_FILE = "2print.temp"
SECRETARY = ("Peter", "Pyle")

args = docopt(__doc__, version="1.1")

if args["-s"] == "LF":
    args["-s"] = '\n'
else:
    args["-s"] = '\n\f'

lpr = args["--lpr"]
if lpr and lpr not in content.printers.keys():
    print("Invalid '--lpr' parameter!")
    sys.exit()
if not args["<gmail_contacts>"]:
    args["<gmail_contacts>"] = CONTACTS

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
    """a Dummy class for use when templates are not required"""
    formatter = ""
    @classmethod
    def self_check(cls):  # No need for the sanity check in this case
        pass

class E0000(object):
    """
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

### Unable to easily initiate a Member object from a record, will
### simply have functions that need only a record for a param.
### Put them all into a separate 'record' module: record.py


# Specify input file and its data:
class Club(object):
    """
    Create such an object for each data base used.
    In the current use case this is the only one and
    it pertains to the 'Bolinas Rod and Boat Club'.
    Might change name of this class to "Club".
    """
    ## Google Contact Labels:
    google_labels = { "applicant," "DockUsers", "Kayak",
            "LIST", "member", "moorings", "Officers"}
    ## Constants and Defaults...
    YEARLY_DUES = 100

    # Data bases used:
    MEMBERSHIP_SPoT = 'Data/memlist.csv'          #}  Default
    EXTRA_FEES_SPoT = 'Data/extra_fees.txt'  #}  file
    CHECKS_RECEIVED = 'Data/receipts.txt'   #}  names.

    # Intermediate &/or temporary files used:
    EXTRA_FEES_JSON = 'Data/extra_fees.json'
    EXTRA_FEES_TBL = 'Data/extra_fees.tbl'  # not used!
    TEMP_MEMBERSHIP_SPoT = 'Data/new_memlist.csv'
    OUTPUT2READ = 'Data/2read.txt'       #} generally goes to stdout.
    MAILING_DIR = 'Data/MailingDir'
    JSON_FILE_NAME4EMAILS = 'Data/emails.json'
    ## ...end of Constants and Defaults.

    def __init__(self, params):
        """
        Each instance must know the format
        of the media. i.e. the parameters.
        This is being redacted since we are not using labels or
        envelopes as was done before. For the time being will simply
        use a "dummy".
        """
        self.infile = Club.MEMBERSHIP_SPoT
        self.name_tuples = []
        self.json_data = []
        self.previous_name = ''              # } Used to
        self.previous_name_tuple = ('', '')  # } check 
        self.first_letter = ''               # } ordering.

    def compare_gmail(self, source_file, google_file, separator):
        """
        Checks for incompatibilities between the two files.
        Need to add examination of "Group Membership" field of Google
        contacts.
        """
        # Determine if we'll be sending emails:
        args["-j"] = args["-j"]
        # In case we are: template = content.bad_email_template
        # Set up collectors:
        # ..temporary collectors:
        g_dict_e = dict()  # keyed by emails, names as values
        g_dict_n = dict()  # keyed by names, email as values
        missing_from_google = dict()  # keyed by first/last name tuple
        names_and_emails = []  # collected from master memlist
        # Reported:
        emails_not_found_in_g = []
        emails_not_found_in_g_header = (
            "Emails in member list but not in google contacts:")
        bad_matches = []
        bad_matches_header = "Common email but names don't match:"
        no_emails = []
        no_emails_header = (
            "Members ({} in number) without an email address:")
        differing_emails = []
        differing_emails_header = (
            "Differing emails: g-contacts & memlist:")
        # the final output
        ret = []

        # Traverse google.csv => g_dict_e and g_dict_n
#       with open(google_file, 'r', encoding='utf-16') as file_obj:
        with open(google_file, 'r', encoding='utf-8') as file_obj:
            google_reader = csv.DictReader(file_obj, restkey='status')
            print('DictReading Google contacts file "{}".'
                .format(file_obj.name))
#           g_counter = 0
#           g_collector = []
            for g_rec in google_reader:
                contact_email = g_rec["E-mail 1 - Value"]
                first_name = " ".join((
                    g_rec["Given Name"],
                    g_rec["Additional Name"],
                    )).strip()
                last_name = " ".join((
                    g_rec["Family Name"],
                    g_rec["Name Suffix"],
                    )).strip()
#               g_counter += 1
#               g_collector.append("{} {} {}".format
#                   (first_name, last_name, contact_email))

                key = contact_email
                g_dict_e[key] = (
                    first_name,
                    last_name,
                    g_rec["Group Membership"],  # ?for future use?
                    )
                
                key = (first_name, last_name,)
                g_dict_n[key] = contact_email
#               _ = input("Key: '{}', Value: '{}'".
                key = (first_name, last_name,)
                g_dict_n[key] = contact_email
#               _ = input("Key: '{}', Value: '{}'".
#                   format(key, value))
        # We now have two dicts: g_dict_e & g_dict_n
        # One keyed by email: values can be indexed as follows:
        #     [0] => first name
        #     [1] => last name
        #     [2] => colon separated list of groups
        # The other keyed by name tuple: value is email

        # Next we iterate through the member list...
        record_number = 0
        with open(source_file, 'r') as file_obj:
            dict_reader = csv.DictReader(file_obj, restkey="status")
            print('DictReading "{}".'.format(file_obj.name))
            for record in dict_reader:
                record_number += 1
#               print(record)
                email = record["email"]
                if email:
                    # append to names_and_emails as a tuple:
                    names_and_emails.append((
                        (record["first"],
                        record["last"]),
                        email))
                    try: # find out if google knows this email:
                        g_info = g_dict_e[email]
                    except KeyError:  # if not:
                        # Add to missing_from_google dict...
                        missing_from_google[
                            (record["first"],
                            record["last"])
                            ] = email
                        # and Append to emails_not_found_in_g...
                        emails_not_found_in_g.append(
                            "{} {} {}"
                            .format(record["first"],
                                record["last"],
                                email))
                        continue
                    # Google knows this email...
                    info = (record["first"],
                        record["last"])
                    if info != g_info[:2]:
                    # but names don't match so append to bad_matches..
                        bad_matches.append("{} {} {}".format(
                            info, record["email"], g_info[:2]))
                else:  # memlist has no email for this member so..
                    # append to no_emails:
                    no_emails.append("{} {}".format(
                        record["first"],
                        record["last"]))
        # Finished traversal of memlist

        # Tabulate the no_emails list to make it more presentable:
        tabulated = []
        table_format_string = "{:<23}{:<23}{:<23}"
        if no_emails:
            while len(no_emails) % 3:
                no_emails.append("")
            n_no_emails = len(no_emails)
            for i in range(0, n_no_emails, 3):
                tabulated.append(table_format_string.format(
                    no_emails[i],
                    no_emails[i + 1],
                    no_emails[i + 2]))
            no_emails = tabulated
        
        # Set up collector in case -j <json_file> is set.
        emails2send = []

        # Look for possibly differing emails...
        for name, email in names_and_emails:
            try:
                g_email = g_dict_n[name]
            except KeyError:
                continue
            if g_email != email:
                differing_emails.append(
                    "{:<9} {:<14} {:<27} {}"
                        .format(
                            name[0],
                            name[1],
                            "'{}'".format(g_email),
                            "'{}'".format(email)))
                if args["-j"]:  # append email to send
                    recipients = (g_email, email)
                    content = email_template.format(
                        ', '.join(recipients),
                        " ".join(name),
                        g_email,
                        email)
                    emails2send.append((recipients, content))

        if args["-j"]:
            with open(args["-j"], 'w') as f_obj:
                json.dump(emails2send, f_obj)
                print('Emails JSON dumped to "{}".'
                    .format(f_obj.name))

        reports_w_names = (
            (bad_matches, "Common emails but names don't match:"),
            (no_emails, no_emails_header.format(n_no_emails)),
            (emails_not_found_in_g,
                "Member emails not found in google contacts:"),
            (differing_emails,
                "Differing emails: Google vs Club"),
            )
            
        for report, report_name in reports_w_names:
            if len(report):
                report_w_header = [report_name] + report
                formatted_report = "\n".join(report_w_header)
                ret.append(formatted_report)
            else:
                ret.append("No entries for '{}'".format(report_name))
#       with open("g_collector", 'w') as file_obj:
#           file_obj.write("Number found: {}".format(g_counter) +
#               '\n' + "\n".join(g_collector))
        return separator.join(ret)
    ### End of compare_gmail method.


    @staticmethod
    def parse_extra_fees(extras_json_file):
        """
        Assumes <extras_json_file> consists of a dict with three keys
        and the value of each is a list consiting of a list of
        <first_name>, <last_name>, <integer_amount>.
        Here's the format:
        { "Mooring": [[<lastname>, <firstname>, <integer_amount>], ...  ],
        "Dock usage": [[<lastname>, <firstname>, <integer_amount>], ... ],
        "Kayak storage": [[<lastname>, <firstname>, <integer_amount>], ...]
        }
        Returns a dict of the form:
        {(<last_name>, <first_name>):  # key
            # value is a tuple with one or more of the following:
            [('dock', <int_value>),
             ('kayak', <int_value>),
             ('mooring', <int_value>)],
        ...
        }
        """
        def translate(category):
            """
            Used to convert the more human readable form into the terse
            form used as a header/key in the membership data base.
            """
            if category == "Mooring":
                return 'mooring'
            if category == "Kayak storage":
                return "kayak"
            if category == "Dock usage":
                return "dock"

        with open(extras_json_file, 'r') as file_obj:
            extra_fees = json.load(file_obj)
            print('Extra fees JSON loaded from "{}".'
                .format(fileobj.name))
        extras = {}
        for category in extra_fees.keys():
            for value in extra_fees[category]:
                to_add = (translate(category), value[2])
                name_tuple = (value[0], value[1])
                _ = extras.setdefault(name_tuple, [])
                extras[name_tuple].append(to_add)
        return extras

#   def create_extra_fees_json(self, extra_fees_txt_file):
#       # this functionality is provided by extra_fees.py
#       pass

    def restore_fees(self, membership_csv_file,
                        dues, fees_json_file,
                        new_membership_csv_file):
        """
        Dues and relevant fees are applied to each member's record
        in a new_membership_csv_file. It can then be checked before
        renaming.
        Sets up and then populates:
            <self.errors>        }  all are
            <self.name_tuples>   }  instance list
            <self.still_owing>   }  attributes
        Several conditions prevent the method from completing (i.e.
        actually restoring fees.) In each instance, the specifics are
        reported inside the <self.errors> attribute.  This happens if
        any member still has dues or fees owing or if a person appears
        in the <fees_json_file> but is not a member (i.e. in the
        <membership_csv_file>.)
        The <fees_json_file> is NOT the SPoL! The extra_fees.txt file
        is the SPoL. The json file can be optionally created by
        running the extra_charges command
        """
        print(
            "Preparing to restore dues and fees to the data base...")
        print(
            "  1st check that all have been zeroed out...")
        self.errors = []
        self.name_tuples = []
        self.still_owing = []
        # MAJOR WORK NEEDS DONE HERE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        err_code = self.traverse_records(membership_csv_file,
                    [(record["last"], record["first"]),
                    self.get_payables])  # vvv
        # Populates self.name_tuples so we can later check that
        # everyone in the extra_fees data base is in fact a member
        # and populates self.still_owing so we can check if OK to
        # proceed.
        if self.still_owing:
            self.errors.append(
                "The following members have not been zeroed out:")
            self.errors = "\n".join(self.errors + self.still_owing)
            print("The following have not been zeroed out:")
            print(self.errors)
            # self.errors can be sent to an error file by caller.
            print(
                "Can't continue until all members are 'zeroed out'.")
            return 1
        else:
            print("All members are zeroed out- OK to continue...")
            assert not self.errors

        new_file = new_membership_csv_file
        if os.path.exists(new_file):
            response = input(
                "...planning to overwrite '{}', OK? (y/n) "
                .format(new_file))
            if not response or not response[0] in "Yy":
                print("Terminating.")
                return 1

        # Preliminaries are done- time to do the work...
        fees_by_name = self.parse_extra_fees(fees_json_file)
        fee_name_tuples = set(fees_by_name.keys())
        fee_name_t_list = list(fee_name_tuples)
        fee_name_t_list.sort()
#       The following two files were used for debugging only:
#       with open("mem_name_tuples.txt", 'w') as file_obj:
#           for tup in mem_name_t_list:
#               file_obj.write("{}, {}\n".format(*tup))
#       with open("fee_name_tuples.txt", 'w') as file_obj:
#           for tup in fee_name_t_list:
#               file_obj.write("{}, {}\n".format(*tup))
        if not fee_name_tuples.issubset(self.name_tuples):
            print("There's a discrepency- one or more fee paying")
            print("members are not in the membership data base.")
            bad_set = (fee_name_tuples -
                {tup for tup in self.name_tuples})
            self.errors.append("Fee payers not in member database:")
            for last, first in bad_set:
                error = "{}, {}".format(last, first)
                print(error)
                self.errors.append(error)
            self.errors.sort()
            self.errors = '\n'.join(self.errors)
            return 1

        # Now we are ready to change the
        # data base (i.e. add dues & fees)
        new_records = []
        with open(membership_csv_file, 'r') as file_obj:
            reader = csv.DictReader(file_obj, restkey='status')
            print('Membership data loaded from "{}".'
                .format(file_obj.name))
            key_list = reader.fieldnames  # Save this for later.
            for record in reader:
                if 'w' in record["status"]:  # Fees are waved.
                    continue
                name_tuple = (record["last"], record["first"])
                dues = record['dues']
                if not dues:
                    dues = 0
                else:
                    dues = int(dues)  # To allow for members who pay
                record['dues'] = dues + self.YEARLY_DUES  # in advance.
                if name_tuple in fee_name_tuples:
                    # We've got fees to enter as well as dues.
                    print("found '{}' to be charged extra"
                        .format(', '.join(name_tuple)))
                    for category, amount in fees_by_name[name_tuple]:
                        assert isinstance(amount, int)
                        existing_amount = record[category]
                        if existing_amount:
                            existing_amount = int(existing_amount)
                        else:
                            existing_amount = 0
                        record[category] = existing_amount + amount
                new_records.append(record)

        with open(new_file, 'w') as file_obj:
            writer = csv.DictWriter(file_obj, fieldnames= key_list)
            writer.writeheader()
            for record in new_records:
                writer.writerow(record)
            new__file = file_obj.name
        print("Done with application of dues and fees...")
        print("...updated membership file is '{}'."
            .format(new__file))


    def get_labels2print(self, source_file):
        """
        Returns a text file ready to be sent to a printer.
        """
        record_reader = csv.reader(
            codecs.open(source_file, 'rU', 'utf-8'),
            dialect='excel')
        pages = []
            
        def deal_with_page(page):
#           print("Page contains {} records".format(n_records))
            """
            For now, we'll collect all the output in memory before
            dispencing it.  May later modify the code to dispence
            one page at a time to restrict memory usage.
            """
            page = '\n'.join(page)
            pages.append(page)
        

        # Deal with a page at a time:
        time2quit = False
        while True:
            # deal with one page at a time:
            page = []

            # put empty lines at top of page:
            for _ in range(self.params.top_margin):
                page.append("")
            # set up all the rows in the page:
            for _ in range(self.params.n_rows_per_page):
                # add a row at a time:
                row_of_data = []
                # collect records to fill a row:
#               print("Collect records to fill a row:)")
                while len(row_of_data) < self.params.n_labels_per_row:
                    try:
#                       print("About to 'next(record_reader)'")
                        next_record = next(record_reader)
#                       print("Just did  'next(record_reader)'")
                    except StopIteration:
#                       print("StopIteration")
#                       _ = input("Enter to continue")
                        next_record = None
                        time2quit = True
                    if next_record:
                        valid_row = self.get_fields(next_record)
                        if valid_row:
                            row_of_data.append(valid_row)
                        else:
                            print("## Input item being left out!")
                            # failure probably because of non
                            # conforming input data.
                    else:
#                       print(
#                           "No next_recorde- appending emtpy_label")
                        row_of_data.append(self.params.empty_label)
#                   print("len(row_of_data) is {}"
#                       .format(len(row_of_data)))
                # We have a row of records but we
                # want columns of record fields:
                for j in range(self.params.n_lines_per_label):
                    # the next set of lines
                    line_components = []
                    for i in range(self.params.n_labels_per_row):
                        line_components.append(row_of_data[i][j])
                    line = ""
                    for l in range(self.params.n_labels_per_row):
                        line = (line +
                            " " * self.params.separation[l] + 
                            line_components[l])
                    line = line.rstrip()
                    if len(line) > self.params.n_chars_wide:
                        original = line
                        line = line[:self.params.n_chars_wide]
                        print("Too long a line...")
                        print(original)
                        print("...is being stripped to:")
                        print(line)
                    page.append(line)

            deal_with_page(page)
            if time2quit:
                break
        print("{} pages ready to print".format(len(pages)))
        return "\f".join(pages) 

    def check_dir4letters(self, dir4letters):
        """
        Set up the directory for postal letters.
        """
        if os.path.exists(dir4letters):
            print("The directory '{}' already exists."
                .format(dir4letters))
            response = input("... OK to overwrite it? ")
            if response and response[0] in "Yy":
                shutil.rmtree(dir4letters)
            else:
                print(
            "Without permission, must abort.")
                sys.exit(1)
        os.mkdir(dir4letters)
        pass

    def check_json_file(self, json_email_file):
        """
        Checks the name of the json output file where
        emails are to be stored.
        """
#       print("method check_json_file param is: {}"
#           .format(json_email_file))
        if os.path.exists(json_email_file):
            print("The file '{}' already exists."
                .format(json_email_file))
            response = input("... OK to overwrite it? ")
            if response and response[0] in "Yy":
                os.remove(json_email_file)
            else:
                print(
            "Without permission, must abort.")
                sys.exit(1)

    def annual_usps_billing2dir(self, source_file, dir4letters):
        """
        Creates (or replaces) <dir4letters> and populates it with
        annual billing statements, one for each member without an
        email addresses on record.
        Note: probably totally redacted- functionality replaced by
        prepare_mailing command.
        """
        if os.path.exists(dir4letters):
            print("The directory '{}' already exists.".
                format(dir4letters))
            response = input("... is it OK to overwrite it? ")
            if response and response[0] in "Yy":
                shutil.rmtree(dir4letters)
            else:
                print(
            "Without permission, must abort.")
                sys.exit(1)
        os.mkdir(dir4letters)
        record_reader = csv.reader(
            codecs.open(source_file, 'rU', 'utf-8'),
            dialect='excel')
        errors = []
        while True:
            additional = ['',]
            try:
                next_record = next(record_reader)
            except StopIteration:
                break
            email = next_record[self.i_email]
            if not email:
                try:
                    extras = [0 if not i else int(i) for i in
                        next_record[self.i_mooring:self.i_kayak + 1]]
                except ValueError:
                    line = "HEADERS: " + ",".join([
                        next_record[self.i_last],
                        next_record[self.i_first],
                        next_record[self.i_email],
                        next_record[self.i_mooring],
                        next_record[self.i_dock],
                        next_record[self.i_kayak],
                        ])
                    errors.append(line)
                    continue
                last = next_record[self.i_last]
                first = next_record[self.i_first]
                address = next_record[self.i_address]
                town = next_record[self.i_town]
                state = next_record[self.i_state]
                postal_code = next_record[self.i_zip_code]
                dues = next_record[self.i_dues]
                if dues:
                    dues = int(dues)
                else:
                    dues = 0
                if not (fees or dues):
                    continue
                fees = sum(extras)
                if fees:
                    additional.append(
                        "In addition you are being charged for:")
                    if extras[0]:
                        additional.append(
                            "\tString & Mooring:    ${}"
                                .format(extras[0]))
                    if extras[1]:
                        additional.append(
                            "\tDock Use:            ${}"
                                .format(extras[1]))
                    if extras[2]:
                        additional.append(
                            "\tKayak/Canoe Storage: ${}"
                                .format(extras[2]))
                    additional.append(
                        "\nTotal due: ${}"
                            .format(fees + dues))
                    additional.append("\n")
                # now send the letter to the directory:
                path2write = os.path.join(
                    dir4letters, "_".join((last, first)))
                with open(path2write, "w") as file_object:
                    file_object.write(
                        self.usps_billing_letter_format.format(
                            first, last,
                            address,
                            town, state, postal_code,
                            first, last,
                            '\n'.join(additional),
                            )
                        )
        if errors:
            print("Records (header only?) that weren't processed:")
            for error in errors:
                print(error)

    def fees_intake(self, infile=CHECKS_RECEIVED):
        """
        Returns a list of strings: subtotals and grand total.
        Sets up and populates self.invalid_lines ....
        (... the only reason it's a class method
        rather than a function or a static method.)
        NOTE: Money taken in (or refunded) must appear
        within line[23:28]! i.e. maximum 5 digits (munus sign
        and only 4 digits if negatime).
        """
        res = ["Fees taken in to date:"]
        self.invalid_lines = []

        total = 0
        subtotal = 0
        date = ''

        with open(infile, "r") as file_obj:
            print('Reading from file "{}".'
                .format(file_obj.name))
            for line in file_obj:
                line= line.rstrip()
                if line[:5] == "Date:":
                    date = line
                if (line[24:27] == "---") and subtotal:
                    res.append("    SubTotal            --- ${}"
                        .format(subtotal))
        #           res.append("{}\n    SubTotal            --- ${}"
        #               .format(date, subtotal))
                    subtotal = 0
                try:
                    amount = int(line[23:28])
                except (ValueError, IndexError):
                    self.invalid_lines.append(line)
                    continue
        #       res.append("Adding ${}.".format(amount))
                total += amount
                subtotal += amount
        res.append("\nGrand Total to Date:    --- ---- ${}"
            .format(total))
#       print("returning {}".format(res))
        return res
## Custom Functions:

    def send_mailing(self, record, content, both=False):
        """
        Sends emails to 'email_only' members and letters to others.
        """
        def send_letter():
            entry = (content["postal_header"]
                    + content["body"]).format(**record)
            entry = helpers.indent(entry)
            path2write = os.path.join(self.dir4letters,
                "_".join((record["last"], record["first"],)))
            with open(path2write, 'w') as file_object:
                print('Writing to file "{}".'
                    .format(file_object.name))
                file_object.write(entry)
        letter_sent = False
        record["subject"] = content["subject"]
        record["date"] = helpers.get_datestamp()
        if record['email']:
            entry = (content["email_header"]
                    + content["body"]).format(**record)
            self.json_data.append([[record["email"]],entry])
        else:
            send_letter()
            letter_sent = True
        if both and not letter_sent:
            send_letter()

    def send_usps(self, record, content):
        """
        Sends USPS letters to all.
        """
        record["subject"] = content["subject"]
        record["date"] = helpers.get_datestamp()
        entry = (content["postal_header"]
                + content["body"]).format(**record)
        entry = helpers.indent(entry)
        path2write = os.path.join(self.dir4letters,
            "_".join((record["last"], record["first"],)))
        with open(path2write, 'w') as file_object:
            print('Writing to "{}".'.format(file_object.name))
            file_object.write(entry)

    def proto_cust_func(self, record, content, destinations):
        """
        <record> is expected to come from the memlist.csv file.
        <content> comes from the Formats.content.py module and
        must be compatable with the function.
        <destinations> is a dict defining values for the
        following keys:
            "json_data":
            "dir4letters":
        """
        pass

    def cust_func0(self, record, content, destinations):
        """
        <record> is expected to come from the memlist.csv file.
        <content> comes from the Formats.content.py module.
        <destinations> is a dict defining values for the
        following keys:
            "json_data":
            "dir4letters":
        """
        if record["first"][0] == "A":
            record["extra0"] = "\nYour first name begins with 'A'."
        if record["second"][1] == "K":
            record["extra1"] = "\nYour second name begins with 'K'."
        record["subject"] = content["subject"]
        pass

    def cust_new_applicant_welcome(member, content):
        if member["status"] == "a1":
            self.send_mailing(member, content)

    def welcome_func(self, member):
        """
        Welcomes new members.
        Apply to an input consisting only of the members to be
        welcomed.
        """
        if member['last'] == 'Stone':
            print("Processing {first} {last}.".format(**member))
            self.send_mailing(member, self.content)

    ### Deprecated methods: developed for "old system."

    def prn_split(self, field, params):
        """
        Helper function used for label printing.
        Fields which are too long are spread over >1 line.
        Takes <field> (a string) and returns an array of strings,
        each not longer than params.n_chars_per_field.
        Returns None and prints an error message if any word is
        longer than the specified limit.
        Returned strings are always params.n_chars_per_field long:
        left based if the beginning of a field,
        right based if constituting the 'overflow.'
        'params' must have attributes 'left_formatter' and
        'right_formatter' as well as 'n_chars_per_field'
        """
        if len(field) > params.n_chars_per_field:
    #       print("field is {} chars long".format(len(field)))
            words = field.split()
            for word in words:
                if len(word) > params.n_chars_per_field:
                    print("# Unable to process the following field...")
                    print(field)
                    print("...because has word(s) longer than {}."
                        .format(params.n_chars_per_field))
                    return
    #       print("field is split into {}".format(words))
            format_left = True
            ok_lines = []
            line = []
            for word in words:
                line.append(word)
                if len(" ".join(line)) > params.n_chars_per_field:
                    ok = " ".join(line[:-1])
                    if format_left:
                        ok_lines.append(
                            params.left_formatter.format(ok))
                        format_left = False
                    else:
                        ok_lines.append(
                            params.right_formatter.format(ok))
                    line = [word, ]
            if line:
                ok = " ".join(line)
                ok_lines.append(params.right_formatter.format(ok))
            return ok_lines
        else:
            return [params.left_formatter.format(field), ]

    def get_fields(self, record):
        """ No prerequisite.
        Makes text of fields fit labels.

        Translates what the data base provides (the
        record) into what we want displayed/printed.
        Takes a record returned by csv.reader.
        Returns an array of strings. The length of the array
        (padded with empty strings as necessary) will match 
        self.params.n_lines_per_label.
        Formats the csv fields, splitting fields into more than
        one line as necessary to remain within constraints.
        Returns None and prints a warning if unable to remain within
        constraints.
        """
        res = []
        lines = []
        # Specify the three fields we want for the label:
        lines.append("{} {}".format(
            record[self.i_first], record[self.i_last]))
        lines.append("{}".format(record[self.i_address]))
        lines.append("{} {} {}" .format(
            record[self.i_town],
            record[self.i_state],
            record[self.i_zip_code]))
        for line in lines:  # Deal with long lines:
            new_lines =  self.prn_split(line, self.params)
            if new_lines:
                res.extend(new_lines)
            else:
                print(
                    "## Unable to process line...")
                print(line)
                print("... in the following record...")
                print(record)
                print("... so it will not be reflected in output!.")
                return
        if len(res) > self.params.n_lines_per_label:
            print("## Following record is too long...")
            for line in lines:
                print("\t{}".format(line))
            return
        n_fields = len(res)
        if n_fields <  self.params.n_lines_per_label:
            n_empty_lines = self.params.n_lines_per_label - n_fields
            n_bottom_blanks = n_top_blanks = n_empty_lines // 2
            n_top_blanks += n_empty_lines % 2
            res = (
                [self.params.empty_line] * n_top_blanks + 
                res + 
                [self.params.empty_line] * n_bottom_blanks
                )
        return res

    def print_custom_envelopes(self, source_file):
        """
        Gets names and addresses from <source_file>
        and "prints" custom envelopes. Wether it goes to printer,
        stdout, or a file is determined by args["<outfile>"].
        NOTE: This code is no longer in use and is expected to be
        redacted completely.
        """
        record_reader = csv.reader(
            codecs.open(source_file, 'rU', 'utf-8'),
            dialect='excel')

        while True:
            try:
                next_record = next(record_reader)
            except StopIteration:
                break
            fields = self.get_fields(next_record)
#           print("fields INITIALLY: {}".format(fields))
            fields = [""] * self.params.top_margin + fields
#           print("fields AFTER format: {}".format(fields))
            for_printer = "\n".join(fields)
            output(for_printer)
#           print(for_printer)
#           _ = input("Enter to continue.")

####  End of Club class declaration.


def ck_fields_cmd():
    """
    Traverses the input file using
    Club method add2malformed
    to select malformed records.
    """
    club = Club(Dummy)
    ret = []
    club.malformed = []
    club.status_list = []
    infile = args["-i"]
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    print("Checking fields...")
    err_code = member.traverse_records(infile,
                (member.add2malformed, member.add2status_list),
                club)
    if err_code:
        print("Error condition! #{}".format(err_code))
    if not club.malformed:
        ret.append("No malformed records found.")
    else:
        if not args['--raw']:
            ret = [
                'Malformed Records',
                '================='] + club.malformed
    if args["-S"]:
        ret.extend(["", "Members /w 'status' Content",
                       '---------------------------']
                       + club.status_list)
    output("\n".join(ret))
##  'output' function reports file manipulation 
##  making the following two lines redundant:
#   if args['-o']:
#       print("Output sent to {}.".format(args['-o']))
    print("...done checking fields.")

def compare_gmail_cmd():
    """
    Reports inconsistencies between the clubs membership list
    and the google csv file (exported gmail contacts.)
    """

    verification = "Is your google contacts cvs file up to date? "
    if verification and input(verification).lower()[0] == 'y':
        club = Club(Dummy)
        if not args["-i"]:
            args["-i"] = Club.MEMBERSHIP_SPoT
        if  not args['<gmail_contacts>']:
            args['<gmail_contacts>'] = CONTACTS 
        print("File from google: '{}'"
            .format(args['<gmail_contacts>']))
        return club.compare_gmail(args['-i'],
                                args['<gmail_contacts>'],
                                args['-s'])
    else:
        print(
            "Best do a Google Contacts export and then begin again.")
        sys.exit()

def show_cmd():
    club = Club(Dummy)
    club.members = []
    club.nmembers = 0
    club.inductees = []
    club.ninductees =0
    club.applicants = []
    club.napplicants = 0
    club.errors = []
    club.by_n_meetings = {}
    infile = args["-i"]
    if not infile:
        infile = club.infile
    print("Preparing membership listings...")
    err_code = member.traverse_records(infile,
                                (member.add2memlist4web,
                                member.is_applicant),
                                club)
    print("...done preparing membership listing...")
    listing4web = ["""FOR MEMBER USE ONLY

THE TELEPHONE NUMBERS, ADDRESSES AND EMAIL ADDRESSES OF THE BOLINAS
ROD & BOAT CLUB MEMBERSHIP CONTAINED HEREIN IS NOT TO BE REPRODUCED
OR DISTRIBUTED FOR ANY PURPOSE WITHOUT THE EXPRESS PERMISSION OF THE
BOARD OF THE BRBC.
LOSS OF MEMBERSHIP IS THE PENALTY.
    """]
    if club.members:
        listing4web.extend(("Club Members ({} in number as of {})"
                .format(club.nmembers, helpers.date),
                            "============"))
        listing4web.extend(club.members)
    if club.applicants:
        listing4web.extend(("", "Applicants ({} in number)"
                .format(club.napplicants),
                                "=========="))
        if club.by_n_meetings:
            sorted_keys = sorted(
                [key for key in club.by_n_meetings.keys()])
            for key in sorted_keys:
                listing4web.append("{}".format(key))
                listing4web.append("--")
                sorted_applicants = sorted(club.by_n_meetings[key])
                listing4web.extend(sorted_applicants)
        else:
            listing4web.extend(club.applicants)
        if club.ninductees:
            listing4web.extend(("", "Inductees ({} in number)"
                    .format(club.ninductees),
                                    "========="))
            listing4web.extend(club.inductees)
    if club.errors:
        listing4web.extend(("", "ERRORS",
                                "======"))
        listing4web.extend(club.errors)

    output("\n".join(listing4web))
    print("...results sent to {}.".format(args['-o']))

def stati_cmd():
    club = Club(Dummy)
    infile = args["-i"]
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    print("Preparing listing of stati.")
    club.m_by_status = {}
    err_code = member.traverse_records(infile,
                                    member.add2m_by_status,
                                    club)
    res = ["No entries found.", ]
    keys = [k for k in club.m_by_status.keys() if k]
    keys.sort()
    if args["-B"]:
        if "be" in keys:
            for value in club.m_by_status["be"]:
                res.append("    {}".format(value))
            if len(res) > 1:
                res[0] = ("Those with bad emails:" +
                        "\n======================")
    elif args["-W"]:
        if "w" in keys:
            for value in club.m_by_status["w"]:
                res.append("    {}".format(value))
        if len(res) > 1:
            res[0] = ("Those whose fees are being waived:" +
                    "\n==================================")
    elif args["-A"]:
        for key in keys:
            if key.startswith('a'):
                res.append("  {}".format(member.status_key_values[key]))
                for value in club.m_by_status[key]:
                    res.append("    {}".format(value))
        if len(res) > 1:
            res[0] = "Applicants:\n==========="
    else:
        for key in keys:
#           print("key is: {}".format(key))
#           print("value is: {}".format(club.m_by_status[key]))
            res.append("\n{}".format(
                        member.status_key_values[key]
                                    ))
            for value in club.m_by_status[key]:
                res.append("\t{}".format(value))
            if len(res) > 1:
                res[0] = "Stati:\n==========="
    res = "\n".join(res)
    output(res)
#   outfile = args["-o"]
#   with open(outfile, 'w') as file_obj:
#       file_obj.write(res)
    print("\n... listing sent to {}.".format(args["-o"]))

def extra_charges(infile, json_file=None):
    """
    A helper function:
    Used by extra_charges_cmd when infile is a txt file.
    Returns a string: a table of charges.
    Also writes data to a json file if a file name is specified.
    """
    json_dict = {}
    dock_usage = []
    mooring = []
    kayak_storage = []
    uninterpretable = []
    n_longest = 0
    res = []

    with open(infile, "r") as f_obj:
        print('Reading from "{}".'.format(f_obj.name))
        for line in f_obj:
            line = line.strip()
            if not line or line[0] == '#':
                continue
            if 'Mooring' in line:
                current = mooring
                key = "Mooring"
            elif 'Dock' in line:
                current = dock_usage
                key = "Dock usage"
            elif 'Kayak' in line:
                current = kayak_storage
                key = "Kayak storage"
            else:
                split_line = line.split()
                if len(split_line) == 3:
                    first = split_line[0]
                    last = split_line[1][:-1] #delete colon
                    amt = int(split_line[2])
                    new_line = "{}, {}: ${}".format(last, first, amt)
                    new_val = [last, first, amt]
                    json_dict.setdefault(key, [])
                    json_dict[key].append(new_val)
                    current.append(new_line)
                else:
                    uninterpretable.append(line)

    if len(dock_usage) > n_longest:
        n_longest = len(dock_usage)
    if len(mooring) > n_longest:
        n_longest = len(mooring)
    if len(kayak_storage) > n_longest:
        n_longest = len(kayak_storage)
    final = (
            ["Dock Usage", "----------"] + [""] * n_longest,
            ["Mooring", "-------"] + [""] * n_longest,
            ["Kayak Storage", "-------------"] + [""] * n_longest
            )
    for i in range(n_longest):
        try:
            final[0][i+2] = dock_usage[i]
            final[1][i+2] = mooring[i]
            final[2][i+2] = kayak_storage[i]
        except IndexError:
            pass

    res = ['',
           "Members Paying Fees For Extra Privileges",
           "========================================",]
    for i in range(n_longest + 1):
        res.append("{:<25} {:<25} {:<25}"
            .format(final[0][i], final[1][i], final[2][i]))
    if json_file:
        lines = ["{"]
        keys = [key for key in json_dict.keys()]
        keys.sort()
        for key in keys:
            lines.append('"{}": ['.format(key))
            for item in json_dict[key]:
                lines.append('    ["{}", "{}", {}],'
                    .format(*item))
            lines[-1] = lines[-1][:-1]
            lines.append('    ],')
        lines[-1] = lines[-1][:-1]
        lines.append('}')
        with open(json_file, 'w') as jfile:
            jfile.write('\n'.join(lines))
            print("Wrote JSON data to {}.".format(jfile.name))
    return '\n'.join(res)


def usps_cmd():
    """
    Generates a cvs file used by Peter to send out minutes.
        first,last,address,town,state,postal_code
    (Members who are NOT in the 'email only' category.)
    Note: Peter (secretary) is purposely NOT 'email_only' so that he
    can get a copy of the printed minutes for inspection.
    """
    infile = args['-i']
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    club = Club(Dummy)
    club.usps_only = []
    err_code = member.traverse_records(infile, member.get_usps, club)
    header = []
    for key in club.fieldnames:
        header.append(key)
        if key == "postal_code":
            break
    res = [",".join(header)]
    res.extend(club.usps_only)
    return '\n'.join(res)
        

def extra_charges_cmd():
    """
    Returns a report of members with extra charges.
    Examines the infile and if it's a csv file, the membership file
    is assumed and report will be from there.

    If infile is a txt file: membership data is not consulted;
    instead we assume the file is in the format of "extra_fees.txt"
    which is the SPoT[1] identifying members who pay for extra
    privileges (mooring, dock usage and kayak storage) along with
    how much they pay.  Using it as input, this command creates a
    table showing members who pay for these extra privileges.

    It also can create a json file: specified by the -j option.
    Such a json file is required by the restore_fees command.

    [1] Single Point of Truth
    """
    infile = args["-i"]
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    suffix = infile[-4:]
    if suffix == ".txt":
        # use function vs method
        res = extra_charges(infile, args["-j"])
        print("Sending output to '{}'.".format(args["-o"]))
        output(res)
        sys.exit()
    elif  suffix == ".csv":
        # use methods: traversal with get_extra_fees
        print("Traversing {} to select mempbers owing extra_fees..."
            .format(infile))
        club = Club(Dummy)
        club.extras_by_member = []
        club.extras_by_category = {}
        club.errors = []
        for key in member.fees_keys:
            club.extras_by_category[key] = []
        err_code = member.traverse_records(infile,
                member.get_extra_charges, club)
    else:
        print("Bad input file!")
        assert False
    res_by_category = []
    if club.extras_by_category:
        res_by_category.extend(["Extra Fees Charged by the Club",
                                "=============================="])
        for key in club.extras_by_category:
            if club.extras_by_category[key]:
                res_by_category.append("")
                res_by_category.append("Members paying for {}"
                    .format(key))
                res_by_category.append("-" * len(
                        res_by_category[-1]))
                for val in club.extras_by_category[key]:
                    res_by_category.append(val)
        res_by_category = '\n'.join(res_by_category)
    else:
        res_by_category = ''
    res_by_member = []
    if club.extras_by_member:
        res_by_member.extend(["Members Paying Extra Fees",
                              "========================="])
        for line in club.extras_by_member:
            res_by_member.append(line)
        res_by_member = '\n'.join(res_by_member)
    else:
        res_by_member = ''
    output("\n\n".join((res_by_category, res_by_member)))
    if club.errors:
        print("Errors:")
        print("\n".join(club.errors))

def payables_cmd():
    """
    Traverses the db populating 
    """
    infile = args['-i']
    if not infile:
        infile = Club.MEMBERSHIP_SPoT
    club = Club(Dummy)
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
    Usage:
  ./utils.py prepare_mailing --which <letter> [--lpr <printer> -i <infile> -j <json_file> --dir <dir4letters>]

    "--which <letter>" must be set to one of the keys found in 
    content.content_types.
    Depending on the above, this command will also need to assign
    attributes to the Club instance to collect "extra_data".

    Should be able to replace all the various billing routines as well
    as provide a general mechanism of sending out notices.
    Accompanying module 'content' provides support.
    """
    import content
    club = Club(Dummy)
    club.which = content.content_types[args["--which"]]
    club.lpr = content.printers[args["--lpr"]]
    club.email = content.prepare_email(club.which)
    club.letter = content.letter_format(club.which, 
                                        args["--lpr"])
#   print("Preparing mailing: '{}'".format(club.which))
    if not args["-i"]:
        args["-i"] = club.MEMBERSHIP_SPoT
    if not args["-j"]:
        args["-j"] = club.JSON_FILE_NAME4EMAILS
    club.json_file_name = args["-j"]
    if not args["--dir"]:
        args["--dir"] = club.MAILING_DIR
    club.dir4letters = args["--dir"]
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
    member.prepare_mailing(args["-i"], club)
    # need to move the json_data to the file
#   if club.json_data:
#       with open(club.json_file_name, 'w') as f_obj:
#           json.dump(club.json_data, f_obj)
#           print('JSON dumped to "{}".'.format(f_obj.name))

def display_emails_cmd(json_file):
    with open(json_file, 'r') as f_obj:
        print('Reading JSON file "{}".'.format(f_obj.name))
        records = json.load(f_obj)
    all_emails = []
    for record in records:
        email = []
        recipients = ', '.join(record[0])
        email.append(">>: " + recipients)
        email.append(record[1])
        email.append('\n')
        all_emails.append("\n".join(email))
    print("Processed {} emails..."
        .format(len(all_emails)))
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
    and lowering the gmail account security setting:
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
    for datum in data:
        if message:
            recipients = datum
            content = message
        else:
            recipients = datum[0]
            content = datum[1]
        counter += 1
        print("Sending email #{} to {}."
            .format(counter, ", ".join(recipients)))
        smtp_send(recipients, content)
        # Using random number to decrease liklyhood that mailing
        # entity (Gmail) will think it's a 'bot' sending the emails.
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
    club = Club(Dummy)
    if not args["-i"]:
        args["-i"] = club.MEMBERSHIP_SPoT
    with open(args["-c"], "r") as content_file:
        print('Reading content from "{}".'.format(content_file.name))
        club.content = content_file.read()
    err_code = member.traverse_records(args["-i"],
        club.send_attachment)

def restore_fees_cmd():
    """
    Assumes the dues paying season is over and all dues and fees
    fields have been zeroed out (either because members have paid or
    been dropped from the club roster.)
    Repopulates the club's master list with the ANNUAL_DUES constant
    and information from args['<extra_fees.json>'].
    If '-t <new_membership_file>' is specified, the original
    membership file is not modified and output is to the new file,
    else the original file is changed.
    """
    club = Club(Dummy)
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
    club = Club(Dummy)
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
            print('Writing to "{}".'.format(file_obj))
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

def mutt_send(recipient, subject, body, attachment=None):
    """
    Does the mass e-mailings with attachment
    if one is provided.
    """
    cmd_args = [ "mutt", "-F", args["-F"], ]
    if attachment:
        cmd_args.extend([ "-a", attachment])
    cmd_args.extend([
        "-s", "{}".format(subject),
        "--", recipient
        ])
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE, 
        input=body, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))

not_used = """
cmds = dict(
    ck_fields = ck_fields_cmd,
    show = show_cmd,
    compare_gmail = compare_gmail_cmd,
    stati = stati_cmd,
    extra_charges = extra_charges_cmd,
    payables = payables_cmd,
    usps = usps_cmd,
    prepare_mailing = prepare_mailing_cmd,
    send_emails = send_emails_cmd,
    print_letters = print_letters_cmd,
    restore_fees = restore_fees_cmd,
    display_emails = display_emails_cmd,
    fees_intake = fees_intake_cmd,
    labels = labels_cmd,
    envelopes = envelopes_cmd,
    show_mailing_categories = show_mailing_categories_cmd,
    )
"""

if __name__ == "__main__":
#   print(args)

    if args["?"]:
        doc_lines = __doc__.split('\n') 
        print('\n'.join(doc_lines[
            (BLANK_LINE_ABOVE_USAGE - TOP_QUOTE_LINE_NUMBER)
            :
            (BLANK_LINE_ABOVE_OPTIONS - TOP_QUOTE_LINE_NUMBER + 1)
            ]))

    elif args["ck_fields"]:
        ck_fields_cmd()

    elif args["compare_gmail"]:
        print("Check the google list against the membership list.")
        output(compare_gmail_cmd())

    elif args["show"]:
        show_cmd()

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
