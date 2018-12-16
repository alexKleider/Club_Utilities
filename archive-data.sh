#!/bin/bash

# File: archive-data.sh

# Archive club data files that are in the Mshp/Py directory but
# excluded from the git repo.

STAMP=`date +%y-%m-%d`
DATA_ARCHIVES='../Archives/Data/'
TARFILE=${STAMP}.tar.gz
mkdir $STAMP
cp  applica*  ${STAMP}/
cp  extra_fees.txt  ${STAMP}/
cp  memlist.csv  ${STAMP}/
cp  receipts*  ${STAMP}/
cp  reimbursements*  ${STAMP}/
cp  report*  ${STAMP}/
cp  todo  ${STAMP}/
cp  mynotes  ${STAMP}/
cp  sensitive  ${STAMP}/
cp  loose-ends  ${STAMP}/
cp  attrition  ${STAMP}/

tar -czvf $TARFILE $STAMP
mv $TARFILE $DATA_ARCHIVES
rm -r $STAMP

# to extract:
# tar xvzf file.tar.gz
