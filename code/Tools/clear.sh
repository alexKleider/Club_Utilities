#!/usr/bin/bash

# File: clear.sh

# Deletes Data/emails.json and Data/MailingDir.
# Working emails should be archived (./archive_mailings.sh)
# and doing so also deletes Data/MailingDir.
# This script is useful when testing and contents 
# of Data/MailingDir can be discarded.

if [ -f /home/alex/Git/Club/Data/emails.json ]
    then
        echo "Removing Data/emails.json"
        rm /home/alex/Git/Club/Data/emails.json
    else
        echo "emails.json not found."
fi

if [ -d /home/alex/Git/Club/Data/MailingDir ]
    then
        echo "Removing Data/MailDir"
        rm -rf /home/alex/Git/Club/Data/MailingDir
    else
        echo "/home/alex/Git/Club/Data/MailingDir not found."
fi


