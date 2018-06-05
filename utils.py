#!/usr/bin/env python3

# File: utils.py

"""
"utils.py" is a utility providing functionality for maintanance
and usage of the Bolinas Rod and Boat Club records. 

Special Note Regarding Emails:
    Generation and sending of emails are done separately through
the use of an intermediary JSON file.  This is done purposely to
encourage proof reading of the emails using the display_json
command before emails are actually sent using the send_emails
command. Here is the suggested sequence:
    ./utils.py compare_gmail google.csv -i memlist.csv -o results -j json2send
    ./utils.py display -i json2send -0 json2check
    vim json2check
    ./utils.py send_emails -i json2send

Usage:
  ./utils.py
  ./utils.py --help | --version
  ./utils.py ck_fields -i <infile> [-o <outfile> -x <file>]
  ./utils.py extra_charges -i <infile> [ -m -d -k  -s <sep> -o <outfile>]
  ./utils.py compare_gmail <gmail_contacts> -i <infile> [-s <sep> -j <json> -o <outfile>]
  ./utils.py (labels | envelopes) -i <infile> [-p <params> -o <outfile> -x <file>]
  ./utils.py usps -i <infile> [-o <outfile>]
  ./utils.py email_billings2json -i <infile> -o <json_file>
  ./utils.py usps_billings2print -i <infile> -b <billings_directory>
  ./utils.py annual_billings -i <infile> -o <json_file> -b <billings_directory>
  ./utils.py send_emails [<content>] -i <json_file>
  ./utils.py display_json -i <json_file> [-o <txt_file>]

Options:
  -h --help  Print this docstring.
  --version  Print version.
  -i <infile>  Specify csv file used as input. (Expected to be a
                membership list of a specific format.)
  -o <outfile>  Specify destination. Choices are stdout, printer, or
                the name of a file. [default: stdout]
  -b <billings_directory>  The directory to be created and into which
                           will be placed billing statements for
                           members without an email address on record.
  -j <json>  Specify an output file in jason if -o is otherwise used.
  -x <log>  Specify a second output file. Useful for logging.
  -p <params>  If not specified, the default is
                               A5160 for labels & E000 for envelopes.
  -m --mooring  List members who have moorings (include the fee.)
  -d --dock  List members with dock privileges (include the fee.)
  -k --kayak  List members who store a kayak (include the fee.)
  -s <sep> --separator=<sep>  Some of the commands have output in
        more than one section. These sections can be separated from 
        one another by either a form feed (ff) (useful if planning to
        send output to a printer) or a double line feed (dlf.)
        [default: dlf]

Commands:
    When run without a command, nothing is done.
    labels: print labels.
    envelopes: print envelopes.
    ck_fields: check for correct number of fields in each record.
    compare_gmail: checks the gmail contacts for incompatabilities
        with the membership list. Be sure to do a fresh export of the
        contacts list.  If the -j option is specified, it names the
        file to which to send emails (in JSON format) to members with
        differing emails in the google contacts and the membership
        list. These can then be proof read before sending them using
        the 'send_emails' command.
    extra_charges: provides lists of members with special charges.
        When none of the optional flags are provide, output is a
        single list of members with the extra charge(s) for each.
        If optional flags are provided, output is a separate list for
        each option specified.
    usps: provides a csv file of members (with their postal addresses)
        who receive minutes by post (rather than email.)
    email_billings2json: prepares billing statements (as a JSON
        string) keyed by email address.  
    usps_billings2print: Creates a directory specified by the argument
        to the -b option and into this directory places a billing
        statemen for each member who does not have an email address
        on record. If a directory of the specified name already
        exists, it will be over written!
    annual_billings: Combines the above two into one command- reads
        the master membership data base (-i <infile>) to create
        emails (into the -o <json_file>) and letters (into the -b
        <billings_dirctory>.)
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
    display_json:  Provides an opportunity to proof read the emails.

"""

