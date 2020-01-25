#!/bin/sh
echo "Type the future date in ISO 8601 (YYYY-MM-DD) format."
read futuredate
echo $futuredate | tr -s '-' ' ' | awk '{dt=mktime($0 " 00-00-00")-systime(); print int(dt/86400+1) " days";}' 
