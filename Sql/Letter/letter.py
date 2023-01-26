#!/usr/bin/env python3

# File: letter.py

"""
A module to support main.py (prepare mailing utility.)
(A slimmed down version of content.py)

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
    func: prepare_letter_template(which_letter, printer):

re printers: Both printer model and windowed
envelope size must be taken into consideration.
"""

import csv
import helpfuncs


def full_name(record):
    parts = []
    keys = record.keys()
    for key in ('prefix', 'first', 'initial', 'last', 'suffix'):
        if key in keys and record[key]:
            parts.append(record[key])
    return ' '.join(parts)


def std_mailing_func(record, club):
    """
    Assumes any prerequisite processing has been done and
    requisite values added to record.
    Mailing is sent if the "test" lambda => True.
    Otherwise the record is ignored.
    """
    if club.which["test"](record):
        record["subject"] = club.which["subject"]
        if club.owing_only:
            if record['owing']:
                q_mailing(record, club)
        else:
            q_mailing(record, club)

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

# # single braces: fields populated by the content_type data.
# # double braces: fields populated by the record data.
letter_bodies = dict(

    angie_print="""
The Bolinas Rod & Boat Club is facing a crisis!

Leadership positions are being vacated and need to be filled.

Our Secretary is retiring; we need at least a Vice President
and may need a President as well; Four of our directors are
ending their terms in February and it's unclear how many will
be willing to stay on for another two year term.

This letter is an urgent appeal for volunteers who might be
willing to stand for election to these important positions.
Important because the Club is facing challenges that it can
only meet if there is a complete and dedicated leadership.

If the Club falters and goes in a direction of which you don't
approve, members will have only themselves to blame for not
stepping up to provide guidance.

If willing to serve please nominate yourself. You can do so
by email (rodandboatclub@gmail.com) or post (94924-0148.)
The annual general meeting is coming up the first Friday of
February so time is running out.
""",

    find_enclosed="""
Please find enclosed.
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

    gmail_warning="""
Google has changed posicy regarding use of gmail as a mail transfer
agent (MTA.)  The reason this is relevant to you as a member of the
Bolinas Rod & Boat Club _and_ a user of gmail is that as of the end of
May, 2022, emails you receive from BR&BC Membership will most likely
come with a warning regarding its authenticity.  The warning is mainly
against opening any accompanying attachments which Membership rarely
if ever sends so hopefully this won't create any hardship for anyone.

Please be assured that there's no malfeasance!
""",

    bad_address="""
Mail sent to you has been returned.

We have your mailing address as :

{extra}

Please let us know if this should be corrected and, if so, to what.
""",

    tpmg_social_security="""
Please find enclosed the documentation I believe you require from the
Social Security Administration concerning Medicare deductions for both
my wife and for me.
""",

    randy="""
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

    bill_paying="""
Thank you for your services.
"""
    )
# ... end of letter_bodies.


