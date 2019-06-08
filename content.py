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
    authors: ak, club,
    content_types
        each provides: {
            "subject": 
            "from": authors["club"],
            "body": letter_bodies["happyNY_and_0th_fees_request"],
            "post_script": a string,
            "func": "some_func", 
            "test": lambda record: True,
            "e_and_or_p": "one_only",
            },
    postal_headers - being redacted in favour of:
    printers: X6505, HL2170, ...

Other items:
    email_header
    def letter_format(which_letter, printer):
    def prepare_email(which_letter):
"""

import helpers

address_format = """{first} {last}
{address}
{town}, {state} {postal_code}
{country}"""

email_header = """From: {}
To: {{email}}
Subject: {}

Dear {{first}} {{last}},"""

letter_bodies = dict(
    proto_content = """
Blah, Blah-
more Blah blah

etc

First extra content is
{extra}

May have as many 'extra's as required as long as each one
has a corresponding entry in the record dict (typically arranged
by the custom function.
""",

    happyNY_and_0th_fees_request = """
A very Happy New Year to all members of the Bolinas Rod & Boat
Club!

One of our resolutions is to do a better job of maintaining
the 'Membership' section of the Club web site:
(rodandboatclub.com, password is 'fish'.) 
Please check it out: click on 'Membership' and see if all
your data is as you would like it to be. Let us know of any
changes that should be made.

By the way, if you are getting this by post but have an email
address that you might be willing to share, we'd very much like
to switch you over to 'email_only' status.

At this time you might be doing some financial planning for the
year; don't forget to include provisions for payment of Club dues
(and possibly fees as well.)  The following is included to help
you in this regard.  It's always acceptable to pay early and get it
behind you.{extra}""",

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

While we've got your attention: please go to the Club web site
(rodandboatclub.com, password is 'fish',) click on 'Membership'
and check that all your data is as you would like it to be.
If you see anything not to your liking, let us know so corrections
can be made.

By the way, if you are getting this by post but have an email
address, we'd very much like to know about it and switch you
over to 'email_only' status.

A statement of your current standing appears bellow;
If there are any dues or fees outstanding, please don't delay.
If the total is zero (or negative) you're all paid up (or more than
paid up) and we thank you.
{{extra}}""".format(helpers.next_club_year()),

    yearly_fees_2nd_request = """
This is a second request being sent out to Club members whose
dues (and/or fees where applicable) for the upcoming (begining
July 1st) Club year have not yet been payed. You should also
note that this is the last notice you can expect to receive
before the late penalty (of $25) is imposed.

Details are as follows:
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

    approved_but_waiting_for_vacancy = """
The Club Executive has approved your application for Club
membership but unfortunately there is currently no vacancy
in the Club membership.  In the mean time you are welcome
to enjoy Club activities and participate as members do.

"Welcome aboard!"

I'll let you know once a vacancy opens up.  """,

    request_inductee_payment = """
The Club Executive has approved your application for Club
membership and there is currently a vacancy in the Club
membership.

"Welcome aboard!"

All that remains for your membership to take effect is payment
of dues.  Please send a check for ${current_dues} to the Club at
    PO Box 248
    Bolinas, CA 94924

Upon receipt of your membership dues, I'll send you more information
about the Club and your privileges as a member there of.""",

    welcome2full_membership = """
It is my pleasure to welcome you as a new member to the Bolinas Rod
and Boat Club!

You will now be receiving meeting minutes (via email) as prepared by
our Club Secretary Peter Pyle.

As you may know, the Club has its own web site: 'rodandboatclub.com'.
It is password protected; the password is 'fish' (a not very closely
guarded secret.)  By clicking on the "Membership" tab, you can find
all your fellow members along with contact information.  If you see
any inaccuracies there, please let me know [1] so corrections can be
made.

Members can (upon payment of a $10 deposit) get a key to the Club
from "keeper of the keys" Ralph Cammicia.  Many take advantage of
having this access to spend time on the balconey enjoying views of
the lagoon and Bolinas Ridge.  Please be sure to lock up upon leaving.

The Club is available for members to rent for private functions (if
certain conditions are met.)  More information can be found on the web
site: "Rules and Forms" and under that "Club Rentals".

Most important of all, come to meetings and other functions to enjoy
the comraderie!""",

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

    )
