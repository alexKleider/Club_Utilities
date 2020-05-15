#!/usr/bin/env python

# File: send.py

"""
Used to send an email.

Usage:  (when used from the command line)
  ./send.py smtp_server [JSON_FILE_NAME]

Options:
  server  can be any of the keys defined in the
        Pymail.config.config dict.

Provides send.  (when imported as a module)

Have not yet implemented ability to use
a second command line argument to specify
a json file from which to load emails.
"""

import sys
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
# from email.mime.base import MIMEBase
# from email import encoders
import mimetypes
import hashlib
import json
import time
import random

try:
    import config
except ModuleNotFoundError:
    import Pymail.config as config

MIN_TIME_TO_SLEEP = 1   #} Seconds between
MAX_TIME_TO_SLEEP = 5   #} email postings.

def pause():
    """
    Provides a random interval between emails so that
    the MTA is less likely to think the process is automated.
    Only used in the case of gmail.
    """
    time.sleep(random.randint(MIN_TIME_TO_SLEEP,
                              MAX_TIME_TO_SLEEP))


rfc5322 = {    # Here for reference, not used by the code.
#  Originator Fields
   "from": "From: ", # mailbox-list CRLF
   "sender": "Sender: ", # mailbox CRLF
   "reply-to": "Reply-To: ", # address-list CRLF

#  Destination Address Fields
   "to": "To: ", # address-list CRLF
   "cc": "Cc: ", # address-list CRLF
   "bcc": "Bcc: ", # [address-list / CFWS] CRLF

#  Identification Fields
   "message-id": "Message-ID: ", # msg-id CRLF
#  "in-reply-to": "In-Reply-To: ", # 1*msg-id CRLF
#  "references": "References: ", # 1*msg-id CRLF
#  "msg-id": [CFWS] "<" id-left "@" id-right ">" [CFWS]
#  "id-left": dot-atom-text / obs-id-left
#  "id-right": dot-atom-text / no-fold-literal / obs-id-right
#  "no-fold-literal": "[" *dtext "]"

#  Informational Fields
   "subject": "Subject: ", # unstructured CRLF
   "comments": "Comments: ", # unstructured CRLF
   "keywords": "Keywords: ", # phrase *("," phrase) CRLF
    }


def get_py_header(header):
    """
    Not used.
    """
    return rfc5322[header.replace('-', '_')]


def get_mailings(json_file_name):
    """
    Reads 'jason_file_name' to...
    Return a dict suitable for use as the 'mailings' parameter
    of the send function (defined below.)
    The json file must be of a format described in the 
    'send' function's docstring.
    """
    with open (json_file_name, 'r') as f_obj:
        return json.load(f_obj)


def get_bytes(text):
    return hashlib.sha224(bytes(text, 'utf-8')).hexdigest()


def pseudo_recipient(plus_name, email):
    """
    Returns an email address that will go to the gmail
    account specified by gmail_address.
    This is only applicable to gmail accounts: emulation of
    multiple addresses all pointing to same inbox:
    my+person1@gmail.com, my+person2@gmail.com, ...
    all go to my@gmail.com
    """
    parts = email.split('@')
    return parts[0] + '+' + plus_name + '@' + parts[1]


def attach(attachment, msg):
    """
    <msg>: an instance of MIMEMultipart() to which to add
    the attachment.
    <attachment> is the name of a file to become an attachment.
    This code has been successfully tested to work for the
    following types of files: text, .docx, .pdf, ..
    so is expected to work for all files.
    """
    basename = os.path.basename(attachment)
    with open(attachment, "rb") as f_obj:
        part = MIMEApplication(
            f_obj.read(), basename)
    # After the file is closed
    part['Content-Disposition'] = (
        'attachment; filename="%s"' % basename)
    msg.attach(part)


