#!/usr/bin/env python3

# File: labels.py

"""
Prints labels getting data from a csv file exported from a spread
sheet.  
"""

import csv
import codecs
import sys

# First specify where the output is to go:
output_file = 'output.tmp'
# May eventually have this specified as a command line argument.

# Specify labels being used.
# Can set up a class for each brand of labels encountered.
# These classes need never be instantiated.
# They are used only to maintain a set of constants.

class A5160(object):
    """
    Avery 5160 labels  3 x 10 grid
    zero based:
        1, 28, 56
        3, 9, 15, 21, 27, 33, 39, 45, 51, 57
        (max content 5 lines of 25 characters each)
    Uses "letter size" blanks.
    BUT: there was a complication- my printer does an unrequested line
    feed if a line exceeds 80 characters!
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

label = A5160

# Specify input file and its data:
class Source(object):
    """
    Create such an object not only for each data base used but also
    for each way the data of that data base is being displayed.
    """
    # define the fields available:
    i_first= 0
    i_second = 1
    i_address1 = 2
    i_City = 3
    i_State = 4
    i_Zip = 5
    i_email = 6
    i_emailOnly = 7
    i_Dock = 8
    i_Mooring = 9
    i_Kayak = 10

    def __init__(self, label):
        """
        Each instance must know the format
        of the labels to be used.
        """
        self.label = label
        self.label.self_check()


    def prn_split(self, field, criteria):
        """
        <field> is a string and if its length is within the limit set
        by criteria.n_chars_per_field, it is returned in a singleton array.
        If len(field) is greater than the limit, more than the one string
        is returned, each within that limit.
        Returns None and prints an error message if any word in field is
        longer than the specified limit.
        Returned strings are always criteria.n_chars_per_field long:
        left based if the beginning of a field,
        right based if constituting the 'overflow.'
        'criteria' must have attributes 'left_formatter' and
        'right_formatter' as well as 'n_chars_per_field'
        """
        if len(field) > criteria.n_chars_per_field:
    #       print("field is {} chars long".format(len(field)))
            words = field.split()
            for word in words:
                if len(word) > criteria.n_chars_per_field:
                    print("# Unable to process the following field...")
                    print(field)
                    print("...because has word(s) longer than {}."
                        .format(criteria.n_chars_per_field))
                    return
    #       print("field is split into {}".format(words))
            format_left = True
            ok_lines = []
            line = []
            for word in words:
                line.append(word)
                if len(" ".join(line)) > criteria.n_chars_per_field:
                    ok = " ".join(line[:-1])
                    if format_left:
                        ok_lines.append(
                            criteria.left_formatter.format(ok))
                        format_left = False
                    else:
                        ok_lines.append(
                            criteria.right_formatter.format(ok))
                    line = [word, ]
            if line:
                ok = " ".join(line)
                ok_lines.append(criteria.right_formatter.format(ok))
            return ok_lines
        else:
            return [criteria.left_formatter.format(field), ]

    def get_fields(self, csv_record):
        """
        Translates what the data base provides (the
        csv_record) into what we want displayed/printed.
        Takes a record returned by csv.reader.
        Returns an array of strings. The length of the array
        (padded with empty strings as necessary) will match 
        self.label.n_lines_per_label.
        Formats the csv fields, splitting fields into more than
        one line as necessary to remain within constraints.
        Returns None and prints a warning if unable to remain within
        constraints.
        """
        res = []
        lines = []
        # Specify the three fields we want for the label:
        lines.append("{} {}".format(
            csv_record[self.i_first], csv_record[self.i_second]))
        lines.append("{}".format(csv_record[self.i_address1]))
        lines.append("{} {} {}" .format(
            csv_record[self.i_City],
            csv_record[self.i_State],
            csv_record[self.i_Zip]))
        for line in lines:  # Deal with long lines:
            new_lines =  self.prn_split(line, label)
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
        if len(res) > self.label.n_lines_per_label:
            print("## Following record is too long...")
            for line in lines:
                print("\t{}".format(line))
            return
        n_fields = len(res)
        if n_fields <  self.label.n_lines_per_label:
            n_empty_lines = self.label.n_lines_per_label - n_fields
            n_bottom_blanks = n_top_blanks = n_empty_lines // 2
            n_top_blanks += n_empty_lines % 2
            res = (
                [self.label.empty_line] * n_top_blanks + 
                res + 
                [self.label.empty_line] * n_bottom_blanks
                )
        return res


    def get_data2print(self, source_file):
        """
        Returns a text file ready to be sent to a printer.
        See comments about plans to change this behavior.
        """

        record_reader = csv.reader(
            codecs.open(source_file, 'rU', 'utf-8'),
            dialect='excel')
        pages = []
        quit = False
            
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
        while True:
            # deal with one page at a time:
            page = []

            # put empty lines at top of page:
            for _ in range(self.label.top_margin):
                page.append("")
            # set up all the rows in the page:
            for _ in range(self.label.n_rows_per_page):
                # add a row at a time:
                row_of_data = []
                # collect records to fill a row:
#               print("Collect records to fill a row:)")
                while len(row_of_data) < self.label.n_labels_per_row:
                    try:
#                       print("About to 'next(record_reader)'")
                        next_record = next(record_reader)
#                       print("Just did  'next(record_reader)'")
                    except StopIteration:
#                       print("StopIteration")
#                       _ = input("Enter to continue")
                        next_record = None
                        quit = True
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
                        row_of_data.append(label.empty_label)
#                   print("len(row_of_data) is {}"
#                       .format(len(row_of_data)))
                # We have a row of records but we
                # want columns of record fields:
                for j in range(self.label.n_lines_per_label):
                    # the next set of lines
                    line_components = []
                    for i in range(self.label.n_labels_per_row):
                        line_components.append(row_of_data[i][j])
                    line = ""
                    for l in range(self.label.n_labels_per_row):
                        line = (line +
                            " " * self.label.separation[l] + 
                            line_components[l])
                    line = line.rstrip()
                    if len(line) > self.label.n_chars_wide:
                        original = line
                        line = line[:self.label.n_chars_wide]
                        print("Too long a line...")
                        print(original)
                        print("...is being stripped to:")
                        print(line)
                    page.append(line)

            deal_with_page(page)
            if quit:
                break
        print("{} pages ready to print".format(len(pages)))
        return "\f".join(pages) 


if __name__ == "__main__":
    source = Source(label)
#   source_file = './Jan18TotalLIST.csv'
    source_file = '../Lists/membership.csv'
    data = source.get_data2print(source_file)
#   print(data, end='')
    with open(output_file, 'w') as fileobj:
        fileobj.write(data)

still_to_consider_doing = """
    use docopt to allow versioning AND
    to use command line arguments to specify
    1. input file (provide file name as argument)
    2. out put => 
        a. stdout
        b. printer
        c. file (provide file name as argument)

    Modify get_fields and the way it is used so that records that
    won't fit onto a label are left out (with a warning provided)
    rather than causing the program to abort.
"""
