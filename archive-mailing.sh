#!/bin/bash

# File: archive-mailing.sh

# Archive after sending out a mailing.
# ... assuming defaults are used:

STAMP=`date +%y-%m-%d`
echo STAMP set to $STAMP

MAILING_ARCHIVES='../Achives/Mailings'
echo MAILING_ARCHIVES set to $MAILING_ARCHIVES 

TARFILE=${STAMP}.tar.gz
echo TARFILE set to $TARFILE

MAILING_DIR='MailingDir'
echo MAILING_DIR set to $MAILING_DIR  

EMAILS_JSON='emails.json'
echo EMAILS_JSON set to $EMAILS_JSON

echo Moving $EMAILS_JSON to ${MAILING_DIR}/$EMAIL_JSON 
echo and $MAILING_DIR to $STAMP

mv $EMAILS_JSON ${MAILING_DIR}/$EMAIL_JSON 
mv $MAILING_DIR $STAMP

tar -czvf $TARFILE $STAMP

echo Moving $TARFILE to $MAILING_ARCHIVES
mv $TARFILE $MAILING_ARCHIVES

echo Recursively removing $STAMP
rm -r $STAMP

