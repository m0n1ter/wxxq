#!/bin/sh
head="<html><head><meta charset='utf-8' /><style>body{background-color:#000;line-height: 24px;font-size: 14px;color: #eae7e7;}</style></head><body>"
end="</body></html>"
for file in `ls *.html`
do
    content=`cat $file`
    content=$head"$content"$end
    echo "$content" > $file
done
