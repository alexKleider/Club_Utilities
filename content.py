#!/usr/bin/env python

# File: content.py

"""
A module to support the utils.py prepare_mailing command.
(... and also the emailing command.)

Rather than importing functions, they are refered to by
name and depend on a dict within the utils.Membership class
with those names as keys and the methods as values.

A number of 'dict's are being used:
    letter_bodies
    authors: ak, membership,
    content_types
        each provides: {
            "subject":
            "from": authors["membership"],
#           'reply2': 'randolf@sonic.net'
            "body": letter_bodies["happyNY_and_0th_fees_request"],
            "post_script": a string,
            "funcs": [func_1, ..],
            "test": lambda record: True,
            "e_and_or_p": "one_only",
            },
    printers: X6505, HL2170, ...

Other items:
    email_header
    def letter_format(which_letter, printer):
    def prepare_email_template(which_letter):
"""

import helpers
import member

address_format = """{first} {last}
{address}
{town}, {state} {postal_code}
{country}"""

custom_lambdas = dict(
    QuattroSolar= (
        lambda record: True
            if 'Quattro Solar' in record["company"]
            else False),
    MarinMechanical= (
        lambda record: True
            if 'Marin Mechanical' in record["company"]
            else False),
    )

email_header = """From: {}
Reply-To: {}
To: {{email}}
Subject: {}

Dear {{first}} {{last}},"""

easy_email_header = """
Dear {first} {last},"""

