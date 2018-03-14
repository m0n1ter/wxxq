#!/bin/sh
index=$1
total=$2
file_name=$1.log
count=1
shuf $file_name | head -n $total > $index$count.task
count=2
shuf $file_name | head -n $total > $index$count.task
count=3
shuf $file_name | head -n $total > $index$count.task
