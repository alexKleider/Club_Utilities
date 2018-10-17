#!/usr/bin/env python3

# File: utils.py

"""
"utils.py" is a utility providing functionality for usage and
maintanance of the Bolinas Rod and Boat Club records.
Most commands deal with a csv file named "memlist.csv" so for
these it is the default input file.
Consult the README file for further info.

Usage:
  ./utils.py [ ? | --help | --version ]
  ./utils.py ck_fields [-r -i <infile> -o <outfile>]
  ./utils.py compare_gmail [<gmail_contacts> -r -i <infile> -s <sep> -j <json> -o <outfile>]
  ./utils.py show [-r -i <infile> -o <outfile> ]
  ./utils.py usps [-i <infile> -o <outfile>]
  ./utils.py extra_charges [--raw -i <infile> -o <outfile>]
  ./utils.py payables [-i <infile>] -o <outfile>
  ./utils.py billing [-i <infile> -o arrears_file -l]  -j <json_file> --dir <dir4letters>
  ./utils.py prepare_mailing [-i <infile> -l] -j <json_file> --dir <dir4letters>
  ./utils.py send_emails [<content>] -j <json_file>
  ./utils.py print_letters --dir <dir4letters> [-s <sep> -e error_file]
  ./utils.py restore_fees [<membership_file> -j <json_fees_file> -t <temp_membership_file> -e <error_file>]
  ./utils.py display_json -j <json_file> [-o <txt_file>]
  ./utils.py fees_intake [-i <infile> -o <outfile> -e <error_file>]
  ./utils.py (labels | envelopes) [-i <infile> -p <params> -o <outfile> -x <file>]
  ./utils.py email_billings2json [-i <infile>] -j <json_file>
  ./utils.py usps_billings2print [-i <infile>] --dir <dir4letters>

Options:
  -h --help  Print this docstring.
  --version  Print version.
  --dir <dir4letters>  The directory to be created and/or read
                      containing letters for batch printing.
  -e <error_file>  Specify name of a file to which an error report
                    can be written.  If not specified, errors are
                    generally reported to stdout.
  -i <infile>  Specify file used as input. Usually defaults to
                memlist.csv (the membership csv file.)
  -j <json>  Specify an output file in jason if -o is otherwise used.
  -l  An option to indicate that all are to get letters, even those
                  with an email address.
  -t <temp_file>  An option provided for when one does not want to risk
                  corruption of an important input file which is to be
                  modified, thus providing an opportunity for proof
                  reading the 'modified' file before renaming it to
                  the original. (Typically named '2proof_read.txt'.)
  -o <outfile>  Specify destination. Choices are stdout, printer, or
                the name of a file. [default: stdout]
  -p <params>  If not specified, the default is
               A5160 for labels & E000 for envelopes.
  -r --raw  Supress headers (to make the output suitable as
            input for 'tabulate.py'.)
  -s <separator>  Some commands may have more than one component to
          their output.  Such componentes can be seprated by either
          a line feed (LF) or a form feed (FF).  [default: FF]
  <gmail_contacts>  [default: google.csv]

Commands:
    When run without a command, prints a usage statement.
    ck_fields: Check for correct number of fields in each record.
        Sends results to -o <outfile> only if there are bad records.
        Use of -r --raw option supresses the header line.
    compare_gmail: Checks the gmail contacts for incompatabilities
        with the membership list. Be sure to do a fresh export of the
        contacts list.  If the -j option is specified, it names the
        file to which to send emails (in JSON format) to members with
        differing emails. (After proof reading, use 'send_emails'.)
    show: Returns membership demographics for display on the web site.
    usps: Creates a csv file containing names and addresses of
        members who receive their Club minutes by post.
    extra_charges: Provides lists of members with special charges.
        Both a list of members each with the charge(s) they pay and
        separate lists for each category of charge. (Dues not
        included.)
        If the <infile> name ends in '.csv' then the/membership main
        data base file is assumed and output will be charges
        outstanding (i.e. owed but still not payed;) if it ends in
        '.txt' then it is assumed to be in the format of the
        "extras.txt" file and output will include all who are paying
        for one or more of the Club's three special privileges. There
        is also the option of creating a json file needed by the
        restore_fees_cmd.
    payables: reports on content of the member data money fields
        providing a listing of those who owe and those who have paid
        in advance.
    billing: Reads the master membership data base (-i <infile>) to
        create emails (into the -o <json_file>) and letters (into
        the -d <dir4letters>.) This command depends on the
        presence of the Formats.content module (Formats.content.py
        file) which can be "edited to suit the season."
        There is the option (-o) of specifying an output file for a
        listing of members still owing.
        This method pretty much elliminates the need for the the
        following 4 commands: labels, envelopes, email_billings2json
        and usps_billings2print.
    prepare_mailing: A general form of the billing command (above.)
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
        specified by the --dir parameter.
    restore_fees: Use this command after all dues and fees have been
        paid- will abort if any are outstanding. Will place the
        results into a file named as a concatination of "new_" and the
        specified membership csv file. One can then mannually check
        the new file and move it if all is well.
    display_json: Provides an opportunity to proof read the emails.
    labels: print labels.       | default: -p A5160  | Both
    envelopes: print envelopes. | default: -p E000   | redacted.
    email_billings2json: prepares billing statements (as a JSON
        string) keyed by email address.  
    usps_billings2print: Creates a directory specified by the argument
        to the --dir option and into this directory places a billing
        statemen for each member who does not have an email address
        on record. If a directory of the specified name already
        exists, it will be over written!
"""
TOP_QUOTE_LINE_NUMBER = 5
BLANK_LINE_ABOVE_USAGE = 11
BLANK_LINE_BELOW_USAGE = 30

