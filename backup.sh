#!/bin/bash

# File: backup.sh

STAMP=`date +%y-%m-%d`
mkdir ../Backup/$STAMP
cp  memlist.csv  ../Backup/$STAMP/
cp  extra_fees.txt  ../Backup/$STAMP/
cp  checks_received.txt  ../Backup/$STAMP/
cp  ../Lists/newmembers  ../Backup/$STAMP/
