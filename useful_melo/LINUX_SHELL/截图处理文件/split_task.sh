#!/bin/sh
index=$1
item_count=$2
month=4
len=$3
for task in `ls $index*.task`
do
	echo $task
	split -l $item_count $task -d -a$len $month-$index-  
	month=`expr $month + 1 `
done
