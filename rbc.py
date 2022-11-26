#!/usr/bin/env python

# File: rbc.py

"""
"rbc" stands for (Bolinas) Rod & Boat Club.
This module is specific to the Bolinas Rod and Boat Club.
Dynamic (changing) data as maintained in SPoT (Single Point of Truth)
files under the 'Data' directory. Stable (rarely changing) data is
kept in other directories. There is also an Archive directory for
temporary storage of archives. All of these as well as the main code
base directory are contained under the top level project directory.
The code base is a git repository. The archive.py utility is available
to backup data to the archive directory and from there it can be
backed up to the Club's Google Drive account. 
It provides the <Club> class which serves largely to keep track of
global values.  Only one instance at a time.
"""

import os
import sys
import csv
import shutil
import helpers

# these initial declarations provide a SPoT[1]
# mainly for use by archive.py via the Club class.
# [1] Single Point of Light (or "DRY" for Don't Repeat Yourself)
root_dir = os.path.expandvars('$CLUB')
# Sources:
data_dir = "Data"
changing_data = (data_dir, )
mailing_dir = 'Data/MailingDir'  # Under Data
email_json_file = 'Data/emails.json'  # ditto
stable_data = ("exclude",
            "Info",
            "README",
            "requirements.txt",
            )
# Destinations:
archive = "Archives"
data_archive = 'Data'
mailing_archive = 'Mailings'
stable_archive = 'Stable'


class Club(object):
    """
    Create such an object for each data base used.
    In the current use case this is the only one and
    it pertains to the 'Bolinas Rod and Boat Club'.

    It may well be that most if not all the methods are redacted,
    their functionality taken over by code found elsewhere.
    """

    # "Archiving" provides for backup.
    # Two categories of data to be archived:
    # 1. constantly changing data
    INCLUDE_HEADERS = False
    INCLUDE_FEES = False
    QUIET = False
    QUIET = True
    DATA_DIR = os.path.join(root_dir, data_dir)
    CHANGING_DATA = [os.path.join(root_dir, entry)
                        for entry in changing_data]
    MAILING_DIR = os.path.join(root_dir, mailing_dir)
    EMAIL_JSON = os.path.join(root_dir, email_json_file)
    MAILING_SOURCES = (MAILING_DIR, EMAIL_JSON)
    # 2. stable rarely changing data
    STABLE_DATA = [os.path.join(root_dir, entry)
                        for entry in stable_data]
    # Destination(s) for the archiving process.
    ARCHIVE_DIR = os.path.join(root_dir, archive)
    DATA_ARCHIVE = os.path.join(ARCHIVE_DIR, data_archive)
    MAILING_ARCHIVE = os.path.join(ARCHIVE_DIR, mailing_archive)
    STABLE_ARCHIVE = os.path.join(ARCHIVE_DIR, stable_archive)
    # We keep a log of archiving done:
    ARCHIVING_INFO = os.path.join(root_dir, "Info/last")

    # Intermediate &/or temporary files used:
    STDOUT = 'output2check.txt'
    OUTPUT2READ = '2read.txt'  # } generally goes to stdout.
    ERRORS_FILE = 'errors.txt'
    
    # # Constants and Defaults...
    YEARLY_DUES = 100
    DOCK_FEE = 75
    KAYAK_FEE = 70
    SECRETARY = "Ed Mann" 
    # meetings are held on (the first[1]) Friday (of each month) and
    # elections are held at the February meeting.
    # [1] Second Friday if the first falls on January 1st.
    ELECTION_MONTH = 2  # February
    N_FRIDAY = 4  # ord of Friday: m, t, w, t, f, s, s

    # Data bases used with default file names.
    MEMBERSHIP_SPoT = os.path.join(DATA_DIR, 'memlist.csv')
    APPLICANT_SPoT = os.path.join(DATA_DIR, "applicants.txt")
    APPLICANT_CSV = os.path.join(DATA_DIR, "applicants.csv")
    SPONSORS_SPoT = os.path.join(DATA_DIR, "sponsors.txt")
    DOCK_SPoT = os.path.join(DATA_DIR, 'dock.txt')
    KAYAK_SPoT = os.path.join(DATA_DIR, 'kayak.txt')
    MOORING_SPoT = os.path.join(DATA_DIR, 'mooring.txt')
    EXTRA_FEES_SPoTs = ( DOCK_SPoT, KAYAK_SPoT, MOORING_SPoT,)
    CONTACTS_SPoT = os.path.expanduser(      # } File to which google
                '~/Downloads/contacts.csv')  # } exports the data.
    RECEIPTS_FILE = os.path.join(DATA_DIR,
            'receipts-{}.txt'.format(helpers.this_year))
    THANK_FILE =  os.path.join(DATA_DIR, '2thank.csv')
    THANK_ARCHIVE =  os.path.join(DATA_DIR,
            'thanked-{}.csv'.format(helpers.this_year))
    ADDENDUM2REPORT_FILE = os.path.join(DATA_DIR, "addendum2report.txt") 

