#!/bin/bash

# File: backup.sh

# ToDo: make this idempotent.

BACKUP="/media/alex/_EAGLE/Brbc"
STAMP=`date +%y-%m-%d`
DEST=${BACKUP}/$STAMP
LAST=`cat ${BACKUP}/last`
echo $STAMP > ${BACKUP}/last

if [-d ${DEST}]; then
  echo Backup already done today. No backup until tomorrow.
  exit 1
fi

mkdir $DEST
cp -al ${BACKUP}/${LAST}/. ${BACKUP}/$DEST
rsync -av --exclude='Py' --delete ../../Mshp/  $DEST

