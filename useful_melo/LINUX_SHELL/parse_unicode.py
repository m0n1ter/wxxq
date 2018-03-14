# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import os
file_name=sys.argv[1]
file=open(file_name)
new_file_name = file_name+".cn"
w=open(new_file_name,'w')
# str="\u5e7f\u4e1c\u7701"
# print str.decode("unicode_escape")
for line in file.readlines():
    w.write(line.decode("unicode_escape")+"\n")