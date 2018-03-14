#!/bin/sh
IFS_old=$IFS
IFS=$'\n'
src_name=$1
i=`expr index $src_name '.'`
i=`expr $i - 1`
folder=${src_name:0:$i}
if [ ! -d "$folder" ];then
   mkdir $folder
fi
cmp_date=''
date=''
content=''
for line in `cat $src_name`
do
   echo "+++++++++"$line
   cmp_date=`echo ${line:0:8}`
   item=`echo $line|awk -F ",;" '{print $0}'`
   item=$item"\n"
   echo $cmp_date
   if [ -z $date ];then
       date=$cmp_date
   fi
   if [ $date = $cmp_date ];then
       content=$content$item
   else
      echo -e $content > $folder/$date.txt
      echo "-----------"
      content=$item
      date=$cmp_date
   fi
done
echo -e $content > $folder/$cmp_date.txt
echo "-----end-------"
IFS=$IFS_old
