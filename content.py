#!/usr/bin/env python

# File: content.py

"""
A module to support the utils.py prepare_mailing command.
(... and also the emailing command.)

Rather than importing functions, they are refered to by
name and depend on a dict within the utils.Membership class
with those names as keys and the methods as values.

A number of 'dict's are being used:
    letter_bodies   Marked by 'b'
    authors: ak, membership,   Marked by 'a'
    content_types   Marked by 'c'
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
    func: prepare_letter_template(which_letter, printer):
    func: prepare_email_template(which_letter):

Printing Letters:
Both the printer and the windowed envelope being used must be taken
into consideration.
"""

import helpers
import member
import rbc

address_format = """{first} {last}
{address}
{town}, {state} {postal_code}
{country}"""

custom_lambdas = dict(
    QuattroSolar=(lambda record: True if 'Quattro Solar' in
                  record["company"] else False),
    MarinMechanical=(lambda record: True if 'Marin Mechanical'
                     in record["company"] else False),)


letter_bodies_docstring = """
Some of these 'bodies' are subject to the format method
and those must have {{double}} parens for the format fields
that must be subsequently filled in by the '..._funcs'.
"""

# # single braces are for fields populated by the content_type data.
# # double braces fields are populated by the record data.
letter_bodies = dict(

    bill_payment="""
Please find enclosed payment.
""",

    for_testing="""
Blah, Blah-
more Blah blah

etc

First extra content is
{extra}

May have as many 'extra's as required as long as each one
has a corresponding entry in the record dict (typically arranged
by the custom function.
""",

    bad_address="""
We have your mailing address as :

{extra}

but mail sent to that address has been returned.

Please let us know a working postal address so records
can be updated.[1]
""",

    meeting_announcement="""
Board members meet at 6pm.
General meeting scheduled for 7:30pm.
Come for the fun!
""",

    feb_meeting="""

We have a special Bolinas Rod and Boat Club meeting coming up
{}.

Board members meet at 5pm.

The general meeting is scheduled for 6:00pm.
Election of Officers is the main agenda item.

Those with reservations[1]  are invited to stay for the
annual dinner to follow.

Come for the fun!
""".format(helpers.next_first_friday()),

    usps_minutes="""
Enclosed, please find the latest Club minutes.
Enjoy!
""",

    happyNY_and_0th_fees_request="""
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

    thank="""
This acknowledges receipt of your recent ${payment} payment.
Thank you.

A statement of your current standing follows:
{extra}

All the best!
""",

    # Correction!!!
    correction="""
You recently received a statement of dues for the upcoming
({}) Club year. I believe the total was in error and the
corrected amount is indicated below.  You can pay it any
time although it isn't due until June.

If you have reason to believe this is in error, please let
me know[1].

My apologies for the confusion (caused by my ineptitude!)
{{extra}}""".format(helpers.club_year(which='next')),



    # Send with March, April, and May minutes:
    first_notice="""
This is a reminder that annual Club dues will be due in June.
That is still a ways out but some might like to know in advance
in order to be able to budget appropriately.  Advance warning
also benefits those that might be planning to be away for the
summer.

A statement of your dues (+/- fees) for the upcoming ({}) Club
year appears bellow.  (If you've any reason to believe that
our accounting might be in error, please let us know[1].)
If the total is zero (or negative) you're all paid up (or more
than paid up) for the upcoming year and we thank you.
{{extra}}""".format(helpers.club_year(which='next')),

    # Send with June minutes:
    June_request="""
The final month of this ({}) Club year is now upon us
and annual dues (and fees where applicable) are due at the end
of the month.

This mailing is going out to all members so everyone can know
where they stand whether already paid up or not.

(If you've any reason to believe that our accounting might be
in error, please let it be known[1].)

Details are as follows:
{{extra}}""".format(helpers.club_year(which='this')),

    July_request="""
The new ({}) Club year has begun. Please send in your dues
(and any applicable fees) to the Bolinas Rod and Boat Club,
PO Box 248, Bolinas, CA 94924.

(If you've any reason to believe that our accounting might be
in error, please let it be known[1].)