TEXT = ".txt"  #| Used by <extra_charges_cmd>
CSV = ".csv"   #| command.
GMAIL_CONTACTS = 'google.csv'

TEMP_FILE = "2print.temp"
SECRETARY = ("Peter", "Pyle")

import os
import shutil
import csv
import codecs
import sys
import time
import json
import subprocess
from docopt import docopt
from helpers import get_datestamp, indent
import Formats

args = docopt(__doc__, version="1.0.1a")
# print(args)

if args["-s"] == "LF":
    args["-s"] = '\n'
else:
    args["-s"] = '\n\f'

if not args["<gmail_contacts>"]:
    args["<gmail_contacts>"] = GMAIL_CONTACTS

SMTP_SERVER = "smtp.gmail.com"

def output(data, destination=args["-o"]):
    """
    Sends data (text) to destination as specified
    by the -o <outfile> command line parameter (which
    defaults to stdout.)
    """
    if destination == 'stdout':
        print(data)
    elif destination == 'printer':
        with open(TEMP_FILE, "w") as fileobj:
            fileobj.write(data)
        subprocess.run(["lpr", TEMP_FILE])
    else:
        print("Writing to {}...".format(destination))
        with open(destination, "w") as fileobj:
            fileobj.write(data)

# Specify characteristics of medium:
# e.g. labels, envelopes, ...
# Can set up a class for each medium.
# These classes need never be instantiated.
# They are used only to maintain a set of constants.

# Template Classes:
# Classes that define parameters pertaining to that onto
# which data is to be printed (i.e. label page, envelope...)
# are named beginning with a letter (A - Avery, E - Envelope, ...)
# followed by a 4 digit number: A5160, E0000, ... .
# Clients typically refer to these as <params>.
# Provided is a Dummy class for use when templates are not required.

class Dummy(object):
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

media = dict(
        e000 = E0000,
        a5160 = A5160,
        )

class Google(object):
    """
    Helps deal with an exported gmail contacts csv file.
    """

    # Record idices:
    i_name = 0  # Name
    i_first = 1 # Given Name
    i_middle = 2 # Middle Name
    i_last = 3  # Family Name
    i_name_suffix = 9  # Name Suffix
    #2  i_additional= 2 # Aditional Name,  #4 Yomi Name
    #5 Given Name Yomi,  #6 Additional Name Yomi,
    #7 Family Name Yomi,  #8 Name Prefix,
    #10 Initials,  #11 Nickname,  #12 Short Name,  #13 Maiden Name,
    #14 Birthday,  #15 Gender,  #16 Location,  #17 Billing Information
    #18 Directory Server,  #19 Mileage,  #20 Occupation, #21 Hobby,
    #22 Sensitivity,  #23 Priority,  #24 Subject,  #25 Notes
    i_groups = 26  # Group Membership
    #27 E-mail 1 - Type
    i_email = 28  # E-mail 1 - Value
    #29 E-mail 2 - Type,  #30 E-mail 2 - Value,  #31 Phone 1 - Type
    #32 Phone 1 - Value,  #33 Organization 1 - Type
    #34 Organization 1 - Name,  #35 Organization 1 - Yomi Name
    #36 Organization 1 - Title,  #37 Organization 1 - Department
    #38 Organization 1 - Symbol,  #39 Organization 1 - Location
    i_job = 40 #Organization 1 - Job Description


