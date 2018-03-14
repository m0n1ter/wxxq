#!/bin/sh
sed -i 's/,/\n/g' sed.txt
sed -i 's/$/=item[&/' sed.txt
awk '{print $0NR}' sed.txt >sed1.txt
sed -i 's/$/]&/' sed1.txt
