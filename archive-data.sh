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

# tar -czvf $TARFILE $STAMP
tar -czf $TARFILE $STAMP
mv $TARFILE $DATA_ARCHIVES
rm -r $STAMP

### to 'untar':
###   $ tar xvzf file.tar.gz