Details are as follows:
{{extra}}""".format(helpers.club_year(which='this')),

    interim_request="""
Club records indicate that you still have dues (and/or
applicable fees) outstanding as follows...

{extra}

If you've any reason to believe that our accounting might be
in error, please let it be known[1]. Otherwise, please send
in your remittance to the
    Bolinas Rod and Boat Club,
    PO Box 248, Bolinas, CA 94924.
at your earliest convenience.
""",

    # Send with August minutes:
    penultimate_warning="""
Club records indicate that your dues (+/- other fees) have
as yet not been paid.  Please be aware that according to
Club bylaws, membership lapses if fees are not paid by Sept 1st.
(If you've any reason to believe that our accounting might be in
error, please let us know[1].)

Please pay promptly; we'd hate to loose you as a member.

Details follow.
{extra}""",

    # Send towards end of August:
    final_warning="""
Club records indicate that your dues (+/- other fees) have
as yet not been paid.  Please be aware that according to
Club bylaws, membership lapses if fees are not paid by Sept 1st.
(If you've any reason to believe that our accounting might be in
error, please let us know[1].)

Please pay promptly; we'd hate to loose you as a member.

Details follow.
{extra}""",

    # Penalties are not levied! Don't send!
    penalty_notice="""
The deadline for Club Dues payment has passed and records indicate
that you are in arrears so a late fee of $25 has been applied.
If you feel this is incorrect, please speak up[1]- we are only
human!  Otherwise, don't delay sending in your check rather than
risk being removed from the Club's list of members.

Details are as follows:
{extra}""",

    covid_final_notice="""
Club records indicate that you have not yet paid Club dues for the
current ({}) membership year.  If you no longer wish to be a
member, no further action is necessary (although we would like to hear
explicitly if that is your choice,) otherwise, please send in payment
which must be received before the end of this month if you are to
remain a member.
{{extra}}
If you would like to remain a member but are unable to make payment
because of financial hardship imposed by the pandemic, please let us
know; the Executive Committee is very concerned about, and wants to
consider, any such cases.

Sincerely,""".format(helpers.club_year(which='this')),

    bad_email="""
Emails sent to you at
    "{email}"
are being rejected.

Can you please help sort this out by contacting us
at rodandboatclub@gmail.com?

Thanks,""",

    new_applicant_welcome="""
As Membership Chair it is my pleasure to welcome you as a new
applicant for membership in the Bolinas Rod and Boat Club.

Please come and enjoy the meetings held on the first Fiday of
each month. Meetings are scheduled to begin at 7:30 pm (except
for the February special dinner meeting which begins at 6pm.)

To become eligible for membership (and not waste your application
fee) you must attend a minimum of three meetings with in the six
month period beginning the date your application was received.""",

    covid_welcome="""
As Membership Chair it is my pleasure to welcome you as a new
applicant for membership in the Bolinas Rod and Boat Club.

The following is part of what used to be the welcoming text
but unfortunately all meetings have been suspended during the
pandemic.

'''
Please come and enjoy the meetings held on the first Fiday of
each month. Meetings are scheduled to begin at 7:30 pm (except
for the February special dinner meeting which begins at 6pm.)

To become eligible for membership (and not waste your application
fee) you must attend a minimum of three meetings with in the six
month period beginning the date your application was received.
'''

Meetings are now being held virtually. The Club Secretary will be
sending you announcements.

