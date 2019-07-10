#!/usr/bin/env python3

# File: mutt_send.py

"""
Usage:
    ./mutt_send.py
    
The following are set within the script as global variables:
    recipient_csv_file,
    subject,
    body_text_file,
    attachment_file
"""

import sys
import csv
import time
import subprocess

for arg in sys.argv[1:]:
    print(arg)

muttrc = 'muttrc'
recipient_csv_file = "experimental.csv"
recipient_csv_file = '../Data/memlist.csv'
subject = "Minutes of recent BR&BC meeting"
body_text_file = "letter.txt"
attachment_file = "/home/alex/Club/Mshp/Minutes/Meeting/190605.pdf"


def mutt_send(recipient, subject, body, attachment=None):
    """
    Does the mass e-mailings with attachment
    if one is provided.
    """
    cmd_args = [ "mutt", "-F", muttrc, ]
    if attachment:
        cmd_args.extend([ "-a", attachment])
    cmd_args.extend([
        "-s", "{}".format(subject),
        "--", recipient
        ])
    p = subprocess.run(cmd_args, stdout=subprocess.PIPE, 
        input=body, encoding='utf-8')
    if p.returncode:
        print("Error: {} ({})".format(
            p.stdout, recipient))

def main():
    with open(body_text_file, 'r') as file_object:
        body = file_object.read()
    with open(recipient_csv_file, 'r') as file_object:
        dict_reader = csv.DictReader(file_object, restkey='status')
        for record in dict_reader:
            mutt_send(record["email"],
                    subject,
                    body,
                    attachment_file)
            print("Sent email /w attachment to {first} {last}."
                .format(**record))
            time.sleep(3)

# Delete following two lines for the real McCoy! #
def main():
    pass

print("Emails are about to be sent to all in the following file:")
print(recipient_csv_file)
with open(recipient_csv_file, 'r') as file_object:
    dict_reader = csv.DictReader(file_object, restkey='status')
print("The body of each email will be the content of the file:")
print(body_text_file)
print("The subject line will read: '{}'."
    .format(subject))
print("The following file will be an attachment:")
print(attachment_file)
response = input("OK to go ahead? (y/n): ")
if response and response[0] in "Yy":
    print("Moving forward...")
    main()
    print("...but not yeat!!")
else:
    print("Aborting.")