TEMP_FILE = "2print.temp"


import os
import shutil
import csv
import codecs
import sys
import pprint
import json
import subprocess
from docopt import docopt

args = docopt(__doc__, version="1.0.0")

if args["--separator"] == "ff":
    SEPARATOR = '\f'
else:
    SEPARATOR = '\n\n'

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
    # define the fields available:
    i_first = 0
    i_last = 1
    i_phone = 2
    i_address = 3
    i_town = 4
    i_state = 5
    i_zip = 6
    i_email = 7
    i_email_only = 8
    i_dues = 9
    i_mooring = 10
    i_dock = 11
    i_kayak = 12

    n_fields_per_record = 13

    email_billing_letter_format = """From: rodandboatclub@gmail.com
To: {}
Subject: Annual Dues and Request for demographics

Dear {} {},

This year the club is attempting to save by sending dues
notices electronically to all for whom we have an email
address on file. Please pop a check into an envelope and
send it on to the club at:

    Bolinas Rod and Boat Club
    PO Box 248
    Bolinas, CA 94924

Your yearly membership fee for the up coming July 1st to June 30th
membership year is $100.
{}

We would also like to verify each member's demographics and (if you
are willing) add a preferred phone number to our data base. Many
members use the membership list on our web page to find contact
information for other members.  Once this is done, we can begin an
update of the membership list that appears on the Club's web site.

Is the following your correct (and preferred) address?
{}, {}, {} {}

Please include a preferred phone number (if you'd like other members
to have access to it) along with your payment of dues.

Thanks in advance,
Alex Kleider, Membership Chair

PS According to Club rules, if not paid by August 1st, the
membership fee goes up to $125. Membership lapses if fees are
not paid by the end of September.  Do it now before you forget!
"""

    usps_billing_letter_format = """

        Bolinas Rod and Boat Club
        PO Box 248
        Bolinas, CA 94924




        {} {}
        {}
        {}, {} {}



        Dear {} {},

            This year the club is attempting to save by sending dues
        notices electronically but unfortunately we do not have your
        email address on file. If you have an email account, please
        let us know so we can add it to the Club data base. Jot it
        down on a piece of paper and send it to us along with your
        membership fee to the Club PO Box given above.

            Your yearly membership fee for the up coming July 1st to
        June 30th membership year is $100.
{}

            We would also like to verify each member's demographics
        and (if you are willing) add a preferred phone number to our
        data base. Many members use the membership list on our web
        page to find contact information for other members.  Once
        this is done, we can begin an update of the membership list
        that appears on the Club's web site.

            Is what appears at the top of this letter your correct
        (and preferred) address?

            Please include a preferred phone number (if you'd like
        other members to have access to it) along with your payment
        of dues.


        Thanks in advance,

        Alex Kleider, Membership Chair

        PS According to Club rules, if not paid by August 1st, the
        membership fee goes up to $125. Membership lapses if fees are
        not paid by the end of September.  Do it now before you forget!
"""

    def __init__(self, params):
        """
        Each instance must know the format
        of the media. i.e. the parameters.
        """
        self.params = params
        self.params.self_check()

    def ck_fields(self, source_file):
        """
        Checks validity of each record in the csv <source_file>
        So far we only check for self.n_fields_per_record.
        """
        print("Checking Fields")
        record_reader = csv.reader(
            codecs.open(source_file, 'rU', 'utf-8'),
            dialect='excel')
        bad = []
        while True:
            try:
                next_record = next(record_reader)
            except StopIteration:
                break
            l = len(next_record)
            if l == self.n_fields_per_record:
                print("OK ", end='')
            else:
                bad.append("{}, {}".format(record[1], record[0]))
        return "\n".join(bad)


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
            csv_record[self.i_zip]))
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

    def compare_w_google(self, source_file, google_file):
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
        record_reader = csv.reader(
            codecs.open(source_file, 'rU', 'utf-8'),
            dialect='excel')
        for next_record in record_reader:
            if next_record[self.i_first] == "first":
                continue
            email = next_record[self.i_email]
            if email:
                # append to names_and_emails as a tuple:
                names_and_emails.append((
                    (next_record[self.i_first],
                    next_record[self.i_last]),
                    email))
                try: # find out if google knows this email:
                    g_info = g_dict_e[email]
                except KeyError:  # if not:
                    # Add to missing_from_google dict...
                    missing_from_google[
                        (next_record[self.i_first],
                        next_record[self.i_last])
                        ] = email
                    # and Append to emails_not_found_in_g...
                    emails_not_found_in_g.append(
                        "{} {} {}"
                        .format(next_record[self.i_first],
                            next_record[self.i_last],
                            email))
                    continue
                # Google knows this email...
                info = (next_record[self.i_first],
                    next_record[self.i_last])
                if info != g_info[:2]:  # but names don't match so
                    # append to bad_matches..
                    bad_matches.append("{} {} {}".format(
                        info, next_record[self.i_email], g_info[:2]))
            else:  # memlist has no email for this member so..
                # append to no_emails:
                no_emails.append("{} {}".format(
                    next_record[self.i_first],
                    next_record[self.i_last]))
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
        return SEPARATOR.join(ret)

    def get_extra_charges(self, source_file):
        """
        Returns a listing of members who have extra charges
        (for mooring, dock usage, and/or kayak storage.)
        """
        def line2append(record, cost):
            return "{} {}:  {}".format(
                record[self.i_first],
                record[self.i_last],
                cost,
                )

        record_reader = csv.reader(
            codecs.open(source_file, 'rU', 'utf-8'),
            dialect='excel')

        ret = []
        all_categories = ["Members with extra charges:",]
        mooring = ["Members paying for a mooring:",]
        dock = ["Members paying for dock privileges:",]
        kayak = ["Members paying for kayak storage:",]
        while True:
            try:
                next_record = next(record_reader)
            except StopIteration:
                break
            try:
                extras = [0 if not i else int(i) for i in
                    next_record[self.i_mooring:]]
                print(extras)
            except ValueError:
                line = "HEADERS: " + ",".join([
                    next_record[self.i_last],
                    next_record[self.i_first],
                    next_record[self.i_email],
                    next_record[self.i_mooring],
                    next_record[self.i_dock],
                    next_record[self.i_kayak],
                    ])
                all_categories.append(line)
                continue
            fees = sum(extras)
            if fees:  # a keeper
                line = ",".join([
                    next_record[self.i_last],
                    next_record[self.i_first],
                    next_record[self.i_email],
                    next_record[self.i_mooring],
                    next_record[self.i_dock],
                    next_record[self.i_kayak],
                    ])
                all_categories.append(line)
                if extras[0]:
                    mooring.append(line2append(next_record,
                        extras[0]))
                if extras[1]:
                    dock.append(line2append(next_record,
                        extras[1]))
                if extras[2]:
                    kayak.append(line2append(next_record,
                        extras[2]))
            else:
                pass  # no action necessary
        if args['--mooring']:
            ret.append(
                "\n".join(mooring))
        if args['--dock']:
            ret.append(
                "\n".join(dock))
        if args['--kayak']:
            ret.append(
                "\n".join(kayak))
        if not (args["--mooring"]
            or args["--dock"]
            or args["--kayak"]):
            return "\n".join(all_categories) 
        return SEPARATOR.join(ret)


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

    def get_USPS_only(self, source_file):
        """
        Selects members who get their copy of meeting minutes
        by US Postal Service. (Members who are NOT in the 'email
        only' category.) Data is presented in csv format consisting
        of the following fields:
            first,last,address,town,state,zip
        """
        record_reader = csv.reader(
            codecs.open(args["-i"], 'rU', 'utf-8'),
            dialect='excel')
        ret = []
        while True:
            try:
                next_record = next(record_reader)
            except StopIteration:
                break
            email_only = next_record[Membership.i_email_only]
            if not email_only:
                entry = (
                    next_record[Membership.i_first],
                    next_record[Membership.i_last],
                    next_record[Membership.i_address],
                    next_record[Membership.i_town],
                    next_record[Membership.i_state],
                    next_record[Membership.i_zip],
                    )
                ret.append(",".join(entry))
        return "\n".join(ret)
    
    def annual_billings(self, source_file,
                        json_file, billing_directory):
        """
        Prepares annual billing statements.
        [ i] emails for those with an email address: >> json_file,
        [ii] letters for those without: >> the billing_directory
        where each letter is in its own file named according to the
        member's last_first name.
        If json_file &/or billing_directory already exist(s),
        confirmation to over write is sought and program aborted if
        not obtained.
        The json_file conforms to the format described in the "If
        <content> is not specified" section of the send_emails_cmd
        function's docstring.
        """
        if os.path.exists(new_directory):
            print("The directory '{}' already exists.")
            response = input("... is it OK to overwrite it? ")
            if response and response[0] in "Yy":
                shutil.rmtree(new_directory)
            else:
                print(
            "Without permission, must abort.")
                sys.exit(1)
        os.mkdir(new_directory)
        if os.path.exists(json_file):
            print("The file '{}' already exists.")
            response = input("... is it OK to overwrite it? ")
            if response and response[0] in "Yy":
                os.remove(json_file)
            else:
                print(
            "Without permission, must abort.")
                sys.exit(1)
        os.mkdir(new_directory)

        json_ret = []
        errors = []

        record_reader = csv.reader(
            codecs.open(source_file, 'rU', 'utf-8'),
            dialect='excel')
        while True:
            try:
                next_record = next(record_reader)
            except StopIteration:
                break
            if not next_record:
                continue
            additional = ['',]
            last = next_record[self.i_last]
            first = next_record[self.i_first]
            address = next_record[self.i_address]
            town = next_record[self.i_town]
            state = next_record[self.i_state]
            postal_code = next_record[self.i_zip]
            email = next_record[self.i_email]
            dues = next_record[self.i_dues]
            if dues:
                dues = int(dues)
            else:
                dues = 0
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
            fees = sum(extras)
            if not (fees or dues):
                continue
            if fees:
                additional.append(
                    "\tIn addition you are being charged for:")
                if extras[0]:
                    additional.append(
                        "\t\tString & Mooring:    ${}"
                            .format(extras[0]))
                if extras[1]:
                    additional.append(
                        "\t\tDock Use:            ${}"
                            .format(extras[1]))
                if extras[2]:
                    additional.append(
                        "\t\tKayak/Canoe Storage: ${}"
                            .format(extras[2]))
                additional.append(
                    "\n\tTotal due: ${}"
                        .format(fees + dues))
                additional.append("\n")
            if email:  # put into json_file
                json_ret.append([[email], 
                    self.email_billing_letter_format.format(
                        email,
                        first, last,
                        '\n'.join(additional),
                        address, town, state, postal_code,
                        )])
            else:  # send letter to directory
                path2write = os.path.join(
                    new_directory, "_".join((last, first)))
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
        with open(json_file, 'w') as file_obj:
            file_obj.write(json.dumps(json_ret))
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
                postal_code = next_record[self.i_zip]
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

    def annual_usps_billing2dir(self, source_file, new_directory):
        """
        Creates (or replaces) <new_directory> and populates it with
        annual billing statements, one for each member without an
        email addresses on record.
        """
        if os.path.exists(new_directory):
            print("The directory '{}' already exists.")
            response = input("... is it OK to overwrite it? ")
            if response and response[0] in "Yy":
                shutil.rmtree(new_directory)
            else:
                print(
            "Without permission, must abort.")
                sys.exit(1)
        os.mkdir(new_directory)
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
                postal_code = next_record[self.i_zip]
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
                    new_directory, "_".join((last, first)))
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

