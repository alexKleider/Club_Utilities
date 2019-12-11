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
cp -r Data/  ${STAMP}/
cp -r Exclude/  ${STAMP}/
cp -r Info/  ${STAMP}/
cp -r Mydata/  ${STAMP}/
cp -r Temp/  ${STAMP}/

tar -czvf $TARFILE $STAMP
mv $TARFILE $DATA_ARCHIVES
rm -r $STAMP


