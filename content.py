#!/usr/bin/env python

# File: content.py

"""
A module to support the utils.py prepare_mailing command.

Custom methods are imported as first class objects from the
utils.Membership class.
"""
import sys
import utils

letters = dict(
    proto_content = """
Blah, Blah-
more Blah blah

etc

First extra content is
{extra0}

May have as many 'extras' as required as long as each one
is defined by the custom function
the content dict.  i.e. {extra1}

Sincerely,
Alex Kleider (Membership)
""",
    happyNY_and_0th_fees_request = """

A very Happy New Year to all members of the Bolinas Rod & Boat
Club!

One of our resolutions is to do a better job of maintaining
the 'Membership' section of the Club web site:
(rodandboatclub.com, password is 'fish',) click on 'Membership'
and check that all your data is as you would like it to be.
If you see anything not to your liking, let us know of any
changes you'd like to see made.  You can reply either by email
(if you are receiving this as an email) or by post (94924-0248).
By the way, if you are getting this by post but have an email
address, we'd very much like to switch you over to 'email_only'
status.

At this time you might be doing some financial planning for the
year; don't forget to include provisions for payment of Club dues
(and possible fees as well.)  The following is included to help
you in this regard.  It's always acceptable to pay early and get it
behind you.{extra}

Sincerely,
Alex Kleider (Membership)

PS If/when you do pay, please send your remittance to
    The Bolinas Rod & Boat Club
    PO Box 248
    Bolinas, CA 94924
It's always a good idea to jot down 'club dues' on the check
in order to prevent any confusion.""",
    yearly_fees_1st_request = """

With July comes the beginning of the new membership year
and ideally we'd like to have all dues and fees in by then.
If you are already paid up, the Club thanks you.

While we've got your attention: please go to the Club web site
(rodandboatclub.com, password is 'fish',) click on 'Membership'
and check that all your data is as you would like it to be.
If you see anything not to your liking, let us know of any
changes you'd like to see made.  You can reply either by email
(if you are receiving this as an email) or by post to the
address provided below.  By the way, if you are getting this
by post but have an email address, we'd very much like to 
know about it and switch you over to 'email_only' status.

A statement of your current standing will appear bellow;
If there are any dues or fees outstanding, please pop your
check into an envelope asap payable and sent to the...
        Bolinas Rod and Boat Club
        PO Box 0248
        Bolinas, CA 94924
{extra}

Sincerely,
Alex Kleider (Membership)""",
    yearly_fees_2nd_request = """
August is upon us and that is when the Club imposes a penalty
for late payment of dues.

Records indicate that you are in arrears.  If you feel this
is incorrect, please speak up[1]- we are only human!
Otherwise, don't delay sending in your check.  The end of
September is when anyone who hasn't payed ceases to be a member.

Because this is the first year we've been sending notices by email,
Club leadership has determined that before late fees are imposed, at
least one posted notice should be sent out[2] so for this year only,
late fees will not be imposed until after the fishing derby coming
up later this month.

Please pop your check into an envelope asap payable and addressed
to the...
        Bolinas Rod and Boat Club
        PO Box 0248
        Bolinas, CA 94924

Details are as follows:
{extra1}

Sincerely,
Alex Kleider (Membership)

[1] rodandboatclub@gmail.com or a letter to the PO Box

[2] If the club has an email address on file for you, you'll be
receiving this by email as well as 'snail mail.' """,
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
        Bolinas, CA 94924

Sincerely,
Alex Kleider (Membership)

[1] rodandboatclub@gmail.com or a letter to the PO Box

[2] If the club has an email address on file for you, you'll be
receiving this by email as well as 'snail mail.' """, 
    bad_email = """
An email sent to you at the following email address:
    "{email}"
was rejected.  Can you please help us sort this out by
contacting us at rodandboatclub@gmail.com?

Thanks,

Alex Kleider (Membership)""",
    new_applicant_welcome = """
As Membership Chair it is my pleasure to welcome you as a new
applicant for membership in the Bolinas Rod and Boat Club.

Please come and enjoy the meetings (first Fiday of each month.)
To become eligible for membership (and not waste your application
fee) you must attend a minimum of three meetings with in the six
month period beginning the date your application was received. 

Sincerely,
Alex Kleider (Membership)""",
    request_inductee_payment = """
As you may already know, the Club Executive approved your
application for Club membership at their last meeting.

"Welcome aboard!"

All that remains for your membership to take effect is payment
of dues.  Please send a check for ${current_dues} to the Club at
    PO Box 248
    Bolinas, CA 94924

Upon receipt of your membership dues, I'll send you more information
about the Club and your privileges as a member there of.


Sincerely,
Alex Kleider (Membership)""",
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
the comraderie!


Sincerely,
Alex Kleider (Membership)


[1] (e)mail to rodandboatclub@gmail.com or PO Box 428, 94924""",
    )

