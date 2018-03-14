#!/bin/sh
# param: index total times prex_len
index=$1
total=$2
file_name=$1.log
sed -i 's/$/<br \/>/g' $file_name
count=1
shuf $file_name | head -n $total > $index$count.task
count=2
shuf $file_name | head -n $total > $index$count.task
count=3
shuf $file_name | head -n $total > $index$count.task

item_count=`expr $total / $3`
month=4
len=$4
for task in `ls $index*.task`
do
	echo $task
	split -l $item_count $task -d -a$len $month-$index-  
	month=`expr $month + 1 `
done

