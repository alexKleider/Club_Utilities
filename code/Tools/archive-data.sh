#!/bin/bash

# File: archive-data.sh

### REDACTED ###  (in favour of archive_data.py)

# Archive the directories which are in the repo directory but not
# part of it because they containing club data files.
# The result is a compressed tar file which is added to the already
# existing ones filed in '../Archives/Data'.
# To extract:
# $ tar xvzf file.tar.gz
# To restore data, use restore.py giving it as a parameter the
# tar.gz file of your choice.
# Would like to rewrite this using Python so as to have the nonrepo
# directories specified by rbc.Club.NONREPO_DIRS rather than being
# hard coded.

STAMP=`date +%y-%m-%d`
LAST=`head Info/last`
echo "Last time data was archived was on $LAST"
DATA_ARCHIVES='${CLUB}/Archives/Data/'
TARFILE=${STAMP}.tar.gz
mkdir $STAMP
echo "Copying Data directory and contents into $STAMP"
cp -r Data/  ${STAMP}/
echo "Copying Exclude directory and contents into $STAMP"
cp -r Exclude/  ${STAMP}/
echo "Copying Info directory and contents into $STAMP"
cp -r Info/  ${STAMP}/
echo "Copying Mydata directory and contents into $STAMP"
cp -r Mydata/  ${STAMP}/
echo "Copying NonRepo directory and contents into $STAMP"
cp -r NonRepo/  ${STAMP}/
echo "Copying Temp directory and contents into $STAMP"
cp -r Temp/  ${STAMP}/
echo "Copying TestData directory and contents into $STAMP"
cp -r TestData/  ${STAMP}/

# tar -czvf $TARFILE $STAMP
echo "Calling tar on $STAMP > $TARFILE"
tar -czf $TARFILE $STAMP
echo "Moving $TARFILE into $DATA_ARCHIVES"
mv $TARFILE $DATA_ARCHIVES
echo "Deleting $STAMP"
rm -r $STAMP
echo "Storing date of this data archiving into file 'Info/last'."
echo $STAMP >> ${CLUBU}/Info/last

### to 'untar':
###   $ tar xvzf file.tar.gz


