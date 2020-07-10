#!/bin/bash

# File: archive-mailing.sh

# Archive after sending out a mailing.
# ... assuming defaults are used:

STAMP=`date +%y-%m-%d`
# STAMP='19-08-07'
MAILING_ARCHIVES='../Archives/Mailings'
TARFILE=${STAMP}.tar.gz
MAILING_DIR='Data/MailingDir'
EMAILS_JSON='Data/emails.json'
echo "Moving email json file into Mailing Directory..."
mv $EMAILS_JSON ${MAILING_DIR}/$EMAIL_JSON 
echo "Renaming Mailing Directory to date stamp..."
mv $MAILING_DIR $STAMP

echo "Create a tarball ..."
tar -czvf $TARFILE $STAMP
echo "Remove othe original ..."
rm -r $STAMP
echo "Move the tarball to the archives ..."
mv $TARFILE $MAILING_ARCHIVES
echo "... all done."


# to extract:
# tar xzvf file.tar.gz
