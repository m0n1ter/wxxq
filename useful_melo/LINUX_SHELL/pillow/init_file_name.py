#-*- coding:utf-8 -*-
from PIL import Image
import random
import os
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)



def liu_heng():
    base = 'C:/Users/Administrator/Desktop/留痕/History/'
    base = unicode(base , "utf8")
    base2 = 'C:/Users/Administrator/Desktop/留痕/New/'
    base2 = unicode(base2 , "utf8")
    if os.path.exists(base2):
        os.rmdir(base2)
    os.mkdir(base2)
    data_pattern = "2017-09-%s.%s"
    num_patter = '%s-%s'
    dirs = os.listdir(base)
    for dir in dirs:
        if os.path.isdir(base+dir) and not os.path.exists(base2+dir):
            os.mkdir(base2+dir)
        if os.path.isdir(base+dir):
            print dir
            childs = os.listdir(base+dir)
            num = len(childs)
            tick = 30/num
            num_dict = {}
            for item in childs:
                i=item.rindex('.')
                back = item[i+1:]
                n =random.randint(1, 30)
                if n in num_dict:
                    num_dict[n] = num_dict[n] + 1
                    n = num_patter % (n,num_dict[n])
                else:
                    num_dict[n] = 0
                new_name = base2+dir+'/'+data_pattern % (n,back)
                old_name = base+dir+'/'+item
                old_name = unicode(str(old_name),'utf-8')
                print old_name,new_name
                try:
                    #os.rename(old_name,new_name)
		    Image.open(old_name).save(new_name)
                except:
                    pass

def process_ip_file():
    base = 'C:/Users/Administrator/Desktop/IPBelly/'
    dirs = os.listdir(base)
    final_ip_file = open('final_ip.csv','w')
    for dir in dirs:
        print base+dir
        ips = open(base+dir).readlines()
        for line in ips:
            final_ip_file.write(line)


if __name__ == '__main__':
    liu_heng()
