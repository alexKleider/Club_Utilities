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
            "post_script": '',
            "func": "some_func", 
            "test": lambda record: True,
            "e_and_or_p": "one_only",
            },
    postal_headers - being redacted in favour of:
    printer_specs: X6505, HL2170, ...

Other items:
    email_header
    def prepare_letter(which_letter, printer_spec):
    def prepare_email(which_letter):
"""

import helpers

address_format = """{first} {last}
{address}
{town}, {state} {postal_code}
{country}"""

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
    yearly_fees_1st_request = """
The Club membership year ends in June and ideally we'd like to
have all dues and fees in by then.  If you are already paid up,
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
If there are any dues or fees outstanding, please pop your
check into an envelope asap payable and sent to the...
        Bolinas Rod and Boat Club
        PO Box 0248
        Bolinas, CA 94924
Please write 'membership' on the 'memo' line to help
avoid confusion.
{extra}""",
    yearly_fees_2nd_request = """
This is a second request being sent out to Club members whose
dues (and/or fees where applicable) for the upcoming (begining
July 1st) Club year have not yet been payed. You should also
note that this is the last notice you can expect to receive
before the late penalty (of $25) is imposed.

Please pop your check into an envelope asap payable and addressed
to the...
        Bolinas Rod and Boat Club
        PO Box 0248
        Bolinas, CA 94924
It would be helpful if you indicate 'membership' on the check
to avoid confusion.

Details are as follows:
{extra}""",
    penalty_notice = """
The deadline for Club Dues payment has passed.  Records indicate that
you are in arrears with regard to payment of Club dues and a late fee
of $25 is now applied in addition to the regular dues payment of $100.
If you feel this is incorrect, please speak up[1]- we are only human!
Otherwise, don't delay sending in your check.  The end of September
is when anyone who hasn't payed ceases to be a member.

Please pop your check (for $125) into an envelope asap payable and
addressed to the...
        Bolinas Rod and Boat Club
        PO Box 0248
        Bolinas, CA 94924""", 
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
As you may already know, the Club Executive approved your
application for Club membership at their last meeting.

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

email_header = """From: {}
To: {{email}}
Subject: {}

Dear {{first}} {{last}},"""

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
        # post_script:  an optional ps
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
        "post_script": '',
        "func": "some_func",
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    happyNY_and_0th_fees_request = {
        "subject": "Happy New Year from the Bolinas R&B Club",
        "from": authors["club"],
        "body": letter_bodies["happyNY_and_0th_fees_request"],
        "post_script": """
PS By the way, if/when you do pay, please send your remittance to
    The Bolinas Rod & Boat Club
    PO Box 248
    Bolinas, CA 94924
It's always a good idea to jot down 'club dues' on the check
in order to prevent any confusion.""",
        "func": "get_owing",
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    yearly_fees_1st_request = {
        "subject": "Bolinas R&B Club fees coming due",
        "from": authors["club"],
        "body": letter_bodies["yearly_fees_1st_request"],
        "post_script": '',
        "func": "get_owing",
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    yearly_fees_2nd_request = {
        "subject":"Second request for BR&BC dues",
        "from": authors["club"],
        "body": letter_bodies["yearly_fees_2nd_request"],
        "signature": '',
        "post_script": """
[1] rodandboatclub@gmail.com or a letter to the PO Box\n
[2] If the club has an email address on file for you, you'll be
receiving this by email as well as 'snail mail.'""",
        "func": "get_owing",
        "test": lambda record: True,
        "e_and_or_p": "both",
        },
    penalty_notice = {
        "subject":"BR&BC dues and penalty for late payment",
        "from": authors["club"],
        "body": letter_bodies["penalty_notice"],
        "post_script": """
[1] rodandboatclub@gmail.com or a letter to the PO Box\n
[2] If the club has an email address on file for you, you'll be
receiving this by email as well as 'snail mail.'""",
        "func": "get_owing",
        "test": lambda record: True,
        "e_and_or_p": "both",
        },
    new_applicant_welcome = {
        "subject": "Welcome to the Club",
        "from": authors["club"],
        "body": letter_bodies["new_applicant_welcome"],
        "post_script": '',
        "func": "std_mailing",
        "test": (
        lambda record: True if 'a1' in record["status"] else False),
        "e_and_or_p": "both",
        },
    request_inductee_payment = {
        "subject": "Welcome to the Bolinas Rod & Boat Club",
        "from": authors["club"],
        "body": letter_bodies["request_inductee_payment"],
        "post_script": '',
        "func": "request_inductee_payment",
        "test": (
        lambda record: True if 'i' in record["status"] else False),
        "e_and_or_p": "both",
        },
    welcome2full_membership = {
        "subject": "You are a member!",
        "from": authors["club"],
        "body": letter_bodies["welcome2full_membership"],
        "post_script": """
