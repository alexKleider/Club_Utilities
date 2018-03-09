#!/usr/bin/env python3

# File: utils.py

"""
-
"utils.py" is a utility providing functionality for maintanance
and usage of the Bolinas Rod and Boat Club records. 

Usage:
  ./utils.py --help | --version
  ./utils.py (labels | envelopes) [-p <params>] -i <infile> [-o <outfile>]
  ./utils.py ck_fields -i <infile> [-o <outfile>]
  ./utils.py compare_gmail [-s <sep>] <gmail_contacts> -i <infile> [-o <outfile>]
  ./utils.py extra_charges [ -m -d -k ] -i <infile>  [-o <outfile>]

Options:
  -h --help  Print this docstring.
  --version  Print version.
  -i <infile>  Specify csv file used as input. (Expected to be a
                membership list of a specific format.)
  -o <outfile>  Specify destination. Choices are stdout, printer, or
                the name of a file. [default: stdout]
  -p <params> --parameters=<params>  If not specified, the default is
                               A5160 for labels & E000 for envelopes.
  -m --mooring  List members who have moorings (include the fee.)
  -d --dock  List members with dock privileges (include the fee.)
  -k --kayak  List members who store a kayak (include the fee.)
  -s <sep> --separator=<sep>  Can choose either a form feed (ff)
                       or a double line feed(dlf.) [default: dlf]

Commands:
    labels: prints labels.
    envelopes: prints envelopes.
    ch_fields: checks for correct number of fields in each record.
    compare_gmail: checks the gmail contacts for incompatabilities
        with the membership list.
    extra_charges: provides lists of members with special charges.
        When none of the optional flags are provide, output is a
        single list of members with the extra charge(s) for each.
        If optional flags are provided, output is a separate list for
        each option specified.
"""

TEMP_FILE = "2print.temp"


import csv
import codecs
import sys
import subprocess
from docopt import docopt

args = docopt(__doc__, version="1.0.0")

if args["--separator"] == "ff":
    SEPARATOR = '\f'
else:
    SEPARATOR = '\n\n'

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
    alternate_indicees = """  ## NOT USED
    i_first = 0  # First Name
    i_ middle = 1  # Middle Name
    i_last = 2  #Last Name
    # 3 Title, 4 Suffix, 5 Initials, 6 Web Page, 7 Gender, 8 Birthday
    # 9 Anniversary, 10 Location, 11 Language, 12 Internet Free Busy
    # 13 Notes
    i_emali = 14  # E-mail Address
    # 15 E-mail 2 Address, 16 E-mail 3 Address, 17 Primary Phone
    # 18 Home Phone, 19 Home Phone 2, 20 Mobile Phone, 21 Pager
    # 22 Home Fax, 23 Home Address, 23 Home Street, 24 Home Street 2
    # 25 Home Street 3, 26 Home Address PO Box, 27 Home City
    # 28 Home State, 29 Home Postal Code, 30 Home Country, 31 Spouse
    # 32 Children, 33 Manager's Name, 34 Assistant's Name
    # 35 Referred By, 36 Company Main Phone, 37 Business Phone
    # 38 Business Phone 2, 39 Business Fax, 40 Assistant's Phone
    # 41 Company, 42 Job Title, 43 Department, 44 Office Location
    i_title = 42
    # 45 Organizational ID Number, 46 Profession, 47 Account
    # 48 Business Address, 49 Business Street, 50 Business Street 2
    # 51 Business Street 3, 52 Business Address PO Box
    # 53 Business City, 54 Business State, 55 Business Postal Code
    # 56 Business Country, 57 Other Phone, 58 Other Fax
    # 59 Other Address, 60 Other Street, 61 Other Street 2
    # 62 Other Street 3, 63 Other Address PO Box, 64 Other City
    # 65 Other State, 66 Other Postal Code, 67 Other Country
    # 68 Callback, 69 Car Phone, 70 ISDN, 71 Radio Phone
    # 72 TTY/TDD Phone, 73 Telex, 74 User 1, 75 User 2, 76 User 3
    # 77 User 4, 78 Keywords, 79 Mileage, 80 Hobby
    # 81 Billing Information, 82 Directory Server, 83 Sensitivity
    # 84 Priority, 85 Private, 86 Categories
"""

    # Record idices:
    i_name= 0  # Name
    i_first= 1 # Given Name
    i_last= 3  # Family Name
    #2  i_additional= 2 # Aditional Name,  #4 Yomi Name
    #5 Given Name Yomi,  #6 Additional Name Yomi
    #7 Family Name Yomi,  #8 Name Prefix,  #9 Name Suffix,
    #10 Initials,  #11 Nickname,  #12 Short Name,  #13 Maiden Name,
    #14 Birthday,  #15 Gender,  #16 Location,  #17 Billing Information
    #18 Directory Server,  #19 Mileage,  #20 Occupation, #21 Hobby,
    #22 Sensitivity,  #23 Priority,  #24 Subject,  #25 Notes
    i_groups= 26  # Group Membership
    #27 E-mail 1 - Type
    i_email= 28  # E-mail 1 - Value
    #29 E-mail 2 - Type,  #30 E-mail 2 - Value,  #31 Phone 1 - Type
    #32 Phone 1 - Value,  #33 Organization 1 - Type
    #34 Organization 1 - Name,  #35 Organization 1 - Yomi Name
    #36 Organization 1 - Title,  #37 Organization 1 - Department
    #38 Organization 1 - Symbol,  #39 Organization 1 - Location
    i_job=40 #Organization 1 - Job Description


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
    i_first= 0
    i_last = 1
    i_address = 2
    i_town = 3
    i_state = 4
    i_zip = 5
    i_email = 6
    i_email_only = 7
    i_mooring = 8
    i_dock = 9
    i_kayak = 10

    def __init__(self, params):
        """
        Each instance must know the format
        of the media. i.e. the parameters.
        """
        self.params = params
        self.params.self_check()


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
        ret = []
        bad_matches = ["Common emails but names don't match:"]
        no_emails = ["Members without emails:", ]
        emails_not_found = [
            "Member emails not found in google contacts:", ]
        # Set up a dict keyed by emails found in the google file.
        g_dict = dict()
        with open(google_file, 'r', encoding='utf-16') as file_obj:
            for line in file_obj:
                line = line.strip()
