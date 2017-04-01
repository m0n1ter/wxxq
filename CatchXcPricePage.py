# -*- coding:utf-8 -*-
"""" 抓取携程的每列车的所有站信息根据列车号来抓取"""
import time
import urllib
import urllib2
import os
import random
from pinyin import PinYin
import sys
import Queue
import threading
from CheckProxyUtil import ProxyUtil
from MysqlUtil import sqlSessionFactory
from httpUtil import httpUtil
# 5为连接池里的最少连接数
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

base_url = "http://trains.ctrip.com/TrainBooking/Ajax/GetTrainDataV2.aspx?DepartureCity=%s&ArrivalCity=%s&DepartureDate=2017-04-02&NO=01"
# post_param = 'http://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getSearchList&value={"IsBus": False, "Filter": "0", "Catalog": "", "IsGaoTie":False, "IsDongChe":False, "CatalogName": "", "DepartureCity": %s, "ArrivalCity": %s, "HubCity": "", "DepartureCityName": %s, "ArrivalCityName": %s, "DepartureDate": "2017-03-24", "DepartureDateReturn": "2017-03-26", "ArrivalDate": "", "TrainNumber": ""}'
base_path = 'xc-price/%s'
getStations_sql = 'select id,begin_stop,begin_alia,end_stop,end_alia from train_stop__task_xc where task=0 limit 1000'
update_sql = 'update train_stop__task_xc set task = 1 where id =%s'
py_util = PinYin()
py_util.load_word('word.data')
factory = None
http_util = None
def getTrainInfoByStation(s_py,e_py,id,file_name):
    item_url = base_url % (s_py,e_py)
    content = http_util.getByProxy(item_url,1)
    if content == '500':
        # 网络异常
        return ''
    print item_url
    file_path = base_path % file_name
    with open(file_path,'w') as f:
            f.write(content)
            f.flush()
            f.close()
    item_sql = update_sql % id
    factory.execute(item_sql)

# job start
def consume_job(id,startStation,start_alia,endStation,end_alia):
    s_py = start_alia
    e_py = end_alia
    s = start_alia
    e = end_alia
    if start_alia == '#N/A':
        s = 'NAN'
        s_py = py_util.hanzi2pinyin_split(string=startStation, split="", firstcode=False)
    if end_alia == '#N/A':
        e = 'NAN'
        e_py = py_util.hanzi2pinyin_split(string=endStation, split="", firstcode=False)
    file_name = '%s-%s-%s.html' % (id,s,e)
    getTrainInfoByStation(s_py,e_py,id,file_name)

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
                id,startStation,start_alia,endStation,end_alia = self.queue.get()
                consume_job(id,startStation,start_alia,endStation,end_alia)
            except Exception as e:
                print '%s:jobing:%s' % (threading.currentThread(),e)

class Produce_Work(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.start()

    def run(self):
        while True:
            if self.queue.qsize() < 1000:
                stations = factory.select(getStations_sql)
                length = len(stations)
                for s in stations:
                    self.queue.put((s[0],s[1],s[2],s[3],s[4]))
                if length < 1000:
                    break
            else:
                time.sleep(2)

def main():
    # 1.检测可用代理
    global factory
    factory = sqlSessionFactory('192.100.2.31','data','opensesame','traincrawler',10)
    util = ProxyUtil('http://api.sports.sina.com.cn/?p=nba&s=match&a=dateMatches&format=json&callback=NBA_JSONP_CALLBACK&date=2017-03-30&dpc=1')
    util.jobStart(factory)
    useful_proxy = util.getProxy()
    global http_util
    http_util = httpUtil(useful_proxy)
    # 2.调度中心开始抓取
    center = ScheduleCenter(20)


if __name__ == "__main__":
    if not os.path.exists('xc-price'):
        os.mkdir('xc-price')
    main()