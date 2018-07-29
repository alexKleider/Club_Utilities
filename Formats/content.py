#!/usr/bin/env python

# File: content.py

"""
A supporting utility.
Povides, in the form of a dict, the formating strings required by the
'billing' command of the Bolinas Rod & Boat Club utility 'util.py'.

This dict can be imported from this module:
    from Formats.content import content
or ...
the dict can be loaded from a json file created by this module.

If run as 'main' it accepts an optional command line argument
which if not provided defaults to "Formats/content.json".

Don't forget to edit to suit- especially don't forget to modify
the date in "postal_header".
"""

import sys
import json

content_july2018 = {
"subject":"July mailing",

"email_header":"""From: rodandboatclub@gmail.com
To: {email}
Subject: {subject}

Dear {first} {last},

""",

"postal_header":"""




Bolinas Rod and Boat Club
PO Box 248
Bolinas, CA 94924


July 23, 2018



{first} {last}
{address}
{town}, {state} {postal_code}



Re: {subject}

Dear {first} {last},

""",

"body":"""

With July comes the beginning of the new membership year
and ideally we'd like to have all dues and fees in by now.
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
{}

Sincerely,
Alex Kleider (Membership)"""

}

content_aug2018 = {
"subject":"August mailing",

"email_header":"""From: rodandboatclub@gmail.com
To: {email}
Subject: {subject}

Dear {first} {last},

""",

"postal_header":"""




Bolinas Rod and Boat Club
PO Box 248
Bolinas, CA 94924


Aug 23, 2018



{first} {last}
{address}
{town}, {state} {postal_code}



Re: {subject}

Dear {first} {last},

""",

"body":"""

.......

A statement of your current standing will appear bellow;
If there are any dues or fees outstanding, please pop your
check into an envelope asap payable and send to the...
        Bolinas Rod and Boat Club
        PO Box 0248
        Bolinas, CA 94924
{}

Sincerely,
Alex Kleider (Membership)"""

}

content = content_aug2018

if __name__ == "__main__":
    if len(sys.argv) > 1:
        jsonfile = sys.argv[1]
    else:
        jsonfile = "Formats/content.json"
    with open(jsonfile, "w") as file_object:
        json.dump(content, file_object)

