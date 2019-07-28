#!/bin/bash

# File: archive-mailing.sh

# Archive after sending out a mailing.
# ... assuming defaults are used:

STAMP=`date +%y-%m-%d`
# STAMP='19-07-24'
MAILING_ARCHIVES='../Archives/Mailings'
TARFILE=${STAMP}.tar.gz
MAILING_DIR='Data/MailingDir'
EMAILS_JSON='Data/emails.json'
mv $EMAILS_JSON ${MAILING_DIR}/$EMAIL_JSON 
mv $MAILING_DIR $STAMP

tar -czvf $TARFILE $STAMP
rm -r $STAMP
mv $TARFILE $MAILING_ARCHIVES


# to extract:
# tar xzvf file.tar.gz