# ... end of letter_bodies.


post_scripts = dict(
    gmail_warning = """ If yours is a gmail account you'll get an alarming warning
that this email may not have come from the Rod and Boat Club.
It was sent through a different mail server, hence the automatic
notice from Google.  All is well.
""",

    remittance = """ By the way, if/when you do pay, please send your remittance to
    The Bolinas Rod & Boat Club
    PO Box 248
    Bolinas, CA 94924
It's always a good idea to jot down 'club dues' on the check
in order to prevent any confusion.""",

    ref1 = """ [1] rodandboatclub@gmail.com or PO Box 748, 94924""",
    )

authors = dict(
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
        mail_signature = "\nSincerely,\n\n\nAlex Kleider",
        ),
    club = dict(
        first = "Bolinas",
        last = "Rod & Boat Club",
        address = "PO Box 248",
        town = "Bolinas",
        state = "CA",
        postal_code = "94924",
        country = "USA",
        email_signature = "\nSincerely,\nAlex Kleider (Membership)",
        email = "rodandboatclub@gmail.com",
        mail_signature = "\nSincerely,\n\n\nAlex Kleider (Membership)",
        ),
    )  # ... end of authors.

# Need to assign one of the following content_types to the 
# Membership instance attribute 'content_type'.

    # Each item in the following dict specifies:
        # subject: re line in letter_bodies, subject line in emails
        # postal_header: to be assigned depending on which
        #     printer is to be used.
        #     (Or if sender is not the Club.)
        # body: text of the letter which may or may not have
        #     one or more 'extra' sections.
        # signature: a 'yours truely' + name.
        # post_scripts:  a list of optional ps
        # func: the Membership method used on each record.
        # test: a lambda function that determines if the record
        #     is to be considered at all.
        # e_and_or_p: send 'both' email and usps, 'usps' (mail only)
        #     or 'one_only' (email if available, othewise usps)
    # One of the following becomes the 'which' attribute
    # of a Membership instance.