Stay safe and let's all hope for more social times in the future!""",

    awaiting_vacancy="""
The Club Executive Committee has, at its last meeting,
approved your application for Club membership.

Unfortunately there is not currently a vacancy (since club
bylaws specify that membership must not be over 200.)

But don't dispair!  You are certainly welcome to enjoy most
if not all of the privileges of membership until a vacancy
occurs at which time I will send you a request for payment of
dues and once paid you will become a full fledged member!

You're almost there; as good as for all intense and purposes!""",

    request_delayed_inductee_payment="""
It's my pleasure to report that a vacancy has come up and so
you can now become a member.

"Welcome aboard!"

All that remains for your membership to take effect is payment
of dues.  Please send a check for ${current_dues} to the Club
(address provided below.)

Upon receipt of your membership dues, I'll send you more information
about the Club and your privileges as a member there of.""",

    request_inductee_payment="""
The Club Executive Committee has, at its last meeting,
approved your application for Club membership.

"Welcome aboard!"

All that remains for your membership to take effect is payment
of dues.  Please send a check for ${current_dues} to the Club
(address provided below.)

Upon receipt of your membership dues, I'll send you more information
about the Club and your privileges as a member there of.""",

    second_request_inductee_payment="""
Your application for Club membership was approved by the
Club Executive Committee at its last meeting and membership
fees have been requested but as yet not received.  Until
payment is received you are not yet a member.  This could
create a problem for the Exec committee since there are applicants
ready to take the spot that you would take if, but only if, the
dues are paid.  The Committee meets in less than a week!

Please send a check for ${current_dues} to the Club
(address provided below.)""",


    welcome2full_membership="""
It is my pleasure to welcome you as a new member to the Bolinas Rod
and Boat Club!

You will be receiving meeting minutes (via email) as prepared by
our Club Secretary Ed Mann.

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

    expired_application="""
It's been more than six months since your membership application has
been received which makes it now expired.  If you still wish to be a
member of the Bolinas Rod and Boat Club the application process must
begin again.""",

    retirement_from_club="""
Your wish to retire from Club membership has been noted.

I know I speak for all members in saying we're sorry to see you go
and wish you all the best in the future.""",

    membership_termination="""
Regretably the Club Executive Committee has been obliged to
terminate your membership because of non payment of dues.

Let me add my own personal sentiment of regret that you have
chosen to leave the club.

I've been asked that you return the club house key that you
got from Ralph.  A stamped addressed envelope has been included
for your convenience.""",

    cover_letter="""
Enclosed you'll find minutes of the Bolinas Rod and Boat Club.""",

    personal="""
The enclosed came to the Club PO Box along with an application.
Obviously it is in error. Since your name is on it I thought
best to send it on to you rather than to Herbert.

I hope this finds you well.
""",

    fromSecretary="""
Enjoy the minutes!
Michael Rafferty, Secretary
""",

    tpmg_social_security="""
Please find enclosed the documentation I believe you require from the
Social Security Administration concerning Medicare deductions for both
my wife and for me.
""",

    fromRandy="""
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

    payment="""
Thank you for your services.
"""
    )
# ... end of letter_bodies.


post_scripts = dict(

    at_request_of_secretary=(
        """ Sent at the request of {}, Secretary"""
        .format(rbc.Club.SECRETARY)),

    remittance=""" Please send remittances to:
    The Bolinas Rod & Boat Club
    PO Box 248
    Bolinas, CA 94924
