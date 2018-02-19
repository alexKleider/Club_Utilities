#!/usr/bin/env python3

# File: labels.py

import csv
import codecs
import sys

# First specify where the output is to go:
output_file = 'output.tmp'

# Specify labels being used:
class A5160(object):
    """
    Avery 5160 labels  3 x 10 grid
    zero based:
        1, 28, 56
        3, 9, 15, 21, 27, 33, 39, 45, 51, 57
        (max content 5 lines of 25 characters each)
    Uses "letter size" blanks.
    """

    n_chars_wide = 80
    n_lines_long = 64

    n_labels_per_page = 30
    n_labels_per_row = 3
    n_rows_per_page = n_labels_per_page // n_labels_per_row
    n_lines_per_label = 6

    n_chars_per_field = 25
    #             /------left_margin (spaces before 1st field in row)
    #             |  /----between 1st and 2nd 
    #             |  |  /--between 2nd & 3rd
    #             |  |  |
    #             v  v  v
    separation = (2, 2, 1)
    top_margin = 2

    entries = []
    pages = []

    def __init__(self, data):
        pass

    def show_page(self):
        pass

label = A5160

# Specify input file and its data:
class Source(object):
    """
    Create such an object for each data base used.
    It is also specific as to which components of the
    data base are to be used and how they are to be
    displayed on the labels.
    """

    def __init__(self, label):
        """
        Each instance must know the format
        of the labels to be used.
        """
        self.label = label

    def get_data2print(self, source_file):
        """
        Returns a text file ready to be sent to a printer.
        """

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

        record_reader = csv.reader(
            codecs.open(source_file, 'rU', 'utf-8'),
            dialect='excel')


        max_field_width = 0
        n_top_blanks = 0
        n_bottom_blanks = 0
        records = []

        field_formatter = ("{{:<{}}}"
            .format(self.label.n_chars_per_field))
#       print("field_formatter is assigned '{}'."
#           .format(field_formatter))

        for record in record_reader:
            entry = (
                (field_formatter.format(
                    "{} {}".format(
                        record[i_first], record[i_second]))),
                (field_formatter.format(
                    "{}".format(record[i_address1]))),
                (field_formatter.format(
                    "{} {} {}" .format(
                        record[i_City],
                        record[i_State],
                        record[i_Zip]))))
            for line in entry:
                if len(line) > self.label.n_chars_per_field:
                    long_entry = "\n".join(entry)
                    print("'{}'"
                            .format(long_entry))
                    print(" .. above entry excedes length allowed."
                        + " Can't go on!")
                    sys.exit()
#           print("Appending.. {}".format(entry))
            records.append(entry)
        n_fields = len(records[0])
        if n_fields > self.label.n_lines_per_label:
            print("Datum contains too many rows. Can not go on.")
            sys.exit()
        else:
            n_empty_lines = self.label.n_lines_per_label - n_fields
            n_bottom_blanks = n_top_blanks = n_empty_lines // 2
            n_top_blanks += n_empty_lines % 2
#           print("# of blank lines top and bottom: {} {}"
#               .format(n_top_blanks, n_bottom_blanks))

        # Adjust length of data to be a multiple
        # of self.label.n_labels_per_page 
#       print("starting with {} records".format(len(records)))
        while (len(records) % self.label.n_labels_per_page): 
            records.append(("", "", ""))
#       print("ending with {} records".format(len(records)))
#       _ = input("Enter to continue.")

        pages = []

        # Deal with a page at a time:
        for page_offset in range(0,
            len(records),
            self.label.n_labels_per_page):
            page = []
            n_records = 0
#           print("Page offset is {}".format(page_offset))
        # page_offset is index of first record on page
        # We iterate through records a page full at a time.

            # put empty lines at top of page
            for i in range(self.label.top_margin):
                page.append("")

            # Deal with labels a row at a time:
#           print("Rows per page is {}"
#               .format(self.label.n_rows_per_page))
            for row_offset in range(0,
                self.label.n_labels_per_page,
                self.label.n_labels_per_row):
#               print("Row offset is {}".format(row_offset))

                # Enter the empty top of the labels:
                for i in range(n_top_blanks):
                    page.append("")
                
                # Populate a row of labels  -------

                g = []     # set up a grid
                for i in range(self.label.n_labels_per_row):
#                   print("Appending {}"
#                       .format(
#                           records[page_offset + row_offset + i]))
                    g.append(records[page_offset + row_offset + i])
                    n_records += 1
                for j in range(n_fields):   # the next set of lines
                    line_components = []
                    for i in range(self.label.n_labels_per_row):
                        line_components.append(g[i][j])
                    line = ""
                    for l in range(self.label.n_labels_per_row):
                        line = (line +
                            " " * self.label.separation[l] + 
                            line_components[l])
                    line = line.rstrip()
                    if len(line) > self.label.n_chars_wide:
                        line = line[:self.label.n_chars_wide]
                        print("Too long a line is being stripped to:")
                        print(line)
                    page.append(line)

                # ------ finished populating the row

                # Enter the empty bottom of the labels:
                for i in range(n_bottom_blanks):
                    page.append("")

#           print("Page contains {} records".format(n_records))
            page = '\n'.join(page)
            pages.append(page)
        print("{} pages ready to print".format(len(pages)))
        return "\f".join(pages) 


if __name__ == "__main__":
    source = Source(label)
    source_file = '../Lists/membership.csv'
    data = source.get_data2print(source_file)
#   print(data, end='')
    with open(output_file, 'w') as fileobj:
        fileobj.write(data)