# Specify input file and its data:
class Membership(object):
    """
    Create such an object not only for each data base used but also
    for each way the data of that data base is being displayed.
    Functionality that depends on formatting (i.e. one of the
    preceding classes) is provided as methods of this class.
    Other functionalities are provided as independent functions.
    """
    YEARLY_DUES = 100

    # Data bases used:
    MEMBER_DB = 'memlist.csv'               #|  
    EXTRA_FEES = 'extra_fees.txt'           #|  To be used
    CHECKS_RECEIVED = 'checks_received.txt' #|  as defaults.

    # Intermediate &/or temporary files used:
    EXTRA_FEES_JSON = 'extra_fees.json'
    TEMP_MEMBER_DB = 'new_memlist.csv'
    OUTPUT2READ = '2read.txt'       #|
        # the last generally goes to stdout.

    # define the fields available and define a method to set up a
    # dict for each instance:
    i_first = 0
    i_last = 1
    i_phone = 2
    i_address = 3
    i_town = 4
    i_state = 5
    i_zip_code = 6
    i_email = 7
    i_email_only = 8
    i_dues = 9
    i_mooring = 10
    i_dock = 11
    i_kayak = 12

    keys_tuple = ("first", "last", "phone", "address",
        "town", "state", "zip", "email", "email_only",
        "dues", "mooring", "dock", "kayak"
        )
    headers = {
        "dues": "Dues",
        "mooring": "Mooring",
        "dock": "Dock Usage",
        "kayak": "Kayak Storage",
        }
    fees_keys = keys_tuple[10:]
    money_keys = keys_tuple[9:]

    n_fields_per_record = 13

    def __init__(self, params):
        """
        Each instance must know the format
        of the media. i.e. the parameters.
        """
        self.infile = Membership.MEMBER_DB
        self.params = params
        self.params.self_check()
        self.malformed = []
        self.errors = []
        self.first_letter = '_'
        self.name_tuple = ('','')  # Used by get_malformed method.
        self.name_tuples = []
        self.list4web = []
        self.extras_by_member = []
        self.extras_by_category = {}
        for key in self.fees_keys:
            self.extras_by_category[key] = []
        self.still_owing = []
        self.advance_payments = []
        self.usps_only = []
        self.json_emails = []
        self.dir4letters = ''

        self.invalid_lines = []
        self.n_members = 0

    # Planning to create 'get' methods that will expect to be given a
    # single record as parameter and will collect data into an
    # attribute named accordingly. The calling routine can then read
    # the attribute.
    
    def make_dict(self, record):
        """
        Expect that using csf.DictReader will make this method
        redundant.
        """
        return {
            "first": record[self.i_first],
            "last": record[self.i_last],
            "phone": record[self.i_phone],
            "address": record[self.i_address],
            "town": record[self.i_town],
            "state": record[self.i_state],
            "zip": record[self.i_zip_code],
            "email": record[self.i_email],
            "email_only": record[self.i_email_only],
            "dues": record[self.i_dues],
            "mooring": record[self.i_mooring],
            "dock": record[self.i_dock],
            "kayak": record[self.i_kayak],
            }

    def traverse_records(self, infile, custom_funcs, extras = None):
        """
        Traverses <infile> and applies <custom_funcs> to each
        record.  <custom_funcs> can be a single function or a
        list of functions.
        Generally each <custom_func> will leave its results in
        one of the attributes (similarly named.)  These custom funcs
        are generally methods with names beginning in 'get_'.
        # Could wrap this up in a try clause and report an error
        # number to prevent errors from aborting the program.
        """
        if callable(custom_funcs):
            custom_funcs = [custom_funcs]
        with open(infile, 'r') as file_object:
            print("Opening {}".format(infile))
            dict_reader = csv.DictReader(file_object)
            for record in dict_reader:
                for custom_func in custom_funcs:
                    if extras:
                        custom_func(record, **extras)
                    else:
                        custom_func(record)

    def get_malformed(self, record):
        """
        Populate self.malformed.
        Checks that each record has self.n_fields_per_record
        and that the money fields are blank or evaluate to
        an integer.
        """
        name_tuple = ("{}".format(record['last']),
                    "{}".format(record['first']))
        if len(record) != self.n_fields_per_record:
            self.malformed.append("{}, {}"
                .format(record['last'], record['first']))
            for key in self.money_keys:
                value = record[key]
                if not value:
                    res = 0
                else:
                    try:
                        res = int(value)
                    except ValueError:
                        self.malformed.append("{}, {}, {}:{}"
                            .format(record['last'], record['first'],
                            key, value))
        if name_tuple < self.name_tuple:
            self.malformed.append("Record out of order: {0}, {1}"
                .format(*name_tuple))
        self.name_tuple = name_tuple

    def get_memlist4web(self, record):
        """
        Populate self.list4web.
        """
        line = (
    "{first} {last} {phone} {address}, {town}, {state} {zip} {email}"
                .format(**record))
        first_letter = record['last'][:1]
        if first_letter != self.first_letter:
#           print("changing first letter from {} to {}"
#               .format(self.first_letter, first_letter))
            self.first_letter = first_letter
            self.list4web.append("")
        self.list4web.append(line)

    def get_name_tuple(self, record):
        """
        Populates self.name_tuples list.
        """
        self.name_tuples.append(("{}".format(record['last']),
                                "{}".format(record['first'])))

    def get_mailing(self, record):
        """
        """
        pass

    def prn_split(self, field, params):
        """
        <field> is a string and if its length is within the limit set
        by params.n_chars_per_field, it is returned in a singleton array.
        If len(field) is greater than the limit, more than the one string
        is returned, each within that limit.
        Returns None and prints an error message if any word in field is
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

    def get_fields(self, csv_record):
        """
        Translates what the data base provides (the
        csv_record) into what we want displayed/printed.
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
            csv_record[self.i_first], csv_record[self.i_last]))
        lines.append("{}".format(csv_record[self.i_address]))
        lines.append("{} {} {}" .format(
            csv_record[self.i_town],
            csv_record[self.i_state],
            csv_record[self.i_zip_code]))
        for line in lines:  # Deal with long lines:
            new_lines =  self.prn_split(line, self.params)
            if new_lines:
                res.extend(new_lines)
            else:
                print(
                    "## Unable to process line...")
                print(line)
                print("... in the following record...")
                print(csv_record)
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

    def compare_w_google(self, source_file, google_file, separator):
        """
        Checks for incompatibilities between the two files.
        """
        # Determine if we'll be sending emails:
        json_file = args["-j"]
        # In case we are: here's the template:
        email_template = """From: rodandboatclub@gmail.com
To: {}
Subject: Which email is best?

Dear {},
Club records have two differing emails for you:
    "{}" and
    "{}" .
Please reply telling us which is the one you want the club to use.
Thanks in advance,
Membership"""

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
        no_emails_header = "Members without an email address:"
        differing_emails = []
        differing_emails_header = (
            "Differing emails: g-contacts & memlist:")
        # the final output
        ret = []

        # Traverse google.csv => g_dict_e and g_dict_n
        with open(google_file, 'r', encoding='utf-16') as file_obj:
            for line in file_obj:  # ?chanage to using csv module?
                line = line.strip()
