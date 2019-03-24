#!/bin/bash

# File: archive-data.sh

# Archive club data files that are in the Mshp/Py directory but
# excluded from the git repo.
# A compressed tar file goes into '../Archives/Data'.
# To extract:
# $ tar xvzf file.tar.gz

STAMP=`date +%y-%m-%d`
DATA_ARCHIVES='../Archives/Data/'
TARFILE=${STAMP}.tar.gz
mkdir $STAMP
cp  Info/applica*  ${STAMP}/
cp  Info/attrition  ${STAMP}/
cp  Info/extra_fees.txt  ${STAMP}/
cp  Info/leadership.txt  ${STAMP}/
cp  Info/loose-ends  ${STAMP}/
cp  memlist.csv  ${STAMP}/
cp  mynotes  ${STAMP}/
cp  mynotes  ${STAMP}/
cp  receipts*  ${STAMP}/
cp  reimbursements*  ${STAMP}/
cp  report*  ${STAMP}/
cp  sensitive  ${STAMP}/
cp  todo  ${STAMP}/

tar -czvf $TARFILE $STAMP
mv $TARFILE $DATA_ARCHIVES
rm -r $STAMP

-rw-r--r-- 1 alex alex   896 Mar 17 18:18 applicants.rpt
-rw-r--r-- 1 alex alex  1993 Dec  6 13:52 application_rules.txt
-rw-r--r-- 1 alex alex   643 Feb 12 18:14 attrition
-rw-r--r-- 1 alex alex   773 Feb 28 09:30 leadership.txt
-rw-rw-r-- 1 alex alex   686 Dec 10 09:50 loose-ends
-rw-r--r-- 1 alex alex 38258 Jan  4 13:24 man_msmtp.txt
-rw-r--r-- 1 alex alex   452 Jan  5 19:03 msmtprc
-rw-r--r-- 1 alex alex    81 Mar 17 18:04 next_commit
-rw-rw-r-- 1 alex alex   739 Mar  1 17:22 proposal.txt
-rw-rw-r-- 1 alex alex  2287 Mar 17 17:30 receipts18-19.txt
-rw-r--r-- 1 alex alex   257 Jan  3 18:30 reimbursements.txt
-rw-r--r-- 1 alex alex  1547 Mar 17 18:46 report
-rw-r--r-- 1 alex alex   573 Mar 17 18:24 report2members.txt
-rw-r--r-- 1 alex alex   698 Mar 18 12:52 rules.txt
-rw-r--r-- 1 alex alex   237 Feb 10 15:52 sensitive
-rw-r--r-- 1 alex alex   147 Dec  8 18:56 todo

