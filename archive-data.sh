#!/bin/bash

# File: archive-data.sh

# Archive club data files that are in the Mshp/Py directory but
# excluded from the git repo.

STAMP=`date +%y-%m-%d`
DATA_ARCHIVES='../Archives/Data/'
TARFILE=${STAMP}.tar.gz
mkdir $STAMP
cp  applica*  ${STAMP}/
cp  attrition  ${STAMP}/
cp  extra_fees.txt  ${STAMP}/
cp  leadership  ${STAMP}/
cp  loose-ends  ${STAMP}/
cp  memlist.csv  ${STAMP}/
cp  mynotes  ${STAMP}/
cp  receipts*  ${STAMP}/
cp  reimbursements*  ${STAMP}/
cp  report*  ${STAMP}/
cp  sensitive  ${STAMP}/
cp  todo  ${STAMP}/

tar -czvf $TARFILE $STAMP
mv $TARFILE $DATA_ARCHIVES
rm -r $STAMP

# to extract:
# tar xvzf file.tar.gz