#               _ = input(line)
                g_rec = line.split(',')
                first_name = " ".join((
                    g_rec[Google.i_first],
                    g_rec[Google.i_middle],
                    )).strip()
                last_name = " ".join((
                    g_rec[Google.i_last],
                    g_rec[Google.i_name_suffix],
                    )).strip()
                key = g_rec[Google.i_email]
                value = (
                    first_name,
                    last_name,
                    g_rec[Google.i_groups],  # ?for future use?
                    )
                g_dict_e[key] = value
                
                key = (first_name, last_name,)
                value = g_rec[Google.i_email]
                g_dict_n[key] = value
#               _ = input("Key: '{}', Value: '{}'".
#                   format(key, value))
        # We now have two dicts: g_dict_e & g_dict_n
        # One keyed by email: values can be indexed as follows:
        # [0] => first name
        # [1] => last name
        # [2] => colon separated list of groups
        # The other keyed by name tuple: value is email

        # Next we iterate through the member list...
        record_number = 0
        with open(source_file, 'r') as file_obj:
            dict_reader = csv.DictReader(file_obj)
            for record in dict_reader:
                record_number += 1
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
                    if info != g_info[:2]:  # but names don't match so
                        # append to bad_matches..
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
            for i in range(0, len(no_emails), 3):
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
                if json_file:  # append email to send
                    recipients = (g_email, email)
                    content = email_template.format(
                        ', '.join(recipients),
                        " ".join(name),
                        g_email,
                        email)
                    emails2send.append((recipients, content))

        if json_file:
            with open(args["-j"], 'w') as f_obj:
                json.dump(emails2send, f_obj)

        reports_w_names = (
            (bad_matches, "Common emails but names don't match:"),
            (no_emails, no_emails_header),
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
        return separator.join(ret)

    def cust_fees_json(self, record, context = None):
        """
        """
        pass

    def cust_fees_csv(self, record, context = None):
        """
        """
        pass

    def cust_func_welcome(self, record):
        """
        This custom function selects new members as defined by having
        200 in the "dues" field and sends them a welcome letter with a
        request for dues.
        """
        if record['dues'] == '200':
            # assign record["extras"] prn (possibly indenting them)
            record["subject"] = self.content["subject"]
            record["date"] = self.content["date"]
            if record['email']:  # create email and add to json:
                entry = (self.content["email_header"]
                    + self.content["body"]).format(**record)
                self.json_data.append([[record['email']],entry])
            # create letter:
            # possibly doubly indenting the "extras" if present
            entry = (self.content["postal_header"]
                + self.content["body"]).format(**record)
            path2write = os.path.join(self.dir4letters,
                "_".join((record["last"], record["first"])))
            with open(path2write, 'w') as file_obj:
                file_obj.write(entry)


    def csv_file_obj_filter(self, source_file_obj,
                            cust_func, info=None):
        """
        Traverses <source_file_obj> (which is assumed to be a csv
        file conforming to what the <Membership> class expects; i.e.
        what's in 'memlist.csv') applying <cust_func> (which may or
        may not need <info>) to each record.
        Results are made available to the calling routine as
        attributes of <self>.
        """
        pass


    def get_extra_charges(self, record):
        """
        Populates the self.extras_by_member list attribute
        and the self.extras_by_category dict attribute.
        """
        name = "{}, {}".format(record['last'], record['first'])
        _list = []
        for key in ("mooring", "dock", "kayak"):
            value = record[key]
            if value:
                value = int(value)
                _list.append("{}- {}".format(key, int(record[key])))
                self.extras_by_category[key].append("{}: {}- {}"
                    .format(name, key, value))
        if _list:
            self.extras_by_member.append("{}: {}"
                .format(name, ", ".join(_list)))

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
        extras = {}
        for category in extra_fees.keys():
            for value in extra_fees[category]:
                to_add = (translate(category), value[2])
                name_tuple = (value[0], value[1])
                _ = extras.setdefault(name_tuple, [])
                extras[name_tuple].append(to_add)
        return extras

    def create_extra_fees_json(self, extra_fees_txt_file):
        # this functionality is provided by extra_fees.py
        pass


    def restore_fees(self, membership_csv_file,
                        dues, fees_json_file,
                        new_membership_csv_file):
        """
        Dues and relevant fees are applied to each member's record
        in a new_membership_csv_file. It can then be checked before
        renaming.
        Populates <self.errors>, an instance attribute, that can be
        checked by a client procedure.
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
        err_code = self.traverse_records(membership_csv_file,
                    [self.get_name_tuple, self.get_payables])  # vvv
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
            reader = csv.DictReader(file_obj)
            key_list = reader.fieldnames  # Save this for later.
            for record in reader:
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
        print("Done with application of dues and fees...")
        print("...updated membership file is '{}'."
            .format(new_file))

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

    def get_usps(self, record):
        """
        Populates self.usps_only with the following comma separated
        values: first, last, address, town, state, and zip, for each
        member who gets her/his copy of meeting minutes by US Postal
        Service.
        """
        if not record['email_only']:
            self.usps_only.append(
                "{first},{last},{address},{town},{state},{zip}"
                .format(**record))

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

    def prepare_mailing(self, mem_csv_file):
        """
        Iterates through all members in the mem_csv_file applying
        <custom_func> to each.  <custom_func> appends emails to 
        <json_data> and creates entries in the <dir4letters>.
        <content> provides boiler plate info. See Formats/content.py
        module for further info.
        Responsibilities of the caller are as follows:
            Set the following instance attributes:
                content (with date added),
                dir4letters, and set up the directory,
                json_file_name (and set up the file),
                json_data (set to []), 
            Be sure custom_func is also an attribute and set to the
            appropriate function.
        Should be able to replace all the various billing routines as
        well as provide a general mechanism of sending out notices.
        <custom_func> could also assign instance variables if required
        by calling routine. (i.e. self.errors)
        """
        self.traverse_records(mem_csv_file, self.cust_func_welcome)
        with open(self.json_file_name, 'w') as file_obj:
            file_obj.write(json.dumps(self.json_data))
    
    def billing(self, content, source_file,
                    json_file, dir4letters,
                    custom_func):
        """
        Prepares annual billing statements.
        [ i] emails for those with an email address: >> json_file,
        [ii] letters for those without: >> the dir4letters
        where each letter is in its own file named according to the
        member's last_first name.
        If json_file &/or dir4letters already exist(s),
        confirmation to over write is sought and program aborted if
        not obtained.
        The json_file conforms to the format described in the "If
        <content> is not specified" section of the send_emails_cmd
        method's docstring.
        This method depends on the presense of <content>, a mapping
        that can be derived from a module set up for this purpose.
        i.e. "Formats.content.py": from Formats.content import content
        This mapping must provide the following keys: "subject",
        "email_header", "postal_header" and "body", all of which have
        place holders for formatting.
        This method pretty much elliminates the need for the following
        five commands: labels, envelopes, usps, email_billings2json
        and usps_billings2print.
        """
        # Set up the Billings directory for postal letters.
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

        # Check the name of the json output file where emails
        # are to be stored:
        if os.path.exists(json_file):
            print("The file '{}' already exists.".format(json_file))
            response = input("... OK to overwrite it? ")
            if response and response[0] in "Yy":
                os.remove(json_file)
            else:
                print(
            "Without permission, must abort.")
                sys.exit(1)

        # Set up arrays for collection of the emails and errors.
        json_ret = []
        errors = []
        arrears = []

        # Read input and process each member one at a time setting
        # up a dict to populate the format strings in 'content':
        record_reader = csv.reader(
            codecs.open(source_file, 'rU', 'utf-8'),
            dialect='excel')
        for next_record in record_reader:
#           next_record = next_record.strip()
            if (not next_record  # Tollerate a blank line.
                    or next_record[0] == "first"):  # Header line.
                continue
            additional = ['',]
            m = {  # Member data used to populate format strings.
                'subject': content['subject'],
                'last': next_record[self.i_last],
                'first': next_record[self.i_first],
                'address': next_record[self.i_address],
                'town': next_record[self.i_town],
                'state': next_record[self.i_state],
                'postal_code': next_record[self.i_zip_code],
                'email': next_record[self.i_email],
                'extras': custom_func(self.make_dict(next_record)),
                'date': date,
                }
#           print(m['extras'])
#           s = input("yY to continue.. ")
#           if not s or not s[0] in "yY":
#               sys.exit()
#           last = next_record[self.i_last]
#           first = next_record[self.i_first]
#           address = next_record[self.i_address]
#           town = next_record[self.i_town]
#           state = next_record[self.i_state]
#           postal_code = next_record[self.i_zip_code]
#           email = next_record[self.i_email]
            if m["extras"]:
                outstanding = ", ".join(m["extras"])
                m["extras"] = '\n'.join(m["extras"])
                name = m['first'] + ' ' + m['last']
                arrears.append("{:<25} {}".format(
                    name, outstanding))
#           else:
#               m["extras"] = "\nYou're all paid up!"

            # Letter is now set up-
            # We need to create email &/or letter...
            if (True
                and m["extras"]
                ):
#           if m["email"]:  # create email and add to json
                entry = (content["email_header"] .format(**m)
                    + content["body"].format(m["extras"]))
                json_ret.append([[m["email"]], entry])
#               print("Appended to json_ret")
            if (True
                and m["extras"]
                ):
#           else:  # create letter and add to directory
                m["extras"] = indent(m["extras"])
                m["extras"] = indent(m["extras"])
                entry = (
                    content["postal_header"].format(**m)
                    + content["body"].format(m["extras"]))
                entry = indent(entry)
                path2write = os.path.join(dir4letters,
                    "_".join((m['last'], m['first'])))
                with open(path2write, "w") as file_object:
                    file_object.write(entry)
        # Comment out next two lines if don't want json (emails.)
        with open(json_file, 'w') as file_obj:
            file_obj.write(json.dumps(json_ret))
        if arrears and args["-a"]:
            with open(args["-a"], 'w') as file_obj:
                file_obj.write('\n'.join(arrears))
        if errors:
            print("Records that weren't processed:")
            for error in errors:
                print(error)


    def annual_email_billings2json(self, source_file):
        """
        Returns a JSON string representing a dictionary-
        keyed by email addresses,
        each value is the billing statement to go to that address.
        """
        record_reader = csv.reader(
            codecs.open(source_file, 'rU', 'utf-8'),
            dialect='excel')
        ret = []
        errors = []
        while True:
            additional = ['',]
            try:
                next_record = next(record_reader)
            except StopIteration:
                break
            if not next_record:
                continue
            email = next_record[self.i_email]
            if email:
                try:
                    extras = [0 if not i else int(i) for i in
                        next_record[self.i_mooring:self.i_kayak+1]]
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
                fees = sum(extras)
                if not (fees or dues):
                    continue
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
                ret.append([[email], 
                    self.email_billing_letter_format.format(
                        email,
                        first, last,
                        '\n'.join(additional),
                        address, town, state, postal_code,
                        )])
        if errors:
            print("Records that weren't processed:")
            for error in errors:
                print(error)
        return json.dumps(ret)

    def annual_usps_billing2dir(self, source_file, dir4letters):
        """
        Creates (or replaces) <dir4letters> and populates it with
        annual billing statements, one for each member without an
        email addresses on record.
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

    def get_payables(self, record):
        """
        Populates self.still_owing and self.advance_payments.

        Checks record for dues &/or fees. If found,
        positives are added to self.still_owing,
        negatives to self.advance_payments.
        """
        name = "{last}, {first}: ".format(**record)
        line_positive = []
        line_negative = []
        for key in self.money_keys:
            if record[key]:
                amount = int(record[key])
                if amount != 0:
                    if amount > 0:
                        assert amount > 0
                        line_positive.append("{} {}".format(
                            self.headers[key], amount))
                    elif amount < 0:
                        assert amount < 0
                        line_negative.append("{} {}".format(
                            self.headers[key], amount))
                    else:
                        assert False
        if line_positive:
            line = (name + ', '.join(line_positive))
            self.still_owing.append(line)
        if line_negative:
            line = (name + ', '.join(line_negative))
            self.advance_payments.append(line)

    def fees_intake(self, infile=CHECKS_RECEIVED):
        """
        Returns a list of strings: subtotals and grand total.
        Replaces the received_totals.py script.
        Populates self.invalid_lines ....
        (... the only reason it's a class method
        rather than a function or a static method.)
        """
        res = ["Fees taken in to date:"]
        self.invalid_lines = []

        total = 0
        subtotal = 0
        date = ''

        with open(infile, "r") as file_obj:
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
                    amount = int(line[24:27])
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
    def welcome_func(self, member):
        """
        Welcomes new members (those with 200 as dues.)
        """
        pass

####  End of Membership class declaration.


def ck_fields_cmd():
    source = Membership(Dummy)
    infile = args["-i"]
    if not infile:
        infile = source.infile
    print("Checking fields...")
    err_code = source.traverse_records(infile,
                                    source.get_malformed)
    if err_code:
        print("Error condition! #{}".format(err_code))
    if not source.malformed:
        output("No malformed records found.")
#       print("No malformed records found.")
    else:
        if not args['--raw']:
            source.malformed = [
                'Malformed Records',
                '================='] + source.malformed
        output("\n".join(source.malformed))
        if args['-o']:
            print("See malformed records in {}.".format(args['-o']))
    print("...done checking fields.")

def show_cmd():
    source = Membership(Dummy)
    infile = args["-i"]
    if not infile:
        infile = source.infile
    print("Preparing membership listing...")
    err_code = source.traverse_records(infile,
                                source.get_memlist4web)
    print("...done preparing membership listing...")
    output("\n".join(source.list4web))
    print("...results sent to {}.".format(args['-o']))

def extra_charges_cmd():
    """
    Returns a report of members with extra charges.
    Examines the infile and if it's a csv file, the membership file is
    assumed and report will be from there.
    If infile is a txt file: membership data is not consulted;
    instead we assume file is in format of extra_fees.txt.
    """
    infile = args["-i"]
    if not infile:
        infile = Membership.MEMBER_DB
    suffix = infile[-4:]
    if suffix == ".txt":
        # use function vs method
        print("Not implemented- use extra_fees.py script instead.")
        sys.exit()
    elif  suffix == ".csv":
        # use methods: traversal with get_extra_fees
        print("Traversing {} to select mempbers owing extra_fees..."
            .format(infile))
        source = Membership(Dummy)
        err_code = source.traverse_records(infile,
                source.get_extra_charges)
    else:
        assert False
    res_by_category = []
    if source.extras_by_category:
        res_by_category.extend(["Extra Fees Charged by the Club",
                                "------------------------------"])
        for key in source.extras_by_category:
            if source.extras_by_category[key]:
                res_by_category.append("")
                res_by_category.append("Members paying for {}:"
                    .format(source.headers[key]))
                for val in source.extras_by_category[key]:
                    res_by_category.append(val)
        res_by_category = '\n'.join(res_by_category)
    else:
        res_by_category = ''
    res_by_member = []
    if source.extras_by_member:
        res_by_member.extend(["Members Paying Extra Fees",
                              "-------------------------"])
        for line in source.extras_by_member:
            res_by_member.append(line)
        res_by_member = '\n'.join(res_by_member)
    else:
        res_by_member = ''
    return "\n\n".join((res_by_category, res_by_member))

def payables_cmd():
    """
    Traverses the db populating 
    """
    infile = args['-i']
    if not infile:
        infile = Membership.MEMBER_DB
    source = Membership(Dummy)
    err_code = source.traverse_records(infile, source.get_payables)
    output = []
    if source.still_owing:
        output.extend(["Members owing",
                       "-------------"])
        output.extend(source.still_owing)
    if source.advance_payments:
        if source.still_owing:
            output.append("\n")
        output.extend(["Members Payed in Advance",
                       "------------------------"])
        output.extend(source.advance_payments)
    return '\n'.join(output)

def usps_cmd():
    """
    Generates a cvs file used by Peter to send out minutes.
        first,last,address,town,state,zip_code
    (Members who are NOT in the 'email only' category.)
    Note: Peter (secretary) is purposely NOT 'email_only' so that he
    can get a copy of the printed minutes for inspection.
    """
    infile = args['-i']
    if not infile:
        infile = Membership.MEMBER_DB
    source = Membership(Dummy)
    err_code = source.traverse_records(infile, source.get_usps)
    header = [key for key in source.keys_tuple[:source.i_email]]
    res = [",".join(header)]
    res.extend(source.usps_only)
    return '\n'.join(res)

def envelopes_cmd():
    if args["--parameters"]:
        medium = media[args["--parameters"]]
    else:
        medium = E0000
    source = Membership(medium)
    source_file = args["-i"]
    source.print_custom_envelopes(source_file)

def labels_cmd():
    if args["--parameters"]:
        medium = media[args["--parameters"]]
    else:
        medium = A5160
    source = Membership(medium)
    source_file = args["-i"]
    return source.get_labels2print(source_file)

def compare_gmail_cmd():
    """
    Reports inconsistencies between the clubs membership list
    and the google csv file (exported gmail contacts.)
    """

    verification = "Is your google contacts cvs file up to date? "
    if verification and input(verification).lower()[0] == 'y':
        source = Membership(Dummy)
        if not args["-i"]:
            args["-i"] = source.infile
        google_file = args['<gmail_contacts>']
        return source.compare_w_google(args['-i'],
                                google_file, args['-s'])
    else:
        print(
            "Best do a Google Contacts export and then begin again.")
        sys.exit()

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
    source = Membership(Dummy)
    if not args['<membership_file>']:
        args['<membership_file>'] = source.MEMBER_DB
    if not args['-j']:
        args['-j'] = source.EXTRA_FEES_JSON
    if not args['-t']:
        args['-t'] = source.TEMP_MEMBER_DB
    ret = source.restore_fees(
        args['<membership_file>'],
        source.YEARLY_DUES,
        args['-j'],
        args['-t']
        )
    if source.errors and args["-e"]:
        with open(args["-e"], 'w') as file_obj:
            file_obj.write(source.errors)
    if ret:
        sys.exit(ret)

def smtp_file(recipient_email_address, message_file):
    """
    Send email as defined in <message_file>
    to the <recipient_email_address> who will 
    receive this email from the Bolinas Rod and Boat Club.
    Note: Must first lower br&bc's account security at:
    https://myaccount.google.com/lesssecureapps
    """
    cmd_args = ("msmtp", "-a", "gmail", recipient_email_address)
    with open(message_file, 'r') as message:
        subprocess.run(cmd_args, stdin=message)

def smtp_text(recipient_email_address, message):
    """
    Send email as defined in <message_file>
    to the <recipient_email_address> who will 
    receive this email from the Bolinas Rod and Boat Club.
    Note: Must first lower br&bc's account security at:
    https://myaccount.google.com/lesssecureapps
    """
    cmd_args = ("msmtp", "-a", "gmail", recipient_email_address)
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE, 
        input=message, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient_email_address))

