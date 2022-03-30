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
root_dir = os.path.split(os.getcwd())[0]
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
#   redacted:
#   EXTRA_FEES_SPoT = os.path.join(DATA_DIR, 'extra_fees.txt')
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

    # Non repo directories (used by archive.py:)
#   print(os.path.split(os.getcwd()))
    (head, tail) = os.path.split(os.getcwd())
#   NONREPO_DIRS = ("Data",
#                   "Exclude",
#                   "Info",
#                   "Mydata",
#                   )
#   NONREPO_DIRS = [os.path.join(
#       os.path.split(os.getcwd())[0],
#       'NR',
#       f) for f in NONREPO_DIRS]
    
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

    # # Google Contact Groups in use:
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
    # # could use the above to check data integrity!! ####
    # # Yet to be implemented. ###
    DOCK_FEE = 75
    KAYAK_FEE = 70
    SECRETARY = "Ed Mann" 
    
    # Miscelaneous 
    DEFAULT_FORMAT = 'listings'
    PATTERN = '{last}, {first}'
    PATTERN4WEB = ('{first} {last} [{phone}] {address}, {town},' +
                   ' {state}, {postal_code} [{email}]')
    with open(MEMBERSHIP_SPoT) as db_stream:
        reader = csv.DictReader(db_stream)
        DB_FIELDNAMES = reader.fieldnames
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

        if args:  # args from docopt
            # the body of this if statement replaces the need for
            # <utils.file_name_args2attributes(self, params)>
            if args['-i']: self.infile = args['-i']
            else: self.infile = Club.MEMBERSHIP_SPoT

            if args['-A']: self.applicant_spot = args['-A']
            else: self.applicant_spot = Club.APPLICANT_SPoT

            if args['-S']: self.sponsor_spot = args['-S']
            else: self.sponsor_spot = Club.SPONSORS_SPoT

            if args['-C']: self.contacts_spot = args['-C']
            else: self.contacts_spot = Club.CONTACTS_SPoT

            if args['-X']: self.extra_fees_spots = args['-X']
            else: self.extra_fees_spots = Club.EXTRA_FEES_SPoTs

            if args['-j']: self.json_file = args['-j']
            else: self.json_file = Club.EMAIL_JSON

            if args["--dir"]: self.mail_dir = args["--dir"]
            else: self.mail_dir = self.MAILING_DIR

            if args['-t']: self.thank_file = args['-t']
            else: self.thank_file = Club.THANK_FILE

            if args['--thanked']:
                self.thank_archive = args['--thanked']
            else: self.thank_archive = Club.THANK_ARCHIVE

            if args['-o']: self.outfile = args['-o']
            else: self.outfile = Club.STDOUT

            if args['-e']: self.errors_file = args['-e']
            else: self.errors_file = Club.ERRORS_FILE

            if args["--cc"]: self.cc = args["--cc"]
            else: self.cc = ''

            if args["--bcc"]: self.bcc = args["--bcc"]
            else: self.bcc = ''

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
        within line[23:28]! i.e. maximum 5 digits (munus sign
        and only 4 digits if negatime).
        """
        res = ["Fees taken in to date:"]
        self.invalid_lines = []

        total = 0
        subtotal = 0
        date = ''

        with open(infile, "r") as file_obj:
            print('Reading from file "{}".'.format(file_obj.name))
            for line in file_obj:
                line = line.rstrip()
                if line[:5] == "Date:":
                    date = line
                if (line[24:27] == "---") and subtotal:
                    res.append("    SubTotal            --- {:>10}"
                               .format(helpers.format_dollar_value(subtotal)))
                    subtotal = 0
                try:
                    amount = int(line[23:28])
                except (ValueError, IndexError):
                    self.invalid_lines.append(line)
                    continue
#               res.append("Adding ${}.".format(amount))
                total += amount
                subtotal += amount
#               print(" adding {}, running total is {}"
#                   .format(amount, total))
        if subtotal:
            res.append("    SubTotal            --- {:>10}"
                       .format(helpers.format_dollar_value(subtotal)))
        res.append("\nGrand Total to Date:    --- ---- {:>10}"
                   .format(helpers.format_dollar_value(total)))
#       print("returning {}".format(res))
        return res
# ##
# ###  End of Club class declaration.

if __name__ == "__main__":
    print("rbc.py compiles OK")
    print("DATA_DIR resolves to {}".format(Club.DATA_DIR))
    sys.exit()
else:
    def print(*args, **kwargs):
        pass

tree = """
ProjectDirectory
├── Archives
│   ├── Data
│   │   └── Temp
│   ├── Mailings
│   │   └── Temp
│   ├── Receipts
│   ├── Reports
│   └── Stable
├── Data
│   ├── 2thank.csv
│   ├── addendum2report.txt
│   ├── applicants.txt
│   ├── dock.txt
│   ├── kayak.txt
│   ├── memlist.csv
│   ├── mooring.txt
│   ├── old_extras
│   ├── receipts-2022.txt
│   ├── redacted-extra_fees.txt
│   ├── sponsors.txt
│   └── thanked-2022.csv
├── exclude
├── Info
│   ├── attrition.txt
│   ├── club_history
│   ├── Formats
│   │   ├── letter_layout.txt
│   │   └── letter_spacing.txt
│   ├── last
│   ├── leadership.txt
│   ├── procedures
│   ├── reimbursements.txt
│   ├── response2membership_inquiries.txt
│   └── Thanked
├── README
├── requirements.txt
├── Stable
│   ├── Guides
│   │   ├── application_for_membership__.pdf
│   │   ├── bylaws
│   │   ├── credentials
│   │   └── mem_duties.txt
│   └── Original
│       ├── 2018
│       │   ├── 2017DOCKUsers.doc
│       │   ├── 2017MOORINGList.doc
│       │   ├── 2018KAYAK FEE.doc
│       │   ├── Bolinas-RBC-mailing-List-20180309.csv
│       │   ├── Jan18TotalLIST.xlsx
│       │   ├── mary_abbot_intro.txt
│       │   ├── MembershipChairDuties.docx
│       │   ├── MemDutiesV2.docx
│       │   └── mylist.xlsx
│       └── README
└── Utils  # in git repo
"""
