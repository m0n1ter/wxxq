# -*- coding:utf-8 -*-
import time
import urllib
import urllib2
import os
import json
import ssl
import sys
import datetime
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
    content =""
    try:
        p = p.encode('utf-8')
        context = ssl._create_unverified_context()
        response = urllib.urlopen(p,context=context)
        content = response.read()
        response.close()
    except:
        pass
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

def increaseDate(dateStr,day=1):
    try:
        d = datetime.datetime.strptime(dateStr,'%Y-%m-%d')
        delta=datetime.timedelta(days=day)
        n_days=d+delta
        tDate = n_days.strftime('%Y-%m-%d')
        return tDate
    except Exception ,e:
        print e
    return time.strftime('%Y-%m-%d', time.localtime(time.time()))


def save_train_info(item_url,useful_date,no):
    # {"trainNum": "D1", "departure": "北京", "arrive": "沈阳","date": "2017-03-25"}
    train_file_name = no+".html"
    last_file_path = 'all_12306stations_417/%s'% train_file_name
    if os.path.exists(last_file_path):
        print '%s has exist!' % train_file_name
    else:
        # content = getByProxy(item_train_url,proxy)
        num = -1
        content = ''
        while num<20:
            num += 1
            catch_url = item_url + useful_date
            print catch_url
            content = get(catch_url)
            if content == '':
                continue
            else:
                json_obj = json.loads(content)
                if len(json_obj['data']['data']) == 0:
                    # useful_date = increaseDate(useful_date)
                    return ''
                else:
                    break
        with open(last_file_path,'w') as f:
            f.write(content)
            f.flush()
            f.close()

def main():
    if not os.path.exists('all_12306stations_417'):
        os.mkdir('all_12306stations_417')
    else:
        print 'station info path exists!'
    base_url = "https://kyfw.12306.cn/otn/czxx/queryByTrainNo?train_no=%s&from_station_telecode=%s&to_station_telecode=%s&depart_date="
    train_code_list = sqlSessionFactory.select('SELECT start_station,end_station,train_no,useful_date,train_code from train_code_list GROUP BY train_code,train_no  ORDER BY train_code,useful_date desc')
    get_alia = "select abbreviation from station_name_12306 where station_name = '%s'"
    # single thread
    for one in train_code_list:
        start_station = one[0]
        end_station = one[1]
        train_no = one[2]
        useful_date = one[3].strftime('%Y-%m-%d')
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
        item_url = base_url % (train_no,s_alia,e_alia)
        save_train_info(item_url,useful_date,train_code)

if __name__ == "__main__":
    sqlSessionFactory('172.16.19.203','data','opensesame','img_upload',20)
    main()



