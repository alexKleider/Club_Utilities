#!/bin/bash

# File: archive-mailing.sh

# Archive after sending out a mailing.
# ... assuming defaults are used:

STAMP=`date +%y-%m-%d`
MAILING_ARCHIVES='../Achives/Mailings'
TARFILE=${STAMP}.tar.gz
MAILING_DIR='MailingDir'
EMAILS_JSON='emails.json'
mv $EMAILS_JSON ${MAILING_DIR}/$EMAIL_JSON 
mv $MAILING_DIR $STAMP

tar -czvf $TARFILE $STAMP
rm -r $STAMP
mv $TARFILE $MAILING_ARCHIVES


# to extract:
# tar xvzf file.tar.gz