#   redacted:
#   EXTRA_FEES_JSON = os.path.join(DATA_DIR, 'extra_fees.json')
#   EXTRA_FEES_TBL = os.path.join(DATA_DIR, 'extra_fees.tbl')  # not used!
#   TEMP_MEMBERSHIP_SPoT = os.path.join(DATA_DIR, 'new_memlist.csv')

    NAME_KEY = "by_name"          # } Used in context of
    CATEGORY_KEY = "by_category"  # } the extra fees.

    APPLICANT_DATA_FIELD_NAMES = (
        "first", "last", "status",
        "app_rcvd", "fee_rcvd",   #} date (or empty
        "1st", "2nd", "3rd",      #} string if event
        "inducted", "dues_paid",  #} hasn't happened.
        "sponsor1", "sponsor2",   # empty strings if not available
        )
    MEETING_DATE_NAMES = APPLICANT_DATA_FIELD_NAMES[5:8]
    ALL_APPLICANTS = False

    # # Google Contact Groups in use:  ("Labels", not "Groups")
    APPLICANT_GROUP = "applicant"
    MEMBER_GROUP = "LIST"
    OFFICER_GROUP = 'Officers'
    INACTIVE_GROUP = 'inactive'
    DOCK_GROUP = 'DockUsers'
    KAYAK_GROUP = 'Kayak'
    MOORING_GROUP = 'moorings'
    SECRETARY_GROUP = 'secretary'
    GOOGLE_GROUPS = {APPLICANT_GROUP, DOCK_GROUP, KAYAK_GROUP,
                     MEMBER_GROUP, MOORING_GROUP, OFFICER_GROUP,
                     SECRETARY_GROUP, INACTIVE_GROUP, 
                     }
    
    # Miscelaneous 
    INCLUDE_BAD_EMAILS = False
    # the following is used only in utils.set_default_args4curses:
    DEFAULT_FORMAT = 'first_last'

    # # ...end of Constants and Defaults.


    n_instances = 0

    @classmethod
    def inc_n_instances(cls):
        cls.n_instances += 1

    def __init__(self, args=None, params=None):
        """
        <args> are the command line arguments provided by docopts.
        <params> was necessary in the past when using labels or
        envelopes but is expected to be redacted since these are
        no longer used. Each instance needed to know the format
        of the media.
        """
        if self.n_instances > 0:
            raise NotImplementedError("Only one instance allowed.")
        self.inc_n_instances()
        
        ######  Set all defaults  #####
        self.include_headers = Club.INCLUDE_HEADERS
        self.include_bad_emails = Club.INCLUDE_BAD_EMAILS
        self.include_fees = Club.INCLUDE_FEES
        self.quiet = Club.QUIET
        self.infile = Club.MEMBERSHIP_SPoT
        self.applicant_spot = Club.APPLICANT_SPoT
        self.applicant_csv = Club.APPLICANT_CSV
        self.all_applicants = Club.ALL_APPLICANTS
        self.sponsors_spot = Club.SPONSORS_SPoT
        self.contacts_spot = Club.CONTACTS_SPoT
        self.extra_fees_spots = Club.EXTRA_FEES_SPoTs
        self.json_file = Club.EMAIL_JSON
        self.mail_dir = self.MAILING_DIR
        self.thank_file = Club.THANK_FILE
        self.thank_archive = Club.THANK_ARCHIVE
        self.outfile = Club.STDOUT
        self.errors_file = Club.ERRORS_FILE
        self.cc = ''
        self.bcc = ''
        self.fee_details = False

        if args:  # override defaults if provided by docopts
            self.include_headers = args['-H']
            self.include_bad_emails = args['--be']
            self.json_file = args['-j']
            self.include_fees = args['-f']
            self.quiet = args['-q']
            if args['-f']: self.fee_details = args['-f']
            if args['-i']: self.infile = args['-i']
            if args['-A']: self.applicant_spot = args['-A']
            if args['--csv']: self.applicant_csv = args['--csv']
            if args['--all_applicants']: self.all_applicants = True
            if args['-S']: self.sponsor_spot = args['-S']
            if args['-C']: self.contacts_spot = args['-C']
            if args['-X']: self.extra_fees_spots = args['-X']