def ck_fields_cmd():
    source = Membership(Dummy)
    source_file = args["-i"]
    return source.ck_fields(source_file)

def extra_charges_cmd():
    """
    Returns a csv report of members with extra charges.
    """
    source = Membership(Dummy)
    source_file = args["-i"]
    return source.get_extra_charges(source_file)

def compare_gmail_cmd():
    """
    Reports inconsistencies between the clubs membership list
    and the google csv file (exported gmail contacts.)
    """

    verification = "Is your google contacts cvs file up to date? "
    if verification and input(verification).lower()[0] == 'y':
        source = Membership(Dummy)
        source_file = args["-i"]
        google_file = args['<gmail_contacts>']
        return source.compare_w_google(source_file, google_file)
    else:
        print(
            "Best do a Google Contacts export and then begin again.")
        sys.exit()

def usps_cmd():
    """
    Generates a cvs file used by Peter to send out minutes.
        first,last,address,town,state,zip
    (Members who are NOT in the 'email only' category.)
    """
    source = Membership(Dummy)
    source_file = args["-i"]
    return source.get_USPS_only(source_file)

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

def usps_billings2print_cmd(infile, output_dir):
    print(
        "using '{}' as input, sending output to the '{}' directory."
            .format(infile, output_dir))
    source = Membership(Dummy)
    source_file = args["-i"]
    source.annual_usps_billing2dir(source_file, output_dir)

