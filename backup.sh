#!/bin/bash

# File: backup.sh
# Versions of this script exist in the following directories:
#    /home/alex/Club/Mshp/Utils
#    /home/alex/Encrypted

# Idempotent to the extent that it will not
# do a back up more than once each day.

# Case specific parts (clearly indicated by "#***")
# are the destination device/directory assigned in the
# next line and the rsync command at the end of the script.

BACKUP="/media/alex/_EAGLE/Brbc"  #***

STAMP=`date +%y-%m-%d`
DEST=${BACKUP}/$STAMP
LAST=`cat ${BACKUP}/last`
SRC="/home/alex/Club/Mshp/"

if [ -d ${DEST} ]; then  # This segment provides idempotency.
  echo Backup already done today. No backup until tomorrow.
  exit 1
else
  echo "All clear to go ahead since the following directory..."
  echo "    ${DEST}"
  echo "doesn't already exist."
fi

mkdir $DEST

# Copy what was previously backed up using hard links...
cp -al ${BACKUP}/${LAST}/. $DEST

# ... then rsync to update that copy with current versions:
#rsync -a --exclude='Utils' --delete $SRC $DEST   #***
rsync -av --exclude='Utils' --delete $SRC $DEST  #***
# The excluded 'Utils' directory is backed up by git.
# Within 'Utils' there are files/directories excluded from git:
# These are archived by the archive_data.sh script which should
# be run before this script.

echo $STAMP > ${BACKUP}/last
echo "All done."