letter_bodies = dict(
    for_testing = """
Blah, Blah-
more Blah blah

etc

First extra content is
{{extra}}

May have as many 'extra's as required as long as each one
has a corresponding entry in the record dict (typically arranged
by the custom function.
""",

    meeting_announcement = """
Board members meet at 6pm.
General meeting scheduled for 7:30pm.
Come for the fun!
""",

    feb_meeting_announcement = """

We have a special Bolinas Rod and Boat Club meeting coming up
February 7th.

Board members meet at 5pm.

The general meeting is scheduled for 6:00pm.
Election of Officers is the main agenda item.

Those with reservations[1]  are invited to stay for the
annual dinner to be held afterwards.

Come for the fun!
""",

    usps_minutes = """
Enclosed, please find the latest Club minutes.
Enjoy!
""",

    happyNY_and_0th_fees_request = """
A very Happy New Year to all members of the Bolinas Rod & Boat
Club!

Another friendly reminder that the Club maintains a membership
list on the 'Membership' section of the Club web site:
(rodandboatclub.com, password is 'fish'.) Please check it out
if you want to get in touch with a fellow member.
changes that should be made.

At this time you might be doing some financial planning for the
year; don't forget to include provisions for payment of Club dues
(and possibly fees as well.)  The following is included to help
you in this regard.  It's always acceptable to pay early and get it
behind you.{extra}

If the number is negative or zero, there'll be nothing due in June.
""",

    February_meeting = """
Things are to be somewhat different for the February meeting
on Friday, the 1st.
The Board will meet at 5:30 and then there will be the general
meeting at 6:00pm.  This meeting also includes a dinner which is
to begin circa 6:30.  Those intending to remain for dinner should
make a reservation- check with Anna Gade (uc_anna@sbcglobal.net.)
Applicants are invited but we ask members not to bring guests,
for the simple reason that seating is limited (hence the importance
of making a reservation.)
""",

    thank_you_for_advanced_payment = """
Your advance payment of dues for the next ({}) Club year
has been received.  Thank you.

All the best!
""".format(helpers.next_club_year()),

    thank_you_for_timely_payment = """
Your timely payment of dues for the next ({}) Club year
has been received.  Thank you.

All the best!
""".format(helpers.next_club_year()),

    yearly_fees_1st_request = """
The current Club membership year ends in June and ideally we'd
like to have all dues and fees for the upcoming ({})
membership year in by then.  If you are already paid up,
the Club thanks you.

Remember that you can find out all about yourself and fellow
club members by going to the Club web site (rodandboatclub.com,
password is 'fish',) click on 'Membership.'  Let us know if any
corrections should be made

A statement of your current standing appears bellow;
If there are any dues or fees outstanding, please don't delay.
If the total is zero (or negative) you're all paid up (or more than
paid up) and we thank you.
{{extra}}""".format(helpers.next_club_year()),

    yearly_fees_2nd_request = """
This is a second request being sent out to Club members whose
dues (and/or fees where applicable) for the current (began
July 1st) Club year have not yet been payed. You should also
note that this is the last notice you can expect to receive
before the late penalty (of $25) is imposed on those who's
remittance has not been received postmarked on or before August 1st.

Details are as follows:
{extra}""",

    yearly_fees_corrected_2nd_request = """
Your membership secretary neglected in the last request for
dues (and fees where applicable) to mention where to send
your check.  Please forgive the oversight. It's:
    Bolinas Rod and Boat Club
    PO Box 248
    Bolinas, CA 94924
Details as to what you still owe follow:
{extra}""",

    final_warning = """
Club records indicate that your dues (+/- other fees) have as
yet not been paid.  Please be aware that according to Club bylaws,
membership lapses if fees are not paid by Sept 1st.

Please pay promptly; we'd hate to loose you as a member.

Details follow.
{extra}""",

    penalty_notice = """
The deadline for Club Dues payment has passed and records indicate
that you are in arrears so a late fee of $25 has been applied.
If you feel this is incorrect, please speak up[1]- we are only
human!  Otherwise, don't delay sending in your check rather than
risk being removed from the Club's list of members.

Details are as follows:
{extra}""",

    bad_email = """
Emails sent to you at
    "{email}"
are being rejected.

Can you please help sort this out by contacting us
at rodandboatclub@gmail.com?

Thanks,""",

    new_applicant_welcome = """
As Membership Chair it is my pleasure to welcome you as a new
applicant for membership in the Bolinas Rod and Boat Club.

Please come and enjoy the meetings (first Fiday of each month.)

To become eligible for membership (and not waste your application
fee) you must attend a minimum of three meetings with in the six
month period beginning the date your application was received.""",

    request_inductee_payment = """
The Club Executive Committee has, at its last meeting,
approved your application for Club membership.

"Welcome aboard!"

All that remains for your membership to take effect is payment
of dues.  Please send a check for ${current_dues} to the Club
(address provided below.)

Upon receipt of your membership dues, I'll send you more information
about the Club and your privileges as a member there of.""",

    second_request_inductee_payment = """
Your application for Club membership was approved by the
Club Executive Committee at its last meeting and membership
fees have been requested but as yet not received.  Until
payment is received you are not yet a member.  This could
create a problem for the Exec committee since there are applicants
ready to take the spot that you would take if, but only if, the
dues are paid.  The Committee meets in less than a week!

Please send a check for ${current_dues} to the Club
(address provided below.)""",


    welcome2full_membership = """
It is my pleasure to welcome you as a new member to the Bolinas Rod
and Boat Club!

You will be receiving meeting minutes (via email) as prepared by
our Club Secretary Peter Pyle.

As you may know, the Club has its own web site: 'rodandboatclub.com'.
It is password protected; the password is 'fish' (a not very closely
guarded secret.)  By clicking on the "Membership" tab, you can find
all your fellow members along with contact information.  If you see
any inaccuracies there, please make it known[1] so corrections can be
made.

Members can (upon payment of a $10 deposit) get a key to the Club
from "keeper of the keys" Ralph Cammicia.  Many take advantage of
having this access to spend time on the balconey enjoying views of
the lagoon and Bolinas Ridge.  Please be sure to lock up upon
leaving.

The Club is available for members to rent for private functions (if
certain conditions are met.)  More information can be found on the web
site: "Rules and Forms" and under that "Club Rentals".

Most important of all, come to meetings and other functions to enjoy
the comraderie!""",

    expired_application = """
It's been more than six months since your membership application has
been received which makes it now expired.  If you still wish to be a
member of the Bolinas Rod and Boat Club the application process must
begin again.""",

    cover_letter = """
Enclosed you'll find minutes of the Bolinas Rod and Boat Club.""",

    personal = """
Enclosed please find the payment.

It was a good dinner and an enjoyable evening.

Sincerely,
Alex Kleider
""",

    fromPeter = """
Enjoy the minutes!
Peter Pyle, Secretary
""",

    tpmg_social_security = """
Please find enclosed the documentation I believe you require from the
Social Security Administration concerning Medicare deductions for both
my wife and for me.
""",

    fromRandy = """
The pluma pescadores, fly fishers, wing of the BRBC will be meeting
in the yurt at the Rushes Thursday at 7 pm.  Snacks, stories, lessons
on knots, equipment comments, lines, leaders, flies and laughter.

Due to lack of outdoor light we will not be casting...yet.  Bring
questions, show and tell items, stories and your own elixir.  We
usually adjourn sometime after 9ish.

15 Rafael Ave.,  off Marin Way.
Park and follow solar yard lights to yurt.
Bring flashlight is best.

Cheers and tight lines.
""",

    payment = """
Thank you for your services.
"""
    )