#               _ = input(line)
                g_rec = line.split(',')
                key = g_rec[Google.i_email]
                value = (
                    g_rec[Google.i_first],
                    g_rec[Google.i_last],
                    g_rec[Google.i_groups],
                    )
                g_dict[key] = value
#               _ = input("Key: '{}, Value: '{}".
#                   format(key, value))
        # We now have a dict keyed by email address with values 
        # which can be indexed as follows:
        # [0] => first name
        # [1] => last name
        # [2] => colon separated list of gorups

#       _ = input(g_dict)
        record_reader = csv.reader(
            codecs.open(source_file, 'rU', 'utf-8'),
            dialect='excel')

        while True:
            try:
                next_record = next(record_reader)
            except StopIteration:
                break
            email = next_record[self.i_email]
            if email:
                try:
                    g_info = g_dict[email]
                except KeyError:
                    emails_not_found.append(
                        "{} {} {}"
                        .format(next_record[self.i_first],
                            next_record[self.i_last],
                            email))
                    continue
                info = (next_record[self.i_first], next_record[self.i_last])
                if info != g_info[:2]:
                    bad_matches.append("{} {} {}".format(
                        info, next_record[self.i_email], g_info))
            else:
                no_emails.append("{} {}".format(
                    next_record[self.i_first],
                    next_record[self.i_last]))
        for report, report_name in (
                (bad_matches, "Bad Matches"),
                (no_emails, "No Emails"),
                (emails_not_found, "Email not found in Contacts")):
            if len(report) > 1:
                formatted_report = "\n".join(report)
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
                extras = [0 if not i else int(i) for i in next_record[8:]]
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
        return "\n\n".join(ret)


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

def print_statement_envelopes():
    if args["--parameters"]:
        medium = media[args["--parameters"]]
    else:
        medium = E0000
    source = Membership(medium)
    source_file = args["-i"]
    source.print_custom_envelopes(source_file)

def get_labels():
    if args["--parameters"]:
        medium = media[args["--parameters"]]
    else:
        medium = A5160
    source = Membership(medium)
    source_file = args["-i"]
    return source.get_labels2print(source_file)

def ck_fields(source_file):
    """
    Checks validity of each record in the csv <source_file>
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
        if l == 11:
            print("OK ", end='')
        else:
            bad.append(next_record)
    for record in bad:
        print("{}, {}".format(record[1], record[0]))

def get_extra_charges():
    """
    Returns a csv report of members with extra charges.
    """
    source = Membership(Dummy)
    source_file = args["-i"]
    return source.get_extra_charges(source_file)

def compare():
    """
    Reports inconsistencies between the clubs membership list
    and the google csv file (exported gmail contacts.)
    """
    source = Membership(Dummy)
    source_file = args["-i"]
    google_file = args['<gmail_contacts>']
    return source.compare_w_google(source_file, google_file)


if __name__ == "__main__":
    print(args)

    if args["ck_fields"]:
        ck_fields(args["-i"])

    elif args["extra_charges"]:
        print("Selecting members with extra charges:")
        print("...being sent to {}.".format(args['-o']))
        output(get_extra_charges())

    elif args["compare_gmail"]:
        print("Check the google list against the membership list.")
        output(compare())

    elif args["labels"]:
        print("Printing labels from '{}' to '{}'"
            .format(args['-i'], args['-o']))
        output(get_labels())

    elif args["envelopes"]:
        # destination is specified within Membership 
        # method print_custom_envelopes() which is called 
        # by print_statement_envelopes()
        print("""Printing envelopes...
    addresses sourced from '{}'
    with output sent to '{}'"""
            .format(args['-i'], args['-o']))
        print_statement_envelopes()