def attach_many(attachments, msg):
    """
    This code was 'plagerized' from the web.
    It is a slightly modified version of an excerpt of
    code submitted by vijay.anand found here..
    https://stackoverflow.com/questions/52292971/sending-single-email-with-3-different-attachments-python-3
    """
    for attachment in attachments:
        content_type, encoding = mimetypes.guess_type(attachment)
        if content_type is None or encoding is not None:
            content_type = "application/octet-stream"
        maintype, subtype = content_type.split("/", 1)
        if maintype == "text":
            with open(attachment) as fp:
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
        elif maintype == "image":
            with open(attachment, "rb") as fp:
                attachment = MIMEImage(fp.read(), _subtype=subtype)
        elif maintype == "audio":
            with open(attachment, "rb")as fp:
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
        else:
            with open(attachment, "rb") as fp:
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment",
                            filename=os.path.basename(attachment))
        msg.attach(attachment)

def attach1(attachment, msg):
    # Open PDF file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically
        # as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )


def into_string(string_or_list):
    """
    Returns a string.
    If given a list it must be of strings and a comma/space
    separated concatination is returned.
    """
    if isinstance(string_or_list, str):
        return string_or_list
    elif isinstance(string_or_list, list):
        return ', '.join(string_or_list)
    else:
        assert(False)


def send(mailings, service='easy', report_progress=True,
                            include_wait=True):
    """
    Sends emails.
    <mailings> is a list of dicts each representing an email to
    be sent. Each dict can have the following keys, some optional:
    'body': a (possibly empty) string.
    'attachments': a list (possible empty) of file names.
    'From', 'Reply-To', 'To', 'Subject', ...
    ...and possibly other commonly used fields defined by rfc5322.
    ...Values are either strings or lists of strings;
    in the latter case the values are converted into a single
    comma separated string.
    """
    server = config.config[service]
    if report_progress:
        print("Initiating SMTP: {host} {port}".format(**server))
    s = smtplib.SMTP(host=server['host'], port=server['port'])
    s.starttls()
    s.ehlo
    s.login(server['user'], server['password'])
    if report_progress:
        print("Logged in as {user} with password REDACTED."
            .format(**server))

    try:
        for mailing in mailings:
            msg = MIMEMultipart()
            body = mailing['body']
            attachments = mailing['attachments']
            del mailing['body']
            del mailing['attachments']
            for key in mailing:
                msg[key] = into_string(mailing[key])
            msg.attach(MIMEText(body, 'plain'))
#           attach_many(attachments, msg)  ## Fails, 2b trouble sh.
            for attachment in attachments:
                attach(attachment, msg)

            if report_progress:
                for key in mailing:
                    print("{}=>{}".format(key, msg[key]))

            s.send_message(msg)
            del msg
            if include_wait:
                pause()
    except:
        s.quit()
        if report_progress:
            print("Pymail.send.send() failed sending to {}."
                .format(mailing['To']))
        raise
    s.quit()


def main(mailings):
    """
    email.mime.text.MIMEText
    email.mime.multipart.MIMEMultipart
    """

if __name__ == "__main__":
    test_body_1 = """
    This is a test using Reply-To: gmail.
    Here's hoping it goes well.
    Goog luck.
    """

    argv_length = len(sys.argv)

    if not argv_length > 1:
        print("SMTP server not specified.")
        sys.exit()
    arg1 = sys.argv[1]
    if not arg1 in config.config:
        print("SMTP server designation invalid.")
        sys.exit()
    server = config.config[arg1]

    if argv_length == 3:
        print("Second argument not yet implemented")
        sys.exit()
        test_mailings = get_mailings(sys.argv[2])
    else:
        test_mailings = [
            {
            'From': 'alex@kleider.ca',
            'Reply-To': 'alexkleider@gmail.com',
            'To': ['akleider@sonic.net',
                pseudo_recipient('ak', 'alexkleider@gmail.com'),
                ],
            'Subject': 'TEST Reply-To',
            'attachments': [
            '/home/alex/Downloads/book_club_2020-2021_listing.docx',],
            'body': test_body_1,
            },
        ]
    send(test_mailings, service=arg1, report_progress=True)

