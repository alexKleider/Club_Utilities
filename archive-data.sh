#!/bin/bash

# File: archive-data.sh

# Archive club data files that are in the Mshp/Py directory but
# excluded from the git repo.
# A compressed tar file goes into '../Archives/Data'.
# To extract:
# $ tar xvzf file.tar.gz

STAMP=`date +%y-%m-%d`
LAST=`head Info/last`
echo "Last time data was archived was on $LAST"
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
echo "Copying TestData directory and contents into $STAMP"
cp -r TestData/  ${STAMP}/

# tar -czvf $TARFILE $STAMP
echo "Calling tar on $STAMP > $TARFILE"
tar -czf $TARFILE $STAMP
echo "Moving $TARFILE into $DATA_ARCHIVES"
mv $TARFILE $DATA_ARCHIVES
echo "Deleting $STAMP"
rm -r $STAMP
echo "Storing date of this data archiving into file 'Info/last'.
echo $STAMP > Info/last

### to 'untar':
###   $ tar xvzf file.tar.gz


