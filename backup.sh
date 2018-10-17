#!/bin/bash

# File: backup.sh

STAMP=`date +%y-%m-%d`
mkdir ../Backup/$STAMP
cp  memlist.csv  ../Backup/$STAMP/
cp  extra_fees.txt  ../Backup/$STAMP/
cp  receipts*.txt  ../Backup/$STAMP/
cp  report*.txt  ../Backup/$STAMP/
cp  ../Lists/newmembers  ../Backup/$STAMP/
