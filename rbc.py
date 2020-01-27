#/usr/bin/env python

# File: rbc.py

import os

# Specify input file and its data:
class Club(object):
    """
    Create such an object for each data base used.
    In the current use case this is the only one and
    it pertains to the 'Bolinas Rod and Boat Club'.

    It may well be that most if not all the methods are redacted,
    their functionality taken over by code found elsewhere.
    """

    ## Constants and Defaults...
    YEARLY_DUES = 100

    # Data bases used with default file names.
    MEMBERSHIP_SPoT = 'Data/memlist.csv'
    APPLICANT_SPoT = "Data/applicants.txt"
    EXTRA_FEES_SPoT = 'Data/extra_fees.txt'
    CONTACTS_SPoT = os.path.expanduser(     #} File to which google
                '~/Downloads/contacts.csv') #} exports the data.
    CHECKS_RECEIVED = 'Data/receipts.txt'  # Zeroed out yearly
        # and then stored in archives with date extension.

    SEPARATOR = "|"   #} File APPLICANT_SPoT must be in a
    N_SEPARATORS = 3  #} specific format for it to be read
                      #} correctly. Number of meetings is
                      #} derived from N_SEPARATORS.
    NAME_KEY = "by_name"         #} Used in context of
    CATEGORY_KEY = "by_category" #} the extra fees.

    ## Google Contact Groups in use:
    GOOGLE_GROUPS = { "applicant," "DockUsers", "Kayak",
            "LIST", "moorings", "Officers", 'Secretary',
            "member",   # 'member' is there but not used.
            }
    ### Should use the above to check data integrity!! ####
    ### Yet to be implemented. ###
    APPLICANT_GROUP = "applicant"  # } These are specific to
    MEMBER_GROUP = "LIST"          # } the gmail contacts csv:
    OFFICER_GROUP = 'Officers'     # } CONTACTS_SPoT
    DOCK = 'DockUsers'
    KAYAK = 'Kayak'
    MOORING = 'moorings'
    SECRETARY = 'Secretary'

    # Intermediate &/or temporary files used:
    EXTRA_FEES_JSON = 'Data/extra_fees.json'
    EXTRA_FEES_TBL = 'Data/extra_fees.tbl'  # not used!
    TEMP_MEMBERSHIP_SPoT = 'Data/new_memlist.csv'
    OUTPUT2READ = 'Data/2read.txt'       #} generally goes to stdout.
    MAILING_DIR = 'Data/MailingDir'
    JSON_FILE_NAME4EMAILS = 'Data/emails.json'
    ## ...end of Constants and Defaults.

    def __init__(self, params=None):
        """
        Each instance must know the format
        of the media. i.e. the parameters (<params>.)
        This is being redacted since we are not using labels or
        envelopes as was done before.
        """
        self.infile = Club.MEMBERSHIP_SPoT
        self.name_tuples = []
        self.json_data = []
        self.previous_name = ''              # } Used to
        self.previous_name_tuple = ('', '')  # } check 
        self.first_letter = ''               # } ordering.

    def ck_data(self, source_file, google_file, separator):
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
                ret.append("\nNo entries for '{}'".format(report_name))
#       with open("g_collector", 'w') as file_obj:
#           file_obj.write("Number found: {}".format(g_counter) +
#               '\n' + "\n".join(g_collector))
        return separator.join(ret)
    ### End of ck_data method.


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

redacted = '''
## Custom Functions:
## I believe the following are all redacted.
## The mailing related methods have been replaced by functions
## in the member.py module, specifically q_mailing(record,club).

    def send_mailing(self, record, content, both=False):
        """
        Sends email if there is content in record['email']
        and a letter if there is not.  If both=True then a
        letter is sent regardless of record['email'] content.
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

'''
####  End of Club class declaration.