[1] (e)mail to rodandboatclub@gmail.com or PO Box 428, 94924""",
        "func": "std_mailing",
        "test": (
        lambda record: True if 'm' in record["status"] else False),
        "e_and_or_p": "both",
        },
    bad_email = {
        "subject": "non-working email",
        "from": authors["club"],
        "body": letter_bodies["bad_email"],
        "post_script": '',
        "func": "std_mailing",
        "test": (
        lambda record: True if 'be' in record["status"] else False),
        "e_and_or_p": "usps",
        }, 
    personal = {
        "subject": "Old Boys Dinner Reimbursement",
        "from": authors["ak"],
        "body": letter_bodies["personal"],
        "post_script": '',
        "func": "std_mailing",
        "test": (
        lambda record: True if 'p' in record["status"] else False),
        "e_and_or_p": "usps",
        }, 
    )
    # ... end of content_types.

printer_specs = dict(
    # Using tuples in case width will ever be needed.
    X6505 = dict(
        indent = 4,
        top = (1,),  # blank lines at top
        frm = (5, 25),  # return window
        date = (4,),  # between windows
        to = (7, 29),  # recipient window
        re = (3,),  # below window
        ),
    HL2170 = dict(
        indent = 3,
        top = (1,),  # blank lines at top
        frm = (5, 25),  # return window
        date = (4,),  # between windows
        to = (7, 29),  # recipient window
        re = (3,),  # below windows => fold
        ),
    other = dict(
        indent = 4,
        top = (1,),  # blank lines at top
        frm = (5, 25),  # return window
        date = (4,),  # between windows
        to = (7, 29),  # recipient window
        re = (3,),  # below windows => fold
        ),
    )
### ... end of printer_specs.

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

def prepare_letter(which_letter, printer_spec):
    """
    Prepares the template for a letter.
    Expect its parameters to be determined by 'globals'-
    probably set as command line arguments using docopt.
    <which_letter> is one of the <content_types>.
    <printer_specs> is one of the <printer_specs>
    Returns a 'letter' with formatting fields of <record>:
    typically {first}, {last}, {address}, {town}, {state},
    {postal_code}, {country}, and possibly (one or more) {extra}(s).
    """
    lpr = printer_specs[printer_spec]
    # top margin:
    ret = [""] * lpr["top"][0]
    # return address:
    ret_addr = address_format.format(**which_letter["from"])
    ret.append(expand(ret_addr, lpr['frm'][0]))
    # format string for date:
    ret.append(expand((helpers.get_datestamp()),lpr['date'][0]))
    # format string for recipient adress:
    ret.append(expand(address_format,lpr['to'][0]))
    # subject/Re: line
    ret.append(expand("Re: {}".format(which_letter["subject"]),
        lpr['re'][0]))
    # format string for salutation:
    ret.append("Dear {first} {last},\n")
    # body of letter (with or without {extra}(s))
    ret.append(which_letter["body"])
    # signarue:
    ret.append(which_letter["from"]["mail_signature"])
    # post script:
    ps = which_letter["post_script"]
    if ps:
        ret.append(ps)
    return '\n'.join(ret)

def prepare_email(which_letter):
    """
    Prepares the template for an email.
    """
    ret = [email_header.format(which_letter["from"]["email"],
                which_letter["subject"]),]
    ret.append(which_letter["body"])
    ret.append(which_letter["from"]["email_signature"])
    ps = which_letter["post_script"]
    if ps:
        ret.append(ps)
    return '\n'.join(ret)

if __name__ == "__main__":
    print("content.py has no syntax errors")
    which = content_types["for_testing"]
    lpr = "X6505"
    letter = prepare_letter(which, lpr)
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
            ' ' * printer_specs[lpr]['indent']))
    print(email)
    with open("email2print", 'w') as fout:
        fout.write(email.format(**rec))


