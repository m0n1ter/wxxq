#!/bin/sh
# param: index total times prex_len
index=$1
#times=$2
log_line=$2
#total=`expr $times \* $log_line`
#echo $total
for((i=1;i<4;i++))
do
sed -i 's/$/<br \/>/g' $index$i.task
done

month=4
len=$3
for task in `ls $index*.task`
do
	echo $task
	split -l $log_line $task -d -a$len $month-$index-  
	month=`expr $month + 1 `
done