def email_billings2json_cmd(infile, json_file):
    source = Membership(Dummy)
    source_file = args["-i"]
    with open(json_file, 'w') as f_obj:
        f_obj.write(
            source.annual_email_billings2json(source_file))

def usps_billings2print_cmd(infile, dir4letters):
    print(
        "using '{}' as input, sending output to the '{}' directory."
            .format(infile, dir4letters))
    source = Membership(Dummy)
    source_file = args["-i"]
    source.annual_usps_billing2dir(source_file, dir4letters)

def billing_cmd():
    source = Membership(Dummy)
    from Formats.content import content
    from Formats.content import custom_func
    # Alternatively, may first run Formats/content.py to create
    # a json file which can then be "load"ed using the json module.
    source.billing(content,
        args["-i"], args["-j"], args["--dir"],
        custom_func)

def prepare_mailing_cmd():
    """
    Should be able to replace all the various billing routines as well
    as provide a general mechanism of sending out notices.
    """
    from Formats.content import content

    source = Membership(Dummy)
    if not args["-i"]:
        args["-i"] = source.MEMBER_DB
    source.content = content
    source.content['date'] = get_datestamp()
    source.dir4letters = args["--dir"]
    source.check_dir4letters(source.dir4letters)
    source.json_file_name = args["-j"]
    source.check_json_file(source.json_file_name)
    source.json_data = []
    source.prepare_mailing(args["-i"])
    # send json_data to file

