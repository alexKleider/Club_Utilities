#!/bin/bash

# File: backup.sh

#### !!! this precedes when I moved Data from beneath Utils
#### !!! to beside it.  Needs a rewrite before being useful.

# will not do a back up more than once each day.

# Case specific parts (clearly indicated by "#***")
# are the destination device/directory assigned in the
# next line and the rsync command at the end of the script.

# This utility backs up everything except what's in the git repo.
# Keep in mind though that current data must first be archived
# (use archive_data.py) and when setting up a new system that data
# must be restored (using restore.py.)

BACKUP="/home/alex/Mnt/Club"  #***  The ScanDisc thumb drive.
# BACKUP="/media/alex/_EAGLE/Brbc"  #*** The Eagle HardDrive

STAMP=`date +%y-%m-%d`
DEST=${BACKUP}/$STAMP
LAST=`cat ${BACKUP}/last`
#SRC="/home/alex/Club/Mshp/"  #***
SRC="/home/alex/Git/Club/"  #***
SRC=${CLUB}  #***

if [ -d ${DEST} ]; then  # This segment provides idempotence.
  echo "Backup already done today. No backup until tomorrow."
  exit 1
else
  echo "All clear to go ahead since the following directory..."
  echo "    ${DEST}"
  echo "doesn't already exist."
fi

echo "Creating $DEST directory.."
mkdir $DEST

# Make sure we save a copy of .git/info/exclude
echo "..save a copy of .git/info/exclude"
cp .git/info/exclude ${CLUB}  #***

# Copy what was previously backed up using hard links...
echo "..creating (using hard links) a copy of previous backup"
cp -al ${BACKUP}/${LAST}/. $DEST

# ... then rsync to update that copy with current versions:
echo "Running rsync to update the copy..."
# Using verbose mode helps pick up errors...
rsync -av --exclude='Utils' --delete $SRC $DEST  #***
# The excluded 'Utils' directory is backed up by git.
# Within 'Utils' there are files/directories excluded from git:
# These are archived by archive-data.py script which should
# be run before doing the backup.

echo "Updating the time stamp."
echo $STAMP > ${BACKUP}/last
echo "All done."

