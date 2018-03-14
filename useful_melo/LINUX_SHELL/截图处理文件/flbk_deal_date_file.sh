#!/bin/sh
IFS_old=$IFS
IFS=$'\n'
src_name=$1
date=''
cmp_date=''
content=''
for line in `cat $src_name` 
do
    echo $line
    cmp_date=`echo "$line"|awk -F "," '{print $3}'` 
    cmp_date=`echo ${cmp_date:0:10}`
    item=`echo "$line"|awk -F "," '{print $0}'` 
    if [ -z $date ]; then
       date=$cmp_date
    fi
    if [ $date = $cmp_date ]; then
       content=$content$item"\n" 
    else
       echo -e $content > $date.txt
       echo "----------------"
       content=$item"\n"
       date=$cmp_date
    fi
done
echo -e $content > $cmp_date.txt
echo "------end----------"
IFS=$IFS_old