def annual_billings_cmd(infile, json_file, billings_directory)
    source = Membership(Dummy)
    source.annual_billings(infile, json_file, billings_directory)

def display_emails_cmd(json_file, output_file=None):
    ret = []
    with open(json_file, 'r') as f_obj:
        emails = json.load(f_obj)
        print("Type 'emails' is '{}'.".format(type(emails)))
    for recipients in emails:
        ret.append(recipients)
        for line in emails[recipients]:
            ret.append(line)
    out_put = "\n".join(ret)
    output(out_put)


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
    spaces!) followed by the text of the email. The "From:" line
    should read as follows:
    "From: rodandboatclub@gmail.com"
    """
    content = args["<content>"]
    j_file = args["-i"]
    message = None
    if content:
        with open(content, 'r') as f_obj:
            message = f_obj.read()
    with open(j_file, 'r') as f_obj:
        data = json.load(f_obj)
    for datum in data:
        if message:
            recipients = datum
            content = message
        else:
            recipients = datum[0]
            content = datum[1]
        smtp_send(recipients, content)


if __name__ == "__main__":
#   print(args)

    if args["ck_fields"]:
        ck_fields_cmd(args["-i"])

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
    (first,last,address,town,state,zip)
for members who receive meeting minutes by mail.""")
        output(usps_cmd())

    elif args["email_billings2json"]:
        print("Sending JSON data to {}."
            .format(args['-o']))
        email_billings2json_cmd(args['-i'], args['-o'])

    elif args["usps_billings2print"]:
        print("Creating (or replacing) directory '{}'"
            .format(args['-b']))
        print("and populating it with dues statements for")
        print("members without an email address on record.")
        usps_billings2print_cmd(args['-i'], args['-b'])
        print("Done creating statements for printing.")

    elif args["annual_billings"]:
        print("Preparing annual billing statements: both email and usps.")
        annual_billings_cmd(args['-i'], args['-o'], args['-b'])
        print("Done with annual billing statements:")
        print("Check emails in '{}' and letters in '{}'."
            .format(json_file, billings_directory))

    elif args["send_emails"]:
        print("Sending emails...")
        send_emails_cmd()
        print("Done sending emails.")

    elif args['display_json']:
        if args['-o']:
            display_emails_cmd(args['-i'], args['-o'])
        else:
            display_emails_cmd(args['-i'])

    else:
        print("You've failed to select a command.")
        print("Try ./utils.py ? # brief!  or")
        print("    ./utils.py -h # for more detail")