postal_headers = {    # Printers vary in spacing!
    # ... so this dict provides an easy way to set spacing to suit.
    # "6505" == Xerox WorkForce 6505 in the Bolinas data closet.
    "6505": """

Bolinas Rod and Boat Club
PO Box 248
Bolinas, CA 94924



{date}



{first} {last}
{address}
{town}, {state} {zip}




Re: {subject}

Dear {first} {last},
""",
    # "Janice" == Janice's printer.
    "Janice": """
""",
    }  # ... end of postal_headers

email_header = """From: rodandboatclub@gmail.com
To: {email}
Subject: {subject}

Dear {first} {last},

"""
# Need to assign one of the following content_types to the 
# Membership instance attribute 'content_type'.

content_types = dict(
    # Each item in this dict specifies:
        # subject: re line in letters, subject line in emails
        # the email_header: the same for all emails
        # postal_header: to be assigned depending on which
        #     printer is to be used.
        # body: text of the letter which may or may not have
        #     one or more 'extra' sections.
        # func: the Membership method used on each record.
        # test: a lambda function that determines if the record
        #     is to be considered at all.
        # e_and_or_p: send 'both' email and usps, 'usps' (mail only)
        #     or 'one_only' (email if available, othewise usps)
    # One of the following becomes the 'which' attribute
    # of a Membership instance.
    happyNY_and_0th_fees_request = {
        "subject": "Happy New Year from the Bolinas R&B Club",
        "email_header": email_header,
#       "postal_header": None,  # Depends on printer to be used.
        "body": letters["happyNY_and_0th_fees_request"],
        "func": utils.Membership.get_owing,
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    yearly_fees_1st_request = {
        "subject": "Bolinas R&B Club fees coming due",
        "email_header": email_header,
#       "postal_header": None,  # Depends on printer to be used.
        "body": letters["yearly_fees_1st_request"],
        "func": utils.Membership.get_owing,
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    yearly_fees_2nd_request = {
        "subject":"Second request for BR&BC dues",
        "email_header": email_header,
#       "postal_header": None,
        "body": letters["yearly_fees_2nd_request"],
        "func": utils.Membership.get_owing,
        "test": lambda record: True,
        "e_and_or_p": "both",
        },
    penalty_notice = {
        "subject":"BR&BC dues and penalty for late payment",
        "email_header": email_header,
#       "postal_header": None,
        "body": letters["penalty_notice"],
        "func": utils.Membership.get_owing,
        "test": lambda record: True,
        "e_and_or_p": "both",
        },
    new_applicant_welcome = {
        "subject": "Welcome to the Club",
        "email_header": email_header,
#       "postal_header": None,
        "body": letters["new_applicant_welcome"],
        "func": utils.Membership.std_mailing,
        "test": (
        lambda record: True if 'a1' in record["status"] else False),
        "e_and_or_p": "both",
        },
    request_inductee_payment = {
        "subject": "Welcome to the Bolinas Rod & Boat Club",
        "email_header": email_header,
#       "postal_header": None,
        "body": letters["request_inductee_payment"],
        "func": utils.Membership.request_inductee_payment,
        "test": (
        lambda record: True if 'i' in record["status"] else False),
        "e_and_or_p": "both",
        },
    welcome2full_membership = {
        "subject": "You are a member!",
        "email_header": email_header,
#       "postal_header": None,
        "body": letters["welcome2full_membership"],
        "func": utils.Membership.std_mailing,
        "test": (
        lambda record: True if 'm' in record["status"] else False),
        "e_and_or_p": "both",
        },
    bad_email = {
        "subject": "non-working email",
        "email_header": email_header,
#       "postal_header": None,
        "body": letters["bad_email"],
        "func": utils.Membership.std_mailing,
        "test": (
        lambda record: True if 'be' in record["status"] else False),
        "e_and_or_p": "usps",
        }, 
    )

if __name__ == "__main__":
    print("content.py has no syntax errors")