def fees_intake_cmd():
    infile = args['-i']
    outfile = args['-o']
    errorfile = args['-e']
    source = Membership(Dummy)
    if infile:
        fees_taken_in = source.fees_intake(infile)
    else:
        fees_taken_in = source.fees_intake()
    res = '\n'.join(fees_taken_in)
    if not outfile or outfile == 'stdout':
        print(res)
    else:
        with open(outfile, 'w') as file_obj:
            file_obj.write(res)
    if source.invalid_lines and errorfile:
        with open(errorfile, 'w') as file_obj:
            file_obj.write('\n'.join(source.invalid_lines))
    

def display_emails_cmd1(json_file, output_file=None):
    ret = []
    with open(json_file, 'r') as f_obj:
        data = f_obj.read()
        emails = json.loads(data)
        print("Type 'emails' is '{}'.".format(type(emails)))
    for recipients in emails:
        ret.append(recipients)
        for line in emails[recipients]:
            ret.append(line)
    out_put = "\n".join(ret)
    output(out_put)

def display_emails_cmd(json_file):
    with open(json_file, 'r') as f_obj:
        records = json.load(f_obj)
    all_emails = []
    for record in records:
        email = []
        recipients = ', '.join(record[0])
        email.append(">>: " + recipients)
        email.append(record[1])
        email.append('\n')
        all_emails.append("\n".join(email))
    return "\n".join(all_emails)


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
    cmd_args = ["msmtp", "-a", "gmail"]
    for recipient in recipients:
        cmd_args.append(recipient)
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE, 
        input=message, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))

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
    with open(j_file, 'r') as f_obj:
        data = json.load(f_obj)
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
        time.sleep(30)