content_types = dict(
    for_testing = {
        "subject": "This is a test.",
        "from": authors["ak"],
        "body": letter_bodies["proto_content"],
        "post_scripts": (post_scripts["gmail_warning"],),
        "func": "test_func",
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    happyNY_and_0th_fees_request = {
        "subject": "Happy New Year from the Bolinas R&B Club",
        "from": authors["club"],
        "body": letter_bodies["happyNY_and_0th_fees_request"],
        "post_scripts": (post_scripts["remittance"],),
        "func": "set_owing",
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    February_meeting = {
        "subject": "Change regarding format and time of next meeting",
        "from": authors["club"],
        "body": letter_bodies["February_meeting"],
        "post_scripts": (),
        "func": "std_mailing",
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    thank_you_for_advanced_payment = {
        "subject": "Thanks for your payment",
        "from": authors["club"],
        "body": letter_bodies["thank_you_for_advanced_payment"],
        "post_scripts": (),
        "func": "std_mailing",
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    thank_you_for_timely_payment = {
        "subject": "Thanks for your payment",
        "from": authors["club"],
        "body": letter_bodies["thank_you_for_timely_payment"],
        "post_scripts": (),
        "func": "std_mailing",
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    yearly_fees_1st_request = {
        "subject": "Bolinas R&B Club fees coming due",
        "from": authors["club"],
        "body": letter_bodies["yearly_fees_1st_request"],
        "post_scripts": (post_scripts["remittance"],),
        "func": "set_owing",
        "test": lambda record: False if (('a' in record["status"]) or
                ('w' in record["status"])) else True,
        "e_and_or_p": "one_only",
        },
    yearly_fees_2nd_request = {
        "subject":"Second request for BR&BC dues",
        "from": authors["club"],
        "body": letter_bodies["yearly_fees_2nd_request"],
        "signature": '',
        "post_scripts": (post_scripts["remittance"],
                    post_scripts["ref1"],),
        "func": "set_owing",
        "test": lambda record: helpers.is_member,
        "e_and_or_p": "one",
        },
    penalty_notice = {
        "subject":"BR&BC dues and penalty for late payment",
        "from": authors["club"],
        "body": letter_bodies["penalty_notice"],
        "post_scripts": (post_scripts["remittance"],
                    post_scripts["ref1"],),
        "func": "set_owing",
        "test": lambda record: helpers.is_member,
        "e_and_or_p": "both",
        },
    bad_email = {
        "subject": "non-working email",
        "from": authors["club"],
        "body": letter_bodies["bad_email"],
        "post_scripts": (),
        "func": "std_mailing",
        "test": (
        lambda record: True if 'be' in record["status"] else False),
        "e_and_or_p": "usps",
        }, 
    new_applicant_welcome = {
        "subject": "Welcome to the Club",
        "from": authors["club"],
        "body": letter_bodies["new_applicant_welcome"],
        "post_scripts": (),
        "func": "std_mailing",
        "test": (
        lambda record: True if 'a0' in record["status"] else False),
        "e_and_or_p": "both",
        },
    request_inductee_payment = {
        "subject": "Welcome to the Bolinas Rod & Boat Club",
        "from": authors["club"],
        "body": letter_bodies["request_inductee_payment"],
        "post_scripts": (),
        "func": "request_inductee_payment",
        "test": (
        lambda record: True if 'ai' in record["status"] else False),
        "e_and_or_p": "both",
        },
    welcome2full_membership = {
        "subject": "You are a member!",
        "from": authors["club"],
        "body": letter_bodies["welcome2full_membership"],
        "post_scripts": (post_scripts["ref1"], ),
        "func": "std_mailing",
        "test": (
        lambda record: True if 'm' in record["status"] else False),
        "e_and_or_p": "both",
        },
    personal = {
        "subject": "Old Boys Dinner Reimbursement",
        "from": authors["ak"],
        "body": letter_bodies["personal"],
        "post_scripts": (),
        "func": "std_mailing",
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
        "func": "std_mailing",
        "test": (
        lambda record: True if 'TPMG' in record["first"] else False),
        "e_and_or_p": "usps",

        },
    )
    # ... end of content_types.

printers = dict(
    # tuples in the case of windows.
    X6505 = dict(
        indent = 4,
        top = 1,  # blank lines at top
        frm = (5, 25),  # return window
        date = 4,  # between windows
        to = (7, 29),  # recipient window
        re = 3,  # below window
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
    )
### ... end of printers (dict specifying printer being used.)

def expand(content, nlines):
    """
    Takes <content> which can be a list of strings/lines
    or all one string (with line feeds separating lines,)
    and returns the same type (either string or list) but
    containing nlines.
    Fails if <content> has more than nlines.
    """
    isstring = False
    if isinstance(content, str):
        isstring = True
        content = content.split("\n")
    if len(content) > nlines:
        print("Error: too many lines in <content>!")
        assert False
    while nlines > len(content):
        if nlines - len(content) >= 2:
            content = [''] + content + ['']
        else:
            content.append('')
    if isstring:
        return '\n'.join(content)
    else:
        return content

def get_postscripts(which_letter):
    """
    Returns a list of lines representing the post scripts
    """
    ret = []
    n = 0
    for post_script in which_letter["post_scripts"]:
        ret.append("\n" + "P"*n + "PS" + post_script)
        n += 1
    return ret

def letter_format(which_letter, printer):
    """
    Prepares the template for a letter.
    <which_letter> is one of the <content_types> and
    <printer> specifies which printer is to be used-
    one of the keys to the <printers> dict.
    Both are found in this module.
    Returns a 'letter' with formatting fields of <record>:
    typically {first}, {last}, {address}, {town}, {state},
    {postal_code}, {country}, and possibly (one or more) {extra}(s).
    """
    lpr = printers[printer]
    # top margin:
    ret = [""] * lpr["top"]
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

def prepare_email(which_letter):
    """
    Prepares the template for an email.
    """
    ret = [email_header.format(which_letter["from"]["email"],
                which_letter["subject"]),]
    ret.append(which_letter["body"])
    ret.append(which_letter["from"]["email_signature"])
    ret.extend(get_postscripts(which_letter))
    return '\n'.join(ret)

if __name__ == "__main__":
    print("content.py has no syntax errors")
    which = content_types["for_testing"]
    lpr = "X6505"
    letter = letter_format(which, lpr)
    email = prepare_email(which)
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


