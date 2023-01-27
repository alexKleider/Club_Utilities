#!/usr/bin/env python3

# File: letters.py

"""
A module to support main.py (prepare mailing utility.)
(A slimmed down version of content.py)

A number of 'dict's are being used:
    letter_bodies
    printers: X6505, HL2170, ...

Other items:
    func: prepare_letter_template(which_letter, printer):

re printers: Both printer model and windowed
envelope size must be taken into consideration.
"""

import csv
import helpfuncs


def add_full_name(record):
    parts = []
    keys = record.keys()
    for key in ('prefix', 'first', 'initial', 'last', 'suffix'):
        if key in keys and record[key]:
            parts.append(record[key])
    record['full_name'] = ' '.join(parts)


def add_name4presentation(record, formality=0):
    if formality == 0:
        record['name4presentation'] = f"{record['first']}"
    elif formality == 1:
        add_full_name(record)
        record['name4presentation'] = f"{full_name(record)}"
    else:
        record['name4presentation'] = ""


def full_address(record):
    add_full_name(record)
    return """{full_name},
{address}
{town}, {state} {postal_code}
{country}""".format(**record)


letter_bodies_docstring = """
Letter bodies are being picked up from the file system.
"""

### !!!!!!!!!!!!!!!!!!!! POSTSCRIPTS !!!!!!!!!!!!!!!!! ##
post_scripts = dict(

    )

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


def letter_text(letter_body, recipient, sender,
                            lpr=printers['X6505_e9'],
                            formality=0):
    """
    Prepares and returns the letter.
    """
    return_address = full_address(sender)
    destination_address = full_address(recipient)
    add_name4presentation(recipient, formality=formality)
    add_name4presentation(sender, formality=formality)
    ret = [""] * lpr["top"]  # add blank lines at top
    ret.append(helpfuncs.expand(return_address, lpr['frm'][0]))
    ret.append(helpfuncs.expand(
            (helpfuncs.get_datestamp()), lpr['date']))
    ret.append(helpfuncs.expand(destination_address,
                                            lpr['to'][0]))
    # subject/Re: line
    ret.append(helpfuncs.expand('', lpr['re']))
    # salutation:
    ret.append(f"Dear {recipient['name4presentation']},\n")
    # body of letter (with or without {extra}(s))
    ret.append(letter_body)
    # signarue:
    if not formality:
        ret.append('\t\t\t\tSincerely,')
    else:
        ret.append('\t\t\t\tYours truely,')
    ret.append(f"\t\t\t\t{sender['name4presentation']}")

    return '\n'.join(ret)


def main():
    pass


def test_full_name():
    with open('Data/new.csv', 'r', newline='') as instream:
        reader = csv.DictReader(instream)
        fieldnames = reader.fieldnames
        for row in reader:
            add_full_name(row)
            print(row['full_name'])


if __name__ == "__main__":
    test_full_name()
    # main()

