#!/bin/bash

# File: jt.sh
# A script for Janice to simplify sending R&BC mailings.

# The following must be set each time before using the script:

DIR="19-05-29"

# Usage:
#  $ jt.sh 

tar -xzvf ${DIR}.tar.gz
cd $DIR
if [ -e emails.json ]; then
    rm emails.json
fi
lpr *
echo Your printer is hopefully now doing its thing and
echo we will now clean by deleting all the following
echo files EXCEPT your backup directory:
cd ..
ls 
rm -r ${DIR}* jt.sh
echo See, only your backup directory remains in your Desktop:
ls
cd ..
echo This should leave you in your home directory:
pwd

