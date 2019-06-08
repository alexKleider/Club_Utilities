#!/bin/bash

# File: backup.sh

# ToDo: make this idempotent.

BACKUP="/media/alex/_EAGLE/Brbc"
STAMP=`date +%y-%m-%d`
DEST=${BACKUP}/$STAMP
LAST=`cat ${BACKUP}/last`
SRC="/home/alex/Club/Mshp/"

if [ -d ${DEST} ]; then
  echo Backup already done today. No backup until tomorrow.
  exit 1
else
  echo "All clear to go ahead. (Directory ${DEST} doesn't exist.)"
fi

mkdir $DEST
cp -al ${BACKUP}/${LAST}/. ${BACKUP}/$DEST
rsync -av --exclude='Utils' --delete $SRC $DEST

echo $STAMP > ${BACKUP}/last
