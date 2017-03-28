# -*- coding:utf-8 -*-
"""" 抓取携程的每列车的所有站信息根据列车号来抓取"""
import time
import urllib
import urllib2
import os
import json
from proxy_ips import proxy_ip
import random
from pinyin import PinYin
import sys
import Queue
import threading
import MySQLdb
from DBUtils.PooledDB import PooledDB
# 5为连接池里的最少连接数
pool = PooledDB(MySQLdb,5,host='192.100.2.31',user='data',passwd='opensesame',db='traincrawler',port=3306)
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# base_url = "http://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getSearchList&value="
post_param = 'http://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getSearchList&value={"IsBus": False, "Filter": "0", "Catalog": "", "IsGaoTie":False, "IsDongChe":False, "CatalogName": "", "DepartureCity": %s, "ArrivalCity": %s, "HubCity": "", "DepartureCityName": %s, "ArrivalCityName": %s, "DepartureDate": "2017-03-24", "DepartureDateReturn": "2017-03-26", "ArrivalDate": "", "TrainNumber": ""}'
base_path = 'xc-station-pages/%s.json'
getStations_sql = 'select id,begin_stop,end_stop from train_stop_20170331_task where task=0 limit 100'
update_sql = 'update train_stop_20170331_task set task = 1 where id =%s'
def  get(p):
    time.sleep(1)
    content = ''
    try:
       p = p.encode('utf-8')
       response = urllib.urlopen(p)
       content = response.read()
       response.close()
       return content.decode('gb2312')
    except Exception as e :
        print e
        content = '500'
    return content

def getByProxy(p):
    time.sleep(1)
    content = ''
    random_ip_i = random.randint(0,len(proxy_ip)-1)
    proxy = proxy_ip[random_ip_i]
    try:
        proxy_handler = urllib2.ProxyHandler({'http': proxy})
        opener = urllib2.build_opener(proxy_handler)
        r = opener.open(p)
        return r.read().decode('UTF-8')
    except Exception as e:
        print 'Thread:%swhen catching url`s error:%s'% (threading.currentThread(),e)
        content = '500'
    return content

def update(sql):
        conn = pool.connection()
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()

def getStations():
    conn = pool.connection()
    cur = conn.cursor()
    rtn = cur.execute(getStations_sql)
    stations = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return stations

def getTrainInfoByStation(startStation,endStation,s_py,e_py,id):
    item_url = post_param % (s_py,e_py,startStation,endStation)
    content = get(item_url)
    if content == '500':
        # 网络异常
        return ''
    print item_url
    file_path = base_path % id
    with open(file_path,'w') as f:
            f.write(content)
            f.flush()
            f.close()
    item_sql = update_sql % id
    update(item_sql)

# job start
def consume_job(startStation,endStation,id):
    py_util = PinYin()
    py_util.load_word('word.data')
    s_py = py_util.hanzi2pinyin_split(string=startStation, split="", firstcode=False)
    e_py = py_util.hanzi2pinyin_split(string=endStation, split="", firstcode=False)
    getTrainInfoByStation(startStation,endStation,s_py,e_py,id)

class ScheduleCenter(object):
    def __init__(self,threadNum=10):
        self.resource = Queue.Queue()
        self.threads = []
        self.__init_produce()
        self.__init_thread_pool(threadNum)

    def __init_thread_pool(self,num):
        time.sleep(2)
        for i in range(num):
            self.threads.append(Consume_Work(self.resource))

    def __init_produce(self):
        self.threads.append(Produce_Work(self.resource))

class Consume_Work(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.start()

    def run(self):
        while True:
            try:
                startStation,endStation,id = self.queue.get()
                consume_job(startStation,endStation,id)
            except Exception as e:
                print '%s:jobing:%s' % (threading.currentThread(),e)

class Produce_Work(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.start()

    def run(self):
        while True:
            stations = getStations()
            length = len(stations)
            for s in stations:
                self.queue.put((s[1],s[2],s[0]))
            time.sleep(100)
            if length < 100:
                break

if __name__ == "__main__":
    if not os.path.exists('xc-station-pages'):
        os.mkdir('xc-station-pages')
    else:
        print 'xc-station-pages path exists!'
    # center = ScheduleCenter(1)
    # driver.quit()