It's always a good idea to jot down 'club dues' on
the check in order to prevent any confusion.""",

    ref1_email_or_PO="""[1] rodandboatclub@gmail.com or PO Box 248, 94924""",

    ref1_reservations="""[1] Reservations can be made through Anna Gade
    (uc_anna@sbcglobal.net.)""",

    covid19="""Because of the current pandemic, the Club is closed
    and in person meetings are suspended. Virtual meetings are still
    bing held and you'll be receiving notices.
    Let's hope for an early return to 'buisness as usual.'
    Stay safe; Stay well.""",

    forgive_duplicate="""This may be a duplication of an email
    already sent in which case please forgive.""",

    )

authors_DOCSTRING = """   ## NOTE ##
A "Sender:" field, determined by the --mta is added to each email at
the time it is sent.  The value of the 'email' field is entered into
the 'From: ' header of the email. A "reply2" field is also available.
"""

authors = dict(  # from
    bc=dict(  # AK in British Columbia
        first="Alex",
        last="Kleider",
        address="3727 Cavin Rd.",
        town="Duncan",
        state="BC",
        postal_code="V9L 6T2",
        country="Canada",
        email_signature="\nSincerely,\nAlex Kleider",
        email="akleider@sonic.net",
        reply2="akleider@sonic.net",
        mail_signature="\nSincerely,\n\n\nAlex Kleider",
        ),
    ak=dict(  # AK in Bolinas
        first="Alex",
        last="Kleider",
        address="PO Box 277",
        town="Bolinas",
        state="CA",
        postal_code="94924",
        country="USA",
        email_signature="\nSincerely,\nAlex Kleider",
        email="akleider@sonic.net",
        reply2="akleider@sonic.net",
        mail_signature="\nSincerely,\n\n\nAlex Kleider",
        ),
    membership=dict(  # Membership Chair
        first="Bolinas",
        last="Rod & Boat Club",
        address="PO Box 248",
        town="Bolinas",
        state="CA",
        postal_code="94924",
        country="USA",
        email_signature="\nSincerely,\nAlex Kleider (Membership)",
        email="rodandboatclub@gmail.com",
        reply2="rodandboatclub@gmail.com",
        mail_signature="\nSincerely,\n\n\nAlex Kleider (Membership)",
        ),
    secretary=dict(   # Club Secretary
        first="Bolinas",
        last="Rod & Boat Club",
        address="PO Box 248",
        town="Bolinas",
        state="CA",
        postal_code="94924",
        country="USA",
        email_signature=(
            "\nSincerely,\nMichael Rafferty (Club Secretary)"),
        email="rodandboatclub@gmail.com",
        reply2="rodandboatclub@gmail.com",
        mail_signature=(
            "\nSincerely,\n\n\nMichael Rafferty (Club Secretary)"),
        ),
    randy=dict(  # Randy Rush in Bolinas Home
        first="Randy",
        last="Rush",
        address="15 Rafael Ave.",
        town="Bolinas",
        state="CA",
        postal_code="94924",
        country="USA",
        email_signature="\nSincerely,\nRandy Rush",
        email='rodandboatclub@gmail.com',
        #       email="alex@kleider.ca",
        reply2='randolph@sonic.net',
        mail_signature="\nSincerely,\n\n\nRandy Rush",
        ),
    )  # ... end of authors.

# One of the following content_types is assigned to the 'which'
# attribute of an instance of utils.Club for mailing purposes.
#
#   # Each item in the following dict specifies:
#       # subject: re line in letter_bodies, subject line in emails
#       # from: expect a value from the 'authors' dict
#       #     each value is itself a dict specifying more info...
#       #     names, address, signatures, reply to, ..
#       # body: text of the letter which may or may not have
#       #     one or more 'extra' sections.
#       # post_scripts:  a list of optional postscripts
#       # funcs: a list of functions used on each record during
#       #     the data gathering traversal of the membership csv.
#       # test: a (usually 'lambda') function that determines
#       #     if the record is to be considered at all.
#       # e_and_or_p: possibilities are:
#       #     'both' email and usps,
#       #     'email' email only,
#       #     'usps' mail only,
#       #  or 'one_only' email if available, othewise usps.
#   # One of the following becomes the 'which' attribute
#   # of a Membership instance.

content_types = dict(  # which_letter
    # ## If a 'salutation' key/value is provied for any of the
    # ## following, the value will be used as the salutation
    # ## instead of a 'Dear {first} {last},' line.
    # ## The first 4 listed values for each are used for first
    # ## stage formatting.
    for_testing={
        "subject": "This is a test.",
        "from": authors["ak"],
        "body": letter_bodies["for_testing"],
        "post_scripts": ('forgive_duplicate',),
        "funcs": [member.testing_func, ],
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    bad_address={
        "subject": "Address correction requested.",
        "from": authors["membership"],
        "body": letter_bodies["bad_address"],
        "post_scripts": (post_scripts["ref1_email_or_PO"],),
        "funcs": [member.bad_address_mailing_func, ],
        "test": member.letter_returned,
        "e_and_or_p": "email",
        },
    bill_payment={
        "subject": "Payment of Invoice.",
        "from": authors["bc"],
        "body": letter_bodies["bill_payment"],
        "post_scripts": (),
        "funcs": [member.std_mailing_func, ],
        "test": lambda record: True,
        "e_and_or_p": "usps",
        },
    meeting_announcement={
        "subject": "Meeting Friday",
        "from": authors["secretary"],
        "body": letter_bodies["meeting_announcement"],
        "post_scripts": (),
        "funcs": (member.std_mailing_func,),
        "test": lambda record: True if record["email"] else False,
        "e_and_or_p": "one_only",
        },
    feb_meeting={
        "subject": "Meeting first Friday of February",
        "from": authors["membership"],
        "body": letter_bodies["feb_meeting"],
        "post_scripts": (
            post_scripts['ref1_reservations'],
            ),
        "funcs": (member.std_mailing_func,),
        "test": lambda record: True if record["email"] else False,
        "e_and_or_p": "email",
        },
    usps_minutes={
        "subject": "Rod & Boat Club Minutes",
        "from": authors["secretary"],
        "body": letter_bodies["usps_minutes"],
        "post_scripts": (),
        "funcs": (member.std_mailing_func,),
        "test": lambda record: False if record["email"] else True,
        "e_and_or_p": "usps",
        },
    happyNY_and_0th_fees_request={
        "subject": "Happy New Year from the Bolinas R&B Club",
        "from": authors["membership"],
        "body": letter_bodies["happyNY_and_0th_fees_request"],
        "post_scripts": (
            post_scripts["remittance"],
            ),
        "funcs": (member.assign_statement2extra_func,
                  member.std_mailing_func),
        "test": lambda record: False if ('r' in record['status']
                                         ) else True,
        "e_and_or_p": "one_only",
        },
    thank={
        "subject": "Thanks for your payment",
        "from": authors["membership"],
        "body": letter_bodies["thank"],
        "post_scripts": (),
        "funcs": (
                member.thank_func,
                ),
        "test": lambda record: True,
        "e_and_or_p": "one_only",
        },
    correction={
        "subject": "Corrected fees statement",
        "from": authors["membership"],
        "body": letter_bodies["correction"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            ),
        "funcs": (member.assign_statement2extra_func,
                  member.std_mailing_func),
        "test": lambda record: True if (
            member.is_member(record) and
            member.not_paid_up(record) and
            not ('w' in record["status"])
            ) else False,
        "e_and_or_p": "one_only",
        },
    first_notice={
        "subject": "Bolinas R&B Club fees coming due",
        "from": authors["membership"],
        "body": letter_bodies["first_notice"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            ),
        "funcs": (member.assign_statement2extra_func,
                  member.std_mailing_func),
        "test": lambda record: True if (
            (member.is_member(record) or
             member.is_inductee(record)) and
            # member.not_paid_up(record) and
            not member.is_non_fee_paying(record)
            ) else False,
        "e_and_or_p": "one_only",
        },
    June_request={
        "subject": "Bolinas R&B Club dues",
        "from": authors["membership"],
        "body": letter_bodies["June_request"],
        "signature": '',
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            ),
        "funcs": (member.assign_statement2extra_func,
                  member.std_mailing_func),
        "test": lambda record: True if (
            member.is_member(record) and
            not ('r' in record["status"]) and
            not ('w' in record["status"])
            and not ('r' in record['status'])
            ) else False,
        "e_and_or_p": "one_only",
        },
    July_request={
        "subject": "Bolinas R&B Club dues",
        "from": authors["membership"],
        "body": letter_bodies["July_request"],
        "signature": '',
        "post_scripts": (
            post_scripts["ref1_email_or_PO"],
            ),
        "funcs": (member.assign_statement2extra_func,
                  member.std_mailing_func),
        "test": lambda record: True if (
            member.is_fee_paying_member(record) and
            member.not_paid_up(record)
            ) else False,
        "e_and_or_p": "one_only",
        },
    interim_request={
        "subject": "Bolinas R&B Club dues",
        "from": authors["membership"],
        "body": letter_bodies["interim_request"],
        "signature": '',
        "post_scripts": (
            post_scripts["ref1_email_or_PO"],
            ),
        "funcs": (member.assign_statement2extra_func,
                  member.std_mailing_func),
        "test": lambda record: True if (
            member.is_fee_paying_member(record) and
            member.not_paid_up(record)
            ) else False,
        "e_and_or_p": "one_only",
        },
    penultimate_warning={
        "subject": "Membership soon to expire",
        "from": authors["membership"],
        "body": letter_bodies["penultimate_warning"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            ),
        "funcs": (member.assign_statement2extra_func,
                  member.std_mailing_func),
        "test": lambda record: True if (
            member.is_fee_paying_member(record) and
            member.not_paid_up(record)
            ) else False,
        "e_and_or_p": "one_only",
        },
    final_warning={
        "subject": "Membership soon to expire",
        "from": authors["membership"],
        "body": letter_bodies["final_warning"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            ),
        "funcs": (member.assign_statement2extra_func,
                  member.std_mailing_func),
        "test": lambda record: True if (
            member.is_fee_paying_member(record) and
            member.not_paid_up(record)
            ) else False,
        "e_and_or_p": "both",
        },
    penalty_notice={      # Penalties are not levied! Don't send!
        "subject": "BR&BC dues and penalty for late payment",
        "from": authors["membership"],
        "body": letter_bodies["penalty_notice"],
        "post_scripts": (
            post_scripts["remittance"],
            post_scripts["ref1_email_or_PO"],
            ),
        "funcs": (member.assign_statement2extra_func,
                  member.std_mailing_func),
        "test": (lambda record: True if
                 (member.is_member(record) and
                  member.not_paid_up(record) and
                  not ('w' in record["status"])
                  and not ('r' in record['status'])
                  ) else False),
        "e_and_or_p": "both",
        },
    covid_final_notice={
        "subject": "BR&BC final notice",
        "from": authors["membership"],
        "body": letter_bodies["covid_final_notice"],
        "post_scripts": (
            post_scripts["remittance"],
            ),
        "funcs": (member.assign_statement2extra_func,
                  member.std_mailing_func),
        "test": (lambda record: True if
                 (member.is_member(record) and
                  member.dues_owing(record) and
                  not ('w' in record["status"])
                  and not ('r' in record['status'])
                  ) else False),
        "e_and_or_p": "both",
        },
    bad_email={
        "subject": "non-working email",
        "from": authors["membership"],
        "body": letter_bodies["bad_email"],
        "post_scripts": (),
        "funcs": (member.std_mailing_func,),
        "test": (lambda record: True if
                 'be' in record["status"].split(member.SEPARATOR)
                 else False),
        "e_and_or_p": "usps",
        },
    new_applicant_welcome={
        "subject": "Welcome to the Club",
        "from": authors["membership"],
        "body": letter_bodies["new_applicant_welcome"],
        "post_scripts": (post_scripts["covid19"],),
        "funcs": (member.std_mailing_func,),
        "test": (lambda record: True if
                 (record["status"]
                  and 'a0' in record["status"].split("|"))
                 else False),
        "e_and_or_p": "one_only",
        },
    covid_welcome={
        "subject": "Welcome to the Club",
        "from": authors["membership"],
        "body": letter_bodies["covid_welcome"],
        "post_scripts": (),
        "funcs": (member.std_mailing_func,),
        "test": (lambda record:
            True if member.is_new_applicant(record)
            else False),
        "e_and_or_p": "one_only",
        },
    awaiting_vacancy={
        "subject": "Membership pending vacancy",
        "from": authors["membership"],
        "body": letter_bodies["awaiting_vacancy"],
        "post_scripts": (),
        "funcs": (member.std_mailing_func,),
        "test": (lambda record: True if member.is_waiting(record)
                                 else False),
        "e_and_or_p": "one_only",
        },
    request_inductee_payment={
        "subject": "Welcome to the Bolinas Rod & Boat Club",
        "from": authors["membership"],
        "body": letter_bodies["request_inductee_payment"],
        "post_scripts": (
            post_scripts["remittance"],
            ),
        "funcs": (member.inductee_payment_f,),
        "test": (lambda record: True if member.is_inductee(record)
                 else False),
        "e_and_or_p": "one_only",
        },
    request_delayed_inductee_payment={
        "subject": "Welcome to the Bolinas Rod & Boat Club",
        "from": authors["membership"],
        "body": letter_bodies["request_delayed_inductee_payment"],
        "post_scripts": (
            post_scripts["remittance"],
            ),
        "funcs": (member.inductee_payment_f,),
        "test": (lambda record: True if member.is_waiting(record)
                 else False),
        "e_and_or_p": "one_only",
        },
    second_request_inductee_payment={
        "subject": "Still awaiting Club dues",
        "from": authors["membership"],
        "body": letter_bodies["second_request_inductee_payment"],
        "post_scripts": (
            post_scripts["remittance"],
            ),
        "funcs": (member.inductee_payment_f,),
        "test": (lambda record: True if member.is_inductee(record)
                 else False),
        "e_and_or_p": "one_only",
        },
    welcome2full_membership={
        "subject": "You are a member!",
        "from": authors["membership"],
        "body": letter_bodies["welcome2full_membership"],
        "post_scripts": (post_scripts["ref1_email_or_PO"],
                         post_scripts["covid19"],
                         ),
        "funcs": (member.std_mailing_func,),
        "test": (lambda record: True if member.is_new_member(record)
                 else False),
        "e_and_or_p": "one_only",
        },

    expired_application={
        "subject": "Application Expired",
        "from": authors["membership"],
        "body": letter_bodies["expired_application"],
        "post_scripts": (),
        "funcs": (member.std_mailing_func,),
        "test": (lambda record: True),
        "e_and_or_p": "one_only",
        },

    retirement_from_club={
        "subject": "Sorry you're leaving us.",
        "from": authors["membership"],
        "body": letter_bodies["retirement_from_club"],
        "post_scripts": (),
        "funcs": (member.std_mailing_func,),
        "test": (lambda record: True),
        "e_and_or_p": "one_only",
        },

    membership_termination={
        "subject": "Sorry you're leaving us.",
        "from": authors["membership"],
        "body": letter_bodies["membership_termination"],
        "post_scripts": (),
        "funcs": (member.std_mailing_func,),
        "test": (lambda record: True if member.is_terminated(record)
                 else False),
        "e_and_or_p": "usps",
        },

    cover_letter={
        "subject": "Recent Minutes",
        "from": authors["secretary"],
        "body": letter_bodies["cover_letter"],
        "post_scripts": (),
        "funcs": (member.std_mailing_func,),
        "test": (lambda record: False if record['email'] else True),
        "e_and_or_p": "one_only",
        },

    personal={
        "subject": "Papers mistakenly included with application",
        "from": authors["ak"],
        "body": letter_bodies["personal"],
        "post_scripts": (),
        "funcs": (member.std_mailing_func,),
        "test": (lambda record: True if 'p' in record["status"]
                 else False),
        "e_and_or_p": "usps",
        },

    tpmg_social_security={
        "subject": "Medicare Reimbursement",
        "from": authors["ak"],
        "salutation": "Dear Sir or Madame,",
        "body": letter_bodies["tpmg_social_security"],
        "post_scripts": (),
        "funcs": (member.std_mailing_func,),
        "test": (lambda record: True if 'TPMG' in record["first"]
                 else False),
        "e_and_or_p": "usps",
        },
    randy={
        "subject": "Pluma Pescadores",
        "from": authors["randy"],
        #       "salutation": "Dear Sir or Madame,",
        "body": letter_bodies["fromRandy"],
        "post_scripts": (),
        "funcs": (member.std_mailing_func,),
        "test": (
            lambda record:
            True if (member.is_member_or_applicant(record)
                     and member.has_valid_email(record))
            else False),
        "e_and_or_p": "email",
        },
    payment={  # # If using this, must edit "test" ##
        "subject": "Payment of Amount Due",
        "from": authors["ak"],
        #       "salutation": "Dear Sir or Madame,",
        "body": letter_bodies["payment"],
        "post_scripts": (),
        "funcs": (member.std_mailing_func,),
        "test": custom_lambdas['MarinMechanical'],
        #       "test": custom_lambdas['QuattroSolar'],
        "e_and_or_p": "usps",
        },

    )
# ... end of content_types.

printers = dict(
    # tuples in the case of envelope windows.
    X6505_e1=dict(  # Smaller envelope.
        # e1: envelope with distances (in mm) from top to
        # top of top window       21
        # bottom of top window    43
        # top of lower window     59
        # bottom of lower window  84
        indent=7,
        top=4,  # blank lines at top  1 ..2
        frm=(4, 25),  # return window 3..6
        date=5,  # lines between windows 7..11
        to=(5, 30),  # recipient window 12..16
        re=2,  # lines below bottom window
        ),
    X6505_e2=dict(  # Larger envelope.
        indent=5,
        top=2,  # blank lines at top  1 ..2
        frm=(4, 25),  # return window 3..6
        date=5,  # lines between windows 7..11
        to=(5, 30),  # recipient window 12..16
        re=2,  # lines below bottom window
        ),
    HL2170=dict(
        indent=3,
        top=1,  # blank lines at top
        frm=(5, 25),  # return window
        date=4,  # between windows
        to=(7, 29),  # recipient window
        re=3,  # below windows => fold
        ),
    Janice=dict(
        indent=4,
        top=4,  # blank lines at top
        frm=(5, 25),  # return window
        date=4,  # between windows
        to=(7, 29),  # recipient window
        re=3,  # below windows => fold
        ),
    Michael=dict(
        indent=0,
        top=0,  # blank lines at top
        frm=(4, 30),  # return window
        date=3,  # between windows
        to=(6, 38),  # recipient window
        re=3,  # below windows => fold
        ),
    )
# ## ... end of printers (dict specifying printer being used.)


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


def prepare_letter_template(which_letter, lpr):
    """
    Prepares the template for a letter.
    <which_letter>: one of the <content_types> and
    <printer>: one of the keys to the <printers> dict
    specifying which printer is to be used (passed as the
    "--lpr" command line parameter.)
    Returns a 'letter' with formatting fields to be filled
    in by expanding <record>:
    typically {first}, {last}, {address}, {town}, {state},
    {postal_code}, {country}, and possibly (one or more)
    {extra}(s) &/or 'PS's.
    """
    #   print(printer)
    #   lpr = printers[printer]
    # top margin:
    #   print(lpr['top'])
    ret = [""] * lpr["top"]  # add blank lines at top
    # return address:
    ret_addr = address_format.format(**which_letter["from"])
    ret.append(helpers.expand(ret_addr, lpr['frm'][0]))
    # format string for date:
    ret.append(helpers.expand(
            (helpers.get_datestamp()), lpr['date']))
    # format string for recipient adress:
    ret.append(helpers.expand(address_format, lpr['to'][0]))
    # subject/Re: line
    ret.append(helpers.expand(
        "Re: {}".format(which_letter["subject"]), lpr['re']))
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


def prepare_email_template(which_letter):
    """
    Prepares the template for an email.
    Used by utils.prepare_mailing_cmd,
    Format fields are subsequently filled by **record.
    """
    ret = ["Dear {first} {last},"]
    ret.append(which_letter["body"])
    ret.append(which_letter["from"]["email_signature"])
    ret.extend(get_postscripts(which_letter))
    return '\n'.join(ret)


def contents():
    """
    Provides a way of getting a quick glimps
    of the various contents provided.
    Typical usage:
        print('\n'.join(contents()))
    """
    tuples = (('custom_lambdas', custom_lambdas),
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
        ret.extend(helpers.tabulate(r,
                                    alignment='<',
                                    max_width=140,
                                    separator=' | ')
                   )
    return ret


def main():
    print("content.py has no syntax errors")
    which = content_types["for_testing"]
    lpr = printers["X6505_e1"]
    letter = prepare_letter_template(which, lpr)
    email = prepare_email_template(which)
    rec = dict(
        first="Jane",
        last="Doe",
        address="nnn An Ave.",
        town="Any Town",
        postal_code="CODE",
        state="CA",
        country="USA",
        email="myemail@provider.com",
        extra="""A lot more junk:
Certainly nothing very serious!
Just a lot of junk.""",
        )
    print("Letter follows...")
    print(letter.format(**rec))
    with open("letter2print", 'w') as fout:
        fout.write(helpers.indent(letter.format(**rec),
                                  lpr['indent']))
    print("Email follows...")
    print(email.format(**rec))
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
    # main()
    print('\n'.join(contents()))