# ... end of letter_bodies.


post_scripts = dict(
    at_request_of_secretary = """ Sent at the request of Peter Pyle, Secretary""",

    remittance = """ Please send remittances to:
    The Bolinas Rod & Boat Club
    PO Box 248
    Bolinas, CA 94924
It's always a good idea to jot down 'club dues' on
the check in order to prevent any confusion.""",

    ref1 = """[1] rodandboatclub@gmail.com or PO Box 748, 94924""",

    reservations = """[1] Reservations can be made through Anna Gade
    (uc_anna@sbcglobal.net.)""",
    )

authors = dict(  # from
    ak = dict(
        first = "Alex",
        last = "Kleider",
        address = "PO Box 277",
        town = "Bolinas",
        state = "CA",
        postal_code = "94924",
        country = "USA",
        email_signature = "\nSincerely,\nAlex Kleider",
        email = "akleider@sonic.net",
        reply2 = "akleider@sonic.net",
        mail_signature = "\nSincerely,\n\n\nAlex Kleider",
        ),
    membership = dict(
        first = "Bolinas",
        last = "Rod & Boat Club",
        address = "PO Box 248",
        town = "Bolinas",
        state = "CA",
        postal_code = "94924",
        country = "USA",
        email_signature = "\nSincerely,\nAlex Kleider (Membership)",
        email = "rodandboatclub@gmail.com",
        reply2 = "rodandboatclub@gmail.com",
        mail_signature = "\nSincerely,\n\n\nAlex Kleider (Membership)",
        ),
    secretary = dict(
        first = "Bolinas",
        last = "Rod & Boat Club",
        address = "PO Box 248",
        town = "Bolinas",
        state = "CA",
        postal_code = "94924",
        country = "USA",
        email_signature = (
            "\nSincerely,\nMichael Rafferty (Club Secretary)"),
        email = "rodandboatclub@gmail.com",
        reply2 = "rodandboatclub@gmail.com",
        mail_signature = (
            "\nSincerely,\n\n\nMichael Rafferty (Club Secretary)"),
        ),
    randy = dict(
        first = "Randy",
        last = "Rush",
        address = "15 Rafael Ave.",
        town = "Bolinas",
        state = "CA",
        postal_code = "94924",
        country = "USA",
        email_signature = "\nSincerely,\nRandy Rush",
        email = 'rodandboatclub@gmail.com',
#       email = "alex@kleider.ca",
        reply2 = 'randolph@sonic.net',
        mail_signature = "\nSincerely,\n\n\nRandy Rush",
        ),
    )  # ... end of authors.

