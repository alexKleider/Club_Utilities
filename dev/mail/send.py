#!/usr/bin/env python3

# File: send.py

"""
Provides a python interface to the command line msmtp command.
By default uses my easydns.com account as mail transfer agent.
Assumes proper configuration of ~/.msmtprc
"""

import sys
import tempfile
import subprocess


def mutt_send(recipient, subject, body,
                attachments=None,
                mutt_config='~/.mutteasy'):
    """
    Does the mass e-mailings with attachment(s) which, if
    provided, must be in the form of a list of files.
    """
    cmd_args = ["mutt", "-F", mutt_config, ]
    cmd_args.extend(["-s", "{}".format(subject)])
    if attachments:
        list2attach = ['-a']
        for path2attach in attachments:
            list2attach.append(path2attach)
        cmd_args.extend(list2attach)
    cmd_args.extend(["--", recipient])
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE,
                       input=body, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))


def smtp_send(recipients, message, account='easy'):
    """
    Send email, as defined in <message>[1],
    to the <recipients> who will receive this email
    from person identified by the 'from' clause in ~/.msmtprc.
    <recipients> must be an iterable of one or more strings
    representing valid email addresses.
    [1] <message> must be in proper format with
    "From:", "To:" & "Subject:" lines (no leading spaces!)
    followed by a blank line and then the text of the email.
    """
    cmd_args = ["msmtp", "-a", account, ]
    for recipient in recipients:
        cmd_args.append(recipient)
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE,
                       input=message, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))


recipients = ("alex@kleider.ca",
              "alexkleider@gmail.com",
#             "alexkleider@protonmail.com",
              )
body="""Body of email sits here.
I hope formatting is preserved.
Sincerely,
Alex Kleider
"""

header = """From: alex@kleider.ca
To: alexkleider@gmail.com
Subject: this is a test

{}""".format(body)

attachments = (
"""# First attachment4testing

This is a test attachment.
""",
"""# Second attachment4testing

Another attachment for testing.
""",
)

test_files = []

def create_attachment_files(
        attachments=attachments,
        test_files=test_files):
    n = 0
    for attachment in attachments:
        temp_file = tempfile.NamedTemporaryFile(mode='w')
        temp_file.write(attachment)
        test_files.append(temp_file)

def delete_attachment_files(test_files=test_files):
    for test_file in test_files:
        test_file.close()

if __name__ == "__main__":
    response = input("Send a test email using m)utt or s)mtp? ")
    if response and response[0] in 'sS':
        print("Using smtp...")
        smtp_send(recipients, header + body)
    elif response and response[0] in 'mM':
        print("Using mutt...")
        create_attachment_files()
        mutt_send('alex@kleider.ca',
                  'this is a test',
                  body,
                  attachments=[attachment.name
                        for attachment in test_files ])
    else:
        print("Must specify M)utt or S)mtp.")


