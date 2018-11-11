#!/bin/bash

# File: backup.sh

# ToDo: make this idempotent.

BACKUP="/media/alex/_EAGLE/Brbc"
STAMP=`date +%y-%m-%d`
DEST=${BACKUP}/$STAMP
mkdir $DEST


rsync -av --exclude='Py' ../../Mshp/  $DEST

