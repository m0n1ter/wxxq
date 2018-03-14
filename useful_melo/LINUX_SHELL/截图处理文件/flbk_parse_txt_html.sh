#!/bin/sh
IFS_old=$IFS
IFS=$'\n'
body='<html><head><meta charset="utf-8" /><style>.datalist {    clear: both;    width: 100%;    border-top: 2px solid #B5CFD9;    border-bottom: 2px solid #B5CFD9;}.datalist td {    padding: 5px 0;    border-bottom: 1px dashed #99BBE8;}.datalist th {    line-height: 250%;    text-align: left;    color: #9EBECB;    font-size: 12px;    font-weight: bold;}body, td, input, textarea, select, button {    color: #666;    font: 12px "Lucida Grande", Verdana, Lucida, Helvetica, Arial, sans-serif;    margin-right: 10px;}</style></head><body><table class="datalist"><tr><th style="width:170px;">手机号</th><th style="width:140px">指令</th><th>时间</th></tr>'
end='</table></body></html>'
for name in `ls 2017*.txt`
do
    echo $name
    item=`awk -F "," '{printf "<tr><td>%s</td><td>%s</td><td>%s</td></tr>",$1,$2,$3}' $name `
    content=$body$item$end
    i=`expr index $name '.txt'`
    echo $i
    file_name=`expr substr $name 1 $i`
    echo $file_name
    echo "$content" > "./html/"$file_name"html"
done
IFS=$IFS_old
