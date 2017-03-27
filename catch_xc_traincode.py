# -*- coding:utf-8 -*-
"""" 抓取携程的每列车的所有站信息根据列车号来抓取"""
import time
import urllib
import urllib2
import os
import json
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

train_url_name = 'train_code_xc.txt'

base_url = 'http://trains.ctrip.com/trainbooking/TrainSchedule/%s/'

def  get(p):
    time.sleep(1)
    try:
       p = p.encode('utf-8')
       response = urllib.urlopen(p)
       content = response.read()
       response.close()
       return content
    except Exception as e :
        print e
    return ''

def getByProxy(p,proxy):
    time.sleep(1)
    try:
        proxy_handler = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(proxy_handler)
        r = opener.open(p)
        return r.read().decode('UTF-8')
    except Exception as e:
        print e
    return ""

def save_train_info(train_info):
    last_file_path = 'train-stations-xc/%s.html' % train_info
    if os.path.exists(last_file_path):
        print '%s has exist!' % train_info
    else:
        item_train_url = base_url % train_info
        # content = getByProxy(item_train_url,proxy)
        content = get(item_train_url)
        with open(last_file_path,'w') as f:
            f.write(content)
            f.flush()
            f.close()

if __name__ == "__main__":
    if not os.path.exists('train-stations-xc'):
        os.mkdir('train-stations-xc')
    else:
        print 'station info path exists!'
    train_url = open(train_url_name)
    all_url = train_url.readlines()
    # single thread
    for line_param in all_url:
        # print line_param.encode('utf-8')
        save_train_info(line_param.encode('utf-8').strip('\n'))
    train_url.flush()
    train_url.close()