### !!!!!!!!!!!!!!!!!!!! POSTSCRIPTS !!!!!!!!!!!!!!!!! ##
post_scripts = dict(

    angie_print="""
Please respond by either replying to this email or by post:
    The Bolinas Rod & Boat Club
    PO Box 248
    Bolinas, CA 94924
""",

    remittance=""" Please send remittances to:
    The Bolinas Rod & Boat Club
    PO Box 248
    Bolinas, CA 94924
It's always a good idea to jot down on the check exactly for
what you are paying in order to prevent any confusion.""",

    ref1_email_or_PO="""[1] rodandboatclub@gmail.com or PO Box 248, 94924""",

    ref1_reservations="""[1] Reservations can be made through Anna Gade
    (uc_anna@sbcglobal.net.)""",

    covid19="""Because of the current pandemic, the Club is currently
    holding hybrid meetings, by zoom or in person. To attend in person
    you must have submitted proof of vaccination to the Club's email
    address.
    Let's hope for an early return to 'business as usual.'
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

content_type_docstring = """
One of the following content_types is assigned to the 'which'
attribute of an instance of utils.Club for mailing purposes.

  Each item in the following dict specifies:
      subject: re line in letter_bodies, subject line in emails
      from: expect a value from the 'authors' dict
          each value is itself a dict specifying more info...
          names, address, signatures, reply to, ..
      body: text of the letter which may or may not have
          one or more 'extra' sections.
      post_scripts:  a list of optional postscripts
      funcs: a list of functions used on each record during
          the data gathering traversal of the membership csv.
      test: a (usually 'lambda') function that determines
          if the record is to be considered at all.
      e_and_or_p: possibilities are:
          'both' email and usps,
          'email' email only,
          'usps' mail only,
       or 'one_only' email if available, otherwise usps.
  One of the following becomes the 'which' attribute
  of a Membership instance.
"""

content_types = dict(  # which_letter
    # ## If a 'salutation' key/value is provided for any of the
    # ## following, the value will be used as the salutation
    # ## instead of a 'Dear {first} {last},' line.
    # ## The first 4 listed values for each are used for first
    # ## stage formatting.
    angie_print={
        "subject": "Executive Commitee Members Needed",
        "from": authors["membership"],
        "body": letter_bodies["angie_print"],
        "post_scripts": (
#           post_scripts['angie_print'],
            ),
        "funcs": [std_mailing_func, ],
        "test": True,
        "e_and_or_p": "usps",
        },
    for_testing={
        "subject": "This is a test.",
        "from": authors["ak"],
        "body": letter_bodies["for_testing"],
        "post_scripts": (
            post_scripts['forgive_duplicate'],
            ),
#       "funcs": [testing_func, ],
        "test": True,
        "e_and_or_p": "one_only",
        },
    gmail_warning={
        "subject": "Gmail warning",
        "from": authors["membership"],
        "body": letter_bodies["gmail_warning"],
        "post_scripts": (),
#       "funcs": [std_mailing_func, ],
        "test": True,
        "e_and_or_p": "email",
        },
    bad_address={
        "subject": "Address correction requested.",
        "from": authors["membership"],
        "body": letter_bodies["bad_address"],
        "post_scripts": (post_scripts["ref1_email_or_PO"],),
#       "funcs": [bad_address_mailing_func, ],
        "test": True,
        "e_and_or_p": "email",
        },

    find_enclosed={  # test will always return False!?!
        "subject": "1040-es",
        "from": authors["ak"],
        "body": letter_bodies["find_enclosed"],
        "post_scripts": (),
#       "funcs": [std_mailing_func,],
        "test": True,
        "e_and_or_p": "usps",
        },

    tpmg_social_security={
        "subject": "Medicare Reimbursement",
        "from": authors["ak"],
        "salutation": "Dear Sir or Madame,",
        "body": letter_bodies["tpmg_social_security"],
        "post_scripts": (),
#       "funcs": (std_mailing_func,),
        "test": True,
        "e_and_or_p": "usps",
        },
    randy={
        "subject": "Pluma Pescadores",
        "from": authors["randy"],
        #       "salutation": "Dear Sir or Madame,",
        "body": letter_bodies["randy"],
        "post_scripts": (),
#       "funcs": (std_mailing_func,),
        "test": True,
        "e_and_or_p": "email",
        },
    bill_paying={  # # If using this, must edit "test" ##
        "subject": "Payment of Amount Due",
        "from": authors["ak"],
        #       "salutation": "Dear Sir or Madame,",
        "body": letter_bodies["bill_paying"],
        "post_scripts": (),
#       "funcs": (std_mailing_func,),
        "test": custom_lambdas['MarinMechanical'],
        #       "test": custom_lambdas['QuattroSolar'],
        "e_and_or_p": "usps",
        },

    )
# ... end of content_types.

printers = dict(
    # tuples in the case of envelope windows.
    X6505_e9=dict(  # Smaller envelope.  #9: 3-7/8 x 8-7/8"
        # e1: envelope with distances (in mm) from top to
        # top of top window       21
        # bottom of top window    43
        # top of lower window     59
        # bottom of lower window  84
        indent=5,
        top=4,  # blank lines at top  1 ..2
        frm=(4, 25),  # return window 3..6
        date=5,  # lines between windows 7..11
        to=(5, 30),  # recipient window 12..16
        re=3,  # lines below bottom window
        ),
    X6505_e10=dict(  # Larger envelope. #10: 4-1/8 x 9-1/2"
        indent=4,
        top=3,  # blank lines at top  1 ..2
        frm=(5, 25),  # return window 3..6
        date=5,  # lines between windows 7..11
        to=(6, 30),  # recipient window 12..16
        re=4,  # lines below bottom window
        ),
    HL2170_e10=dict(  # large envelopes, Cavin Rd usb printer
        indent=3,
        top=1,  # blank lines at top
        frm=(5, 25),  # return window
        date=4,  # between windows
        to=(7, 29),  # recipient window
        re=3,  # below windows => fold
        ),
    peter_e10=dict(  # Larger envelope. #10: 4-1/8 x 9-1/2"
        indent=5,
        top=4,  # blank lines at top
        frm=(4, 25),  # return window
        date=5,  # between windows
        to=(6, 29),  # recipient window
        re=3,  # below windows => fold
        ),
    angie_e9=dict(    # Smaller envelope.  #9: 3-7/8 x 8-7/8"
        indent=0,
        top=0,  # blank lines at top
        frm=(4, 40),  # return window
        date=7,  # between windows
        to=(7, 40),  # recipient window
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
    Returns a 'letter' /w formatting fields.
    """
    ret = [""] * lpr["top"]  # add blank lines at top
    # return address:
    ret_addr = address_format.format(**which_letter["from"])
    ret.append(helpfuncs.expand(ret_addr, lpr['frm'][0]))
    # format string for date:
    ret.append(helpfuncs.expand(
            (helpfuncs.get_datestamp()), lpr['date']))
    # format string for recipient adress:
    ret.append(helpfuncs.expand(address_format, lpr['to'][0]))
    # subject/Re: line
    ret.append(helpfuncs.expand(
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
    Provides a way of getting a quick glimpse
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
        ret.extend(helpfuncs.tabulate(r,
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
        fout.write(helpfuncs.indent(letter.format(**rec),
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

def test_full_name():
    with open('Data/new.csv', 'r', newline='') as instream:
        reader = csv.DictReader(instream)
        fieldnames = reader.fieldnames
        for row in reader:
            print(full_name(row))



if __name__ == "__main__":
    test_full_name()
    # main()
#   print('\n'.join(contents()))
#   print("content.py compiles OK")
else:
    def print(*args, **kwargs):
        pass