def print_letters(dir4letters):
    successes = []
    failures = []
    for letter_name in os.listdir(dir4letters):
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


if __name__ == "__main__":
#   print(args)

    if args["?"]:
        doc_lines = __doc__.split('\n') 
        print('\n'.join(doc_lines[
            (BLANK_LINE_ABOVE_USAGE - TOP_QUOTE_LINE_NUMBER)
            :
            (BLANK_LINE_BELOW_USAGE - TOP_QUOTE_LINE_NUMBER + 1)
            ]))

    elif args["ck_fields"]:
        ck_fields_cmd()

    elif args["show"]:
        show_cmd()

    elif args["extra_charges"]:
        print("Selecting members with extra charges:")
        print("...being sent to {}.".format(args['-o']))
        output(extra_charges_cmd())

    elif args["compare_gmail"]:
        print("Check the google list against the membership list.")
        output(compare_gmail_cmd())

    elif args["labels"]:
        print("Printing labels from '{}' to '{}'"
            .format(args['-i'], args['-o']))
        output(labels_cmd())

    elif args["envelopes"]:
        # destination is specified within Membership 
        # method print_custom_envelopes() which is called 
        # by print_statement_envelopes()
        print("""Printing envelopes...
    addresses sourced from '{}'
    with output sent to '{}'"""
            .format(args['-i'], args['-o']))
        envelopes_cmd()

    elif args["usps"]:
        print("""Preparing a csv file listing
    (first,last,address,town,state,zip_code)
for members who receive meeting minutes by mail.""")
        output(usps_cmd())

    elif args["email_billings2json"]:
        print("Sending JSON data to {}."
            .format(args['-j']))
        email_billings2json_cmd(args['-i'], args['-j'])

    elif args["usps_billings2print"]:
        print("Creating (or replacing) directory '{}'"
            .format(args['--dir']))
        print("and populating it with dues statements for")
        print("members without an email address on record.")
        usps_billings2print_cmd(args['-i'], args['--dir'])
        print("Done creating statements for printing.")

    elif args["billing"]:
        print("Preparing annual billing statements: both email and usps.")
        billing_cmd()
        print("Done with annual billing statements:")
        print("Check emails in '{}' and letters in '{}'."
            .format(args["-j"], args["--dir"]))

    elif args["prepare_mailing"]:
        print("Preparing emails and letters...")
        prepare_mailing_cmd()
        print("...finished preparing emails and letters.")

    elif args["payables"]:
        print("Preparing listing of payables...")
        output(payables_cmd())

    elif args["send_emails"]:
        print("Sending emails...")
        send_emails_cmd()
        print("Done sending emails.")

    elif args["print_letters"]:
        print("Printing letters ...")
        print_letters(args["--dir"])
        print("Done printing letters.")

    elif args['display_json']:
        output(display_emails_cmd(args['-j']))
    
    elif args['restore_fees']:
        restore_fees_cmd()

    elif args['fees_intake']:
        fees_intake_cmd()

    else:
        print("You've failed to select a command.")
        print("Try ./utils.py ? # brief!  or")
        print("    ./utils.py -h # for more detail")

