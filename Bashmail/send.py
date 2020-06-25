#!/usr/bin/env python3

# File Bashmail/send.py

"""
Used to send an email from bash by calling the subprocess module
to call msmtp or mutt (depending if attachments need to be sent.)

Provides send() when imported as a module.
Provides same "send()" functionality as that found in Pymail.send
"""

import os
import time
import subprocess

# Note: the 'To' header is NOT included in the following:
header_keys = ("From", "Sender", "Reply-To",
                 "Cc", "Bcc", "Subject", )

def smtp_send(email, mta):
    """
    WARNING: Can not accommodate attachments!
    First parameter is a dict with keys and values
    specifying an email.  If there are attachments
    a warning is printed and they are NOT sent.
    <mta> specifies which Mail Transfer Agent to use.
    """
    cmd_args = ["msmtp", "-a", mta, "-t", "--"]
    message = []
    included_keys = email.keys()
    for key in header_keys:
        if key in included_keys:
            message.append("{}: {}".format(key, email[key]))
    if message:
        message.append('')
        message = '\n'.join(message)
        message = message + email['body']
    else:
        message = email['body']
    if "attachments" in email and email["attachments"]:
        print("Not configured to send attachments:")
        for attachment in attachments:
            print ("Attachment '{}' is NOT being included."
                .format(attachment))
    for recipient in email['To'].split(','):
        print("Appending recipient '{}'.".format(recipient))
        cmd_args.append(recipient)
    print(cmd_args)
    print(message)
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE, 
        input=message, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))


def mutt_send(email, mta):
    """
    Choose mutt to send email if there are attachments.
    """
    cmd_args = [ "mutt", "-F",
        os.path.expanduser("~/.mutt{}".format(mta)), ]
    cmd_args.extend(["-s", "{}".format(email["Subject"])])
    if email["attachments"]:
        list2attach = ['-a']
        for path2attach in email["attachments"]:
            list2attach.append(path2attach)
        cmd_args.extend(list2attach)
        cmd_args.appand("--")
    if type(email['To'])==str:
        cmd_args.append(email['To'])
    else:
        cmd_args.extend(email['To'])
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE, 
        input=email["body"], encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, email['To']))


def send_email_using_mutt(email, mta):
    mutt_send(email, mta)


def send_email(email, mta):
    if ('attachments' in email.keys()   # key is there ..
    and email['attachments']):          # and has a value.
        mutt_send(email, mta)
    else:                         # no attachment to include
        msmtp_send(email, mta)


def send(emails, mta, report_progress=True,
                            include_wait=True):
    """
    Sends emails using msmtp.
    <email> is a dict representing an email to be sent.
    Keys, some optional, can be as follows:
    'body': a (possibly empty) string. (optional)
    'attachments': a list (possible empty) of file names. (optional)
    'From', 'Reply-To', 'To', 'Subject', ...
    ...and possibly other commonly used fields defined by rfc5322.
    ...Values are either strings or lists of strings;
    in the latter case the values are converted into a single
    comma separated string.
    """
    counter = 0
    n_emails = len(emails)
    ret = []
    if mta != 'clubg':
        response = input(
            "Gmail addressees will get a warning! Continue? ")
        if response and response[0] in 'yY':
            pass
        else:
            sys.exit()
    for email in emails:
        counter += 1
        if report_progress:
            print("Sending email #{}/{} to {}..."
    #           .format(counter, n_emails, ", ".join(email['To'])))
                .format(counter, email['To']))
        mutt_send(email, mta)  #Using mutt; msmtp not working.
        if include_wait:
            time.sleep(random.randint(MIN_TIME_TO_SLEEP,
                                    MAX_TIME_TO_SLEEP))
#  Rest redacted because msmtp seems to not be working.        
#       if 'attachments' in emails:  # use mutt:
#           mutt_send(email, mta)
#       else:                        # use msmtp:
#           smtp_send(email, mta)

redacted_part_of_send = '''
        recipients = [
            recipient for recipient in email['To'].split(',')]
        keys = [key for key in email.keys()]
        for key in header_keys:
            if key in keys:
                ret.append("{}: {}".format(key, email[key]))
        ret.append('')
        ret.append(email['body'])
        if 'attachments' in keys:
            print( "Unable to send attachments by this mechanism.")
            for attachment in email['attachments']:
                print("Attachment '{}' has not been sent to {}."
                    .format(email.attachment, email['To']))
        counter += 1
        print("Sending email #{} to {}."
            .format(counter, ", ".join(email['To'])))
        smtp_send(recipients, '\n'.join(ret))
        if include_wait:
            time.sleep(random.randint(MIN_TIME_TO_SLEEP,
                                    MAX_TIME_TO_SLEEP))
'''

