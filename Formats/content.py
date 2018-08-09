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


{date}



{first} {last}
{address}
{town}, {state} {postal_code}



Re: {subject}

Dear {first} {last},

""",

"body":"""
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
{}

Sincerely,
Alex Kleider (Membership)

[1] rodandboatclub@gmail.com or a letter to the PO Box

[2] If the club has an email address on file for you, you'll be
receiving this by email as well as 'snail mail.'
"""

}

content = content_aug2018


def custom_aug2018(record, log = None):
    """
    Returns a (possibly empty) list of strings.
    Determines what to place in the customizable spot of a letter.
    A specialized version of this function will have to be written
    for each letter and passed to the <billing> method.
    <record> should be a dict created by the <make_dict> method of
    the <Membership> class.
    <log>, if provided, is assumed to be a mutable iterable.
    """
    ret = []

    fees = {}
    fees["Club dues"] = record["dues"]
    fees["Mooring"] = record["mooring"]
    fees["Dock usage"] = record["dock"]
    fees["Kayak storage"] = record["kayak"]
    total_due = 0
    for item in ["Club dues", "Mooring",
                    "Dock usage", "Kayak storage"]:
        if fees[item]:
            fee = int(fees[item])
        else:
            fee = 0
        if fee:
            total_due += fee
            ret.append(
                "{:<13}: ${}".format(item, fee))
    if ret:
        if log:
            log.append("{:<25} {}".format(
                record["first"] + ' ' + record["last"],
                ", ".join(ret)))
        ret.append("Total:           ${}".format(total_due))
        pass

    else:
#       ret = ["\nYou're all paid up!"]
        pass
    return ret

custom_func = custom_aug2018

if __name__ == "__main__":
    if len(sys.argv) > 1:
        jsonfile = sys.argv[1]
    else:
        jsonfile = "Formats/content.json"
    with open(jsonfile, "w") as file_object:
        json.dump(content, file_object)

