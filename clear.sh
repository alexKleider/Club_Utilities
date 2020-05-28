#!/usr/bin/bash

# File: clear.sh

# Deletes Data/MailingDir and all it's contents.
# Working emails should be archived (./archive_mailings.sh)
# and doing so also deletes Data/MailingDir.
# This script is useful when testing and contents 
# of Data/MailingDir can be discarded.

if [ -f Data/emails.json ]
    then
        echo "Removing Data/emails.json"
        rm Data/emails.json
    else
        echo "emails.json not found."
fi

if [ -d Data/MailingDir ]
    then
        echo "Removing Data/MailDir"
        rm -rf Data/MailingDir
    else
        echo "Data/MailingDir not found."
fi


