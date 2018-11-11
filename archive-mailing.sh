#!/bin/bash

# File: archive-mailing.sh

# Archive after sending out a mailing.
# ... assuming defaults are used:

STAMP=`date +%y-%m-%d`
MAILING_ARCHIVES='../Achives/Mailings/'
TARFILE=${STAMP}.tar.gz

MAILING_DIR='MailingDir'
EMAILS_JSON='emails.json'

mv $EMAIL_JSON ${MAILING_DIR}/
mv $MAILING_DIR $STAMP

tar -czvf $TARFILE $STAMP
mv $TARFILE $MAILING_ARCHIVES
rm -r $STAMP

