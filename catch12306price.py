# -*- coding:utf-8 -*-
"""" 抓取携程的每列车的所有站信息根据列车号来抓取"""
import time
import datetime
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

# base_url = "http://trains.ctrip.com/TrainBooking/Ajax/GetTrainDataV2.aspx?DepartureCity=%s&ArrivalCity=%s&DepartureDate=2017-04-02&NO=01"
post_param = 'http://kyfw.12306.cn/otn/leftTicket/queryTicketPrice?train_no=%s&from_station_no=%s&to_station_no=%s&seat_types=%s&train_date='
base_path = '12306-price-json/%s'
getStations_sql = 'select id,tno,tdate,start_no,end_no,tid,seat_type from 12306trains where task=0 limit 1000'
update_sql = 'update 12306trains set task = 1 where id =%s'
py_util = PinYin()
py_util.load_word('word.data')
factory = None
http_util = None
def getTrainInfoByStation(id,tno,tdate,startno,endno,tid,seat_type,file_name):
    b_url = post_param % (tid,startno,endno,seat_type)
    item_url = b_url + tdate
    content = ''
    num = 0
    while num<5:
        content = http_util.getByProxyNoSSL(item_url,1)
        if content == '':
            d = datetime.datetime.strptime(tdate,'%Y-%m-%d')
            delta=datetime.timedelta(days=1)
            n_days=d+delta
            tdate = n_days.strftime('%Y-%m-%d')
            item_url = b_url + tdate
            content = http_util.getByProxy(item_url,1)
            num+=1
        else:
            break
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
def consume_job(id,tno,tdate,startno,endno,tid,seat_type):

    file_name = '%s.json' % (id)
    getTrainInfoByStation(id,tno,tdate,startno,endno,tid,seat_type,file_name)

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
                id,tno,tdate,startno,endno,tid,seat_type = self.queue.get()
                consume_job(id,tno,tdate,startno,endno,tid,seat_type)
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
                    self.queue.put((s[0],s[1],s[2],s[3],s[4],s[5],s[6]))
                if length < 1000:
                    break
            else:
                time.sleep(2)

def main():
    # 1.检测可用代理
    global factory
    factory = sqlSessionFactory('172.16.19.203','data','opensesame','img_upload',10)
    util = ProxyUtil('http://api.sports.sina.com.cn/?p=nba&s=match&a=dateMatches&format=json&callback=NBA_JSONP_CALLBACK&date=2017-03-30&dpc=1')
    util.jobStart(factory)
    useful_proxy = util.getProxy()
    global http_util
    http_util = httpUtil(useful_proxy)
    # 2.调度中心开始抓取
    center = ScheduleCenter(20)


if __name__ == "__main__":
    if not os.path.exists('12306-price-json'):
        os.mkdir('12306-price-json')
    main()