#           if args['-j']: self.json_file = args['-j']
            if args["--dir"]: self.mail_dir = args["--dir"]
            if args['-t']: self.thank_file = args['-t']
            if args['--thanked']:
                self.thank_archive = args['--thanked']
            if args['-o']: self.outfile = args['-o']
            self.owing_only = args['--oo']
            Club.cc_sponsors = False
            if args['--cc']:
                (Club.cc_sponsors, Club.ccs) = helpers.clarify_cc(
                                        args['--cc'], 'sponsors')
            else:
                (Club.cc_sponsors, Club.ccs) = (False, [])
            if Club.cc_sponsors:  # collect applicant/sponsor data
                data.populate_sponsor_data(Club)
                data.populate_applicant_data(Club)
            if args['-e']: self.errors_file = args['-e']
            if args["--cc"]: self.cc = args["--cc"]
            if args["--bcc"]: self.bcc = args["--bcc"]
            if args['ATTACHMENTS']:
                self.attachment = args['ATTACHMENTS']
            else:
                self.attachment = None

        self.previous_name = ''              # } Used to
        self.previous_name_tuple = ('', '')  # } check
        self.first_letter = ''               # } ordering.


    def __repr__(self):
        attrs = [
                 'sponsor_spot',
                 'sponsors_by_applicant',
                 ]
        ret = []
        print('About to build attribute listing ...')
        for attr in attrs:
            if hasattr(self, attr):
                ret.append("{}::{}".format(attr, getattr(self, attr)))
            else:
                ret.append("{}::??".format(attr))
        return ','.join(ret)


    def fee_totals(self, infile=RECEIPTS_FILE):
        """
        Returns a list of strings: subtotals and grand total.
        Sets up and populates self.invalid_lines ....
        (... the only reason it's a class method
        rather than a function or a static method.)
        NOTE: Money taken in (or refunded) must appear
        within line[28:33]! i.e. maximum 5 digits (munus sign
        and only 4 digits if negative).
        """
        print("Running Club.fee_totals()")
        res = ["Fees taken in to date:"]
        self.invalid_lines = []

        total = 0
        subtotal = 0

        with open(infile, "r") as file_obj:
            print('Reading from file "{}".'.format(file_obj.name))
            for line in file_obj:
                line = line.rstrip()  # get rid of trailing '\n'
                if line.startswith("Date:") or not line.strip():
                    continue  # Ignore date headers and blank lines
                if (line[29:32] == "---") and subtotal:
                    res.append(
                        "    SubTotal                 --- {:>10}"
                       .format(helpers.format_dollar_value(subtotal)))
                    subtotal = 0
                try:
                    amount = int(line[28:33])
                except (ValueError, IndexError):
                    self.invalid_lines.append(line)
                    continue
                total += amount
                subtotal += amount
        if subtotal:
            res.append("         SubTotal            --- {:>10}"
                       .format(helpers.format_dollar_value(subtotal)))
        res.append("\nGrand Total to Date:         --- ---- {:>10}"
                   .format(helpers.format_dollar_value(total)))
        ## Find 'error' lines (those without expected data)
        ## in club.invalid_lines
        return res
# ##
# ###  End of Club class declaration.

if __name__ == "__main__":
    print("rbc.py compiles OK")
    print("DATA_DIR resolves to {}".format(Club.DATA_DIR))
    sys.exit()
#else:
#    def print(*args, **kwargs):
#        pass