# One of the following content_types is assigned to the 'which'
# attribute of an instance of utils.Club for mailing purposes.

    # Each item in the following dict specifies:
        # subject: re line in letter_bodies, subject line in emails
        # from: expect a value from the 'authors' dict
        #     each value is itself a dict specifying more info...
        #     names, address, signatures, reply to, ..
        # body: text of the letter which may or may not have
        #     one or more 'extra' sections.
        # post_scripts:  a list of optional postscripts
        # funcs: a list of functions used on each record during
        #     the data gathering traversal of the membership csv.
        # test: a (usually 'lambda') function that determines
        #     if the record is to be considered at all.
        # e_and_or_p: possibilities are:
        #     'both' email and usps,
        #     'email' email only,
        #     'usps' mail only,
        #  or 'one_only' email if available, othewise usps.
    # One of the following becomes the 'which' attribute
    # of a Membership instance.

content_types = dict(  # which_letter
    for_testing = {
        "subject": "This is a test.",
        "from": authors["ak"],
        "body": letter_bodies["for_testing"],
        "post_scripts": (),
        "funcs": [member.std_mailing, ],
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    meeting_announcement = {
        "subject": "Meeting Friday",
        "from": authors["secretary"],
        "body": letter_bodies["meeting_announcement"],
        "post_scripts": (),
        "funcs": (member.std_mailing,),
        "test": lambda record: True if record["email"] else False,
        "e_and_or_p": "one_only",
        },
    feb_meeting_announcement = {
        "subject": "Meeting first Friday of February",
        "from": authors["membership"],
        "body": letter_bodies["feb_meeting_announcement"],
        "post_scripts": (post_scripts['reservations'],),
        "funcs": (member.std_mailing,),
#       "test": lambda record: True,
        "test": lambda record: True if record["email"] else False,
        "e_and_or_p": "email",
        },
    usps_minutes = {
        "subject": "Rod & Boat Club Minutes",
        "from": authors["secretary"],
        "body": letter_bodies["usps_minutes"],
        "post_scripts": (),
        "funcs": (member.std_mailing,),
        "test": lambda record: False if record["email"] else True,
        "e_and_or_p": "usps",
        },
    happyNY_and_0th_fees_request = {
        "subject": "Happy New Year from the Bolinas R&B Club",
        "from": authors["membership"],
        "body": letter_bodies["happyNY_and_0th_fees_request"],
        "post_scripts": (post_scripts["remittance"],),
        "funcs": (member.set_owing,),
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    February_meeting = {
        "subject": "Change regarding format and time of next meeting",
        "from": authors["membership"],
        "body": letter_bodies["February_meeting"],
        "post_scripts": (),
        "funcs": (member.std_mailing,),
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    thank_you_for_advanced_payment = {
        "subject": "Thanks for your payment",
        "from": authors["membership"],
        "body": letter_bodies["thank_you_for_advanced_payment"],
        "post_scripts": (),
        "funcs": (member.std_mailing,),
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    thank_you_for_timely_payment = {
        "subject": "Thanks for your payment",
        "from": authors["membership"],
        "body": letter_bodies["thank_you_for_timely_payment"],
        "post_scripts": (),
        "funcs": (member.std_mailing,),
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    yearly_fees_1st_request = {
        "subject": "Bolinas R&B Club fees coming due",
        "from": authors["membership"],
        "body": letter_bodies["yearly_fees_1st_request"],
        "post_scripts": (post_scripts["remittance"],),
        "funcs": (member.set_owing,),
        "test": lambda record: False if (('a' in record["status"]) or
                ('w' in record["status"])) else True,
        "e_and_or_p": "one_only",
        },
    yearly_fees_2nd_request = {
        "subject":"Second request for BR&BC dues",
        "from": authors["membership"],
        "body": letter_bodies["yearly_fees_2nd_request"],
        "signature": '',
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1"],
            ),
        "funcs": (member.set_owing,),
        "test": lambda record: True if ((
            member.is_member(record) and
            member.not_paid_up(record))
            ) else False,
        "e_and_or_p": "one_only",
        },
    yearly_fees_corrected_2nd_request = {
        "subject":"Second request for BR&BC dues",
        "from": authors["membership"],
        "body": letter_bodies["yearly_fees_corrected_2nd_request"],
        "signature": '',
        "post_scripts": (
#           post_scripts["remittance"],
#           post_scripts["ref1"],
            ),
        "funcs": (member.set_owing,),
        "test": lambda record: True if ((
            member.is_member(record) and
            member.not_paid_up(record))
            ) else False,
        "e_and_or_p": "one_only",
        },
    final_warning = {
        "subject":"Membership soon to expire",
        "from": authors["membership"],
        "body": letter_bodies["final_warning"],
        "post_scripts": (post_scripts["remittance"],),
        "funcs": (member.set_owing,),
        "test": lambda record: True if ((
            member.is_member(record) and
            member.not_paid_up(record))
            ) else False,
        "e_and_or_p": "both",
        },
    penalty_notice = {
        "subject":"BR&BC dues and penalty for late payment",
        "from": authors["membership"],
        "body": letter_bodies["penalty_notice"],
        "post_scripts": (post_scripts["remittance"],),
        "funcs": (member.set_owing,),
        "test": lambda record: True if ((
            member.is_member(record) and
            member.not_paid_up(record))
            ) else False,
        "e_and_or_p": "both",
        },
    bad_email = {
        "subject": "non-working email",
        "from": authors["membership"],
        "body": letter_bodies["bad_email"],
        "post_scripts": (),
        "funcs": (member.std_mailing,),
        "test": (
        lambda record: True if 'be' in record["status"] else False),
        "e_and_or_p": "usps",
        },
    new_applicant_welcome = {
        "subject": "Welcome to the Club",
        "from": authors["membership"],
        "body": letter_bodies["new_applicant_welcome"],
        "post_scripts": (),
        "funcs": (member.std_mailing,),
        "test": (
        lambda record: True if
            (record["status"] and 'a' in record["status"].split("|"))
            else False),
        "e_and_or_p": "one_only",
        },
    request_inductee_payment = {
        "subject": "Welcome to the Bolinas Rod & Boat Club",
        "from": authors["membership"],
        "body": letter_bodies["request_inductee_payment"],
        "post_scripts": (post_scripts["remittance"],),
        "funcs": (member.request_inductee_payment,),
        "test": (
        lambda record: True if 'ai' in record["status"] else False),
        "e_and_or_p": "one_only",
        },
    second_request_inductee_payment = {
        "subject": "Still awaiting Club dues",
        "from": authors["membership"],
        "body": letter_bodies["second_request_inductee_payment"],
        "post_scripts": (post_scripts["remittance"],),
        "funcs": (member.request_inductee_payment,),
        "test": (
        lambda record: True if 'ai' in record["status"] else False),
        "e_and_or_p": "one_only",
        },
    welcome2full_membership = {
        "subject": "You are a member!",
        "from": authors["membership"],
        "body": letter_bodies["welcome2full_membership"],
        "post_scripts": (post_scripts["ref1"], ),
        "funcs": (member.std_mailing,),
        "test": (
        lambda record: True if 'm' in record["status"] else False),
        "e_and_or_p": "one_only",
        },

    expired_application = {
        "subject": "Application Expired",
        "from": authors["membership"],
        "body": letter_bodies["expired_application"],
        "post_scripts": ( ),
        "funcs": (member.std_mailing,),
        "test": (
        lambda record: True if record["first"] == 'Joseph'
                and record['last'] == 'Nowicki' else False),
        "e_and_or_p": "one_only",
        },

    cover_letter ={
        "subject": "Recent Minutes",
        "from": authors["secretary"],
        "body": letter_bodies["cover_letter"],
        "post_scripts": ( ),
        "funcs": (member.std_mailing,),
        "test": (
        lambda record: False if record['email'] else True),
        "e_and_or_p": "one_only",
        },

    personal = {
        "subject": "Old Boys Dinner Reimbursement",
        "from": authors["ak"],
        "body": letter_bodies["personal"],
        "post_scripts": (),
        "funcs": (member.std_mailing,),
        "test": (
        lambda record: True if 'p' in record["status"] else False),
        "e_and_or_p": "usps",
        },
    tpmg_social_security = {
        "subject": "Medicare Reimbursement",
        "from": authors["ak"],
        "salutation": "Dear Sir or Madame,",
        "body": letter_bodies["tpmg_social_security"],
        "post_scripts": (),
        "funcs": (member.std_mailing,),
        "test": (
        lambda record: True if 'TPMG' in record["first"] else False),
        "e_and_or_p": "usps",
        },
    randy = {
        "subject": "Pluma Pescadores",
        "from": authors["randy"],
#       "salutation": "Dear Sir or Madame,",
        "body": letter_bodies["fromRandy"],
        "post_scripts": (),
        "funcs": (member.std_mailing,),
        "test": (
            lambda record:
            True if (member.is_member_or_applicant(record)
            and member.has_valid_email(record))
            else False),
        "e_and_or_p": "email",
        },
    payment = { ## If using this, must edit "test" ##
        "subject": "Payment of Amount Due",
        "from": authors["ak"],
#       "salutation": "Dear Sir or Madame,",
        "body": letter_bodies["payment"],
        "post_scripts": (),
        "funcs": (member.std_mailing,),
        "test": custom_lambdas['MarinMechanical'],
#       "test": custom_lambdas['QuattroSolar'],
        "e_and_or_p": "usps",
        },

    )
    # ... end of content_types.

printers = dict(
    # tuples in the case of windows.
    X6505 = dict(
        indent = 5,
        top = 2,  # blank lines at top  1 ..2
        frm = (4, 25),  # return window 3..6
        date = 5,  # lines between windows 7..11
        to = (5, 30),  # recipient window 12..16
        re = 2,  # lines below bottom window
        ),
    HL2170 = dict(
        indent = 3,
        top = 1,  # blank lines at top
        frm = (5, 25),  # return window
        date = 4,  # between windows
        to = (7, 29),  # recipient window
        re = 3,  # below windows => fold
        ),
    Janice = dict(
        indent = 4,
        top = 4,  # blank lines at top
        frm = (5, 25),  # return window
        date = 4,  # between windows
        to = (7, 29),  # recipient window
        re = 3,  # below windows => fold
        ),
    Michael = dict(
        indent = 0,
        top = 0,  # blank lines at top
        frm = (4, 30),  # return window
        date = 3,  # between windows
        to = (6, 38),  # recipient window
        re = 3,  # below windows => fold
        ),
    )
### ... end of printers (dict specifying printer being used.)

def expand_array(content, n):
    if len(content) > n:
        print("ERROR: too many lines in <content>")
        print("    parameter of content.expand()!")
        assert False
    a = [item for item in content]
#   print('n=={} '.format(n), end='')
    while n > len(a):
        if n - len(a) >= 2:
            a = [''] + a + ['']
        else:
            a.append('')
#       print('n=={} '.format(n), end='')
    return a


def expand_string(content, n):
    a = content.split('\n')
    ret = expand_array(a, n)
    return '\n'.join(ret)


def expand(content, nlines):
    """
    Takes <content> which can be a list of strings or
    all one string with line feeds separating it into lines.
    Returns the same type (either string or list) but of <nlines>
    length, centered by blank strings/lines. If need an odd number
    of blanks, the odd one is at end (rather than the beginning.
    Fails if <content> has more than nlines.
    """
    if isinstance(content, str):
        return expand_string(content, nlines)
    else:
        return expand_array(content, nlines)


def get_postscripts(which_letter):
    """
    Returns a list of lines representing the post scripts
    """
    ret = []
    n = 0
    for post_script in which_letter["post_scripts"]:
        ret.append("\n" + "P"*n + "PS " + post_script)
        n += 1
    return ret


def letter_format(which_letter, printer):
    """
    Prepares the template for a letter.
    <which_letter>: one of the <content_types> and
    <printer>: one of the keys to the <printers> dict
    specifying which printer is to be used (passed as the
    "--lpr" command line parameter.)
    Returns a 'letter' with formatting fields of <record>:
    typically {first}, {last}, {address}, {town}, {state},
    {postal_code}, {country}, and possibly (one or more)
    {extra}(s) &/or 'PS's.
    """
    lpr = printers[printer]
    # top margin:
    ret = [""] * lpr["top"]  # add blank lines at top
    # return address:
    ret_addr = address_format.format(**which_letter["from"])
    ret.append(expand(ret_addr, lpr['frm'][0]))
    # format string for date:
    ret.append(expand((helpers.get_datestamp()),lpr['date']))
    # format string for recipient adress:
    ret.append(expand(address_format,lpr['to'][0]))
    # subject/Re: line
    ret.append(expand("Re: {}".format(which_letter["subject"]),
        lpr['re']))
    # format string for salutation:
    try:
        ret.append(which_letter["salutation"] + "\n")
    except KeyError:
        ret.append("Dear {first} {last},\n")
    # body of letter (with or without {extra}(s))
    ret.append(which_letter["body"])
    # signarue:
    ret.append(which_letter["from"]["mail_signature"])
    # post script:
    ret.extend(get_postscripts(which_letter))
    return '\n'.join(ret)

def prepare_email_template(which_letter, easy=False):
    """
    Prepares the template for an email.
    Used by utils.prepare_mailing_cmd,
    """
    if easy:
        ret = [easy_email_header]
    else:
        ret = [email_header.format(
                    which_letter["from"]["email"],
                    which_letter["from"]["reply2"],
                    which_letter["subject"]),]
    ret.append(which_letter["body"])
    ret.append(which_letter["from"]["email_signature"])
    ret.extend(get_postscripts(which_letter))
    return '\n'.join(ret)

def choices():
    """
    Provides a way of getting a quick glimps
    of the various contents provided.
    Typical usage:
        print('\n'.join(choices()))
    """
    tuples = ( ('custom_lambdas', custom_lambdas),
               ('letter_bodies', letter_bodies),
               ('post_scripts', post_scripts),
               ('authors', authors),
               ('content_types', content_types),
               ('printers', printers),
                )
    ret = []
    for tup in tuples:
        ret.append('')
        ret.append(tup[0])
        ret.append('=' * len(tup[0]))
        r = []
        for key in tup[1]:
            r.append(key)
        ret.extend(
            helpers.tabulate(r, alignment='<', max_width=120))
    return ret

def main():
    print("content.py has no syntax errors")
    which = content_types["for_testing"]
    lpr = "X6505"
    letter = letter_format(which, lpr)
    email = prepare_email_template(which)
    rec = dict(
        first = "First",
        last = "Last",
        address = "nnn An Ave.",
        town = "Any Town",
        postal_code = "CODE",
        state = "CA",
        country = "USA",
        extra = """A lot more junk:
Certainly nothing very serious!
Just a lot of junk.""",
        email = "myemail@provider.com",
        )
    print(letter.format(**rec))
    with open("letter2print", 'w') as fout:
        fout.write(helpers.indent(letter.format(**rec),
            ' ' * printers[lpr]['indent']))
    print(email)
    with open("email2print", 'w') as fout:
        fout.write(email.format(**rec))


duplicate_email_template = """From: rodandboatclub@gmail.com
To: {}
Subject: Which email is best?

Dear {},
Club records have two differing emails for you:
    "{}" and
    "{}" .
Please reply telling us which is the one you want the club to use.
Thanks in advance,
Membership"""


if __name__ == "__main__":
    print('\n'.join(choices()))
