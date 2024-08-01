#!/bin/bash

# first input:  label sent breqfast request
# second input:  'IRIS' or 'NCEDC'

echo 'Retrieving data'

id=$1
echo $id

datac=$2
echo $datac

if [ "$datac" = "IRIS" ] 
then 
echo "Getting data via IRIS"
HOST='ftp.iris.washington.edu'
USER='ftp'
PASSWD='rebecca.colquhoun@univ.ox.ac.uk'
echo $HOST $USER $PASSWD $FILE
ftp -n $HOST << EOF 
quote USER $USER 
quote PASS $PASSWD
prompt off
cd pub/userdata/Rebecca_Colquhoun/
binary
mget *$id*
quit
EOF

find $id*seed -print0 | xargs -0 -I file tar -xvf file

find $id/*.mseed -print0 | xargs -0 -I file rdseed -f file -d -z 3 -E -g $id/$id.dataless
    
elif [ "$datac" = "NCEDC" ] 
then
    echo "Getting data via NCEDC"
HOST='ncedc.org'
USER='anonymous'
PASSWD=''
echo $HOST $USER $PASSWD $FILE
ftp -n $HOST << EOF 
quote USER $USER 
quote PASS $PASSWD
cd /outgoing/userdata/breq_fast/Jessica.Hawthorne
prompt off
binary
mget *$id*
mdelete *$id*
quit
EOF

find *$id* -print0 | xargs -0 -I file rdseed -f file -d -E -z 3
#rdseed -f nc.$id -d -z 3
fi





