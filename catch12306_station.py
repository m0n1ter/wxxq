# -*- coding:utf-8 -*-
import time
import urllib
import urllib2
import os
import json as jn
import ssl
import sys
import Queue
import threading
from proxy_ips import proxy_ip
from MysqlUtil import sqlSessionFactory
default_encoding = 'utf-8'
from train_no_dict import train_codes
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
def  get(p):
    time.sleep(1)
    p = p.encode('utf-8')
    context = ssl._create_unverified_context()
    response = urllib.urlopen(p,context=context)
    content = response.read()
    response.close()
    return content.decode('UTF-8')

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

def save_train_info(train_info,no):
    # {"trainNum": "D1", "departure": "北京", "arrive": "沈阳","date": "2017-03-25"}
    train_file_name = no+".html"
    last_file_path = 'all_12306stations_415/%s'% train_file_name
    if os.path.exists(last_file_path):
        print '%s has exist!' % train_file_name
    else:
        # content = getByProxy(item_train_url,proxy)
        content = get(train_info)
        with open(last_file_path,'w') as f:
            f.write(content)
            f.flush()
            f.close()

def main():
    if not os.path.exists('all_12306stations_415'):
        os.mkdir('all_12306stations_415')
    else:
        print 'station info path exists!'
    base_url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date=%s"
    train_code_list = sqlSessionFactory.select('select start_station,end_station,train_no,useful_date,train_code from train_code_list')
    get_alia = "select abbreviation from station_name_12306 where station_name = '%s'"
    # single thread
    for one in train_code_list:
        start_station = one[0]
        end_station = one[1]
        train_no = one[2]
        useful_date = one[3]
        train_code = one[4]
        s_alia = sqlSessionFactory.select(get_alia % start_station)
        if len(s_alia)==0:
            s_alia='NAN'
        else:
            s_alia = s_alia[0][0]
        e_alia = sqlSessionFactory.select(get_alia % end_station)
        if len(e_alia)==0:
            e_alia='NAN'
        else:
            e_alia = e_alia[0][0]
        item_url = base_url % (train_no,s_alia,e_alia,useful_date)
        print item_url
        save_train_info(item_url,train_code)

if __name__ == "__main__":
    sqlSessionFactory('172.16.19.203','data','opensesame','img_upload',20)
    main()



