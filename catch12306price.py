# -*- coding:utf-8 -*-
"""" 抓取携程的每列车的所有站信息根据列车号来抓取"""
import time
import datetime
import urllib
import urllib2
import os
import random
import json
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
getStations_sql = 'select id,tno,tdate,start_no,end_no,tid,seat_type,start_station,end_station from 12306trains where task=0 limit 1000'
update_sql = 'update 12306trains set task = 1 where id =%s'
findCodeByIdSql = 'select tno,start_station,tid,seat_type,end_station from 12306trains where id =%s'
findStationSql = "select * from train_line_stop where train_code ='%s' and name ='%s'"
getBegin2EndSql = "SELECT NAME from train_line_stop where train_code = '%s' and (depart_time is NULL or arrive_time is NULL) ORDER BY sequence"
insert_price_sql = "insert INTO train_price_qn_tmp(train_code,name,from_name,start_time,end_time,duration,hard_seat,soft_seat,hard_bed_1,soft_bed_1,class_1,class_2,high_grade_bed_1,business_seat,grade,days,premium_seat,origin_stop,terminal,sequence,train_no,staytime) values('%s','%s','%s','%s','%s',%s,%s,%s,%s,%s,%s,%s,%s,%s,'%s',%s,%s,'%s','%s',%s,'%s',%s)"
py_util = PinYin()
py_util.load_word('word.data')
factory = None
http_util = None

def getPriceByKey(k,price_dic):
    p = 0
    if k in price_dic:
        p = price_dic[k]
        if p:
           p = p[1:]
    return p

def parseHtml(content,train_code,start_station,id,tid,end_station):
    station = factory.select(findStationSql % (train_code,end_station))
    b2e = factory.select(getBegin2EndSql % train_code)
    sequence = station[0][3]
    arrive_time = station[0][4]
    stayTime = station[0][5]
    days = station[0][6]
    duration = station[0][7]
    departTime = station[0][8]
    grade = station[0][9]
    origin = b2e[0][0]
    terminal = b2e[1][0]
    price_json = json.loads(content)
    price_dic = price_json['data']
    A1 = getPriceByKey('A1',price_dic)
    A3 = getPriceByKey('A3',price_dic)
    A4 = getPriceByKey('A4',price_dic)
    A6 = getPriceByKey('A6',price_dic)
    A9 = getPriceByKey('A9',price_dic)
    O = getPriceByKey('O',price_dic)
    M = getPriceByKey('M',price_dic)
    item_sql = insert_price_sql % (train_code,end_station,start_station,departTime,arrive_time,duration,A1,0,A3,A4,O,M,A6,A9,grade,days,0,origin,terminal,sequence,tid,stayTime)
    factory.execute(item_sql)

def getTrainInfoByStation(id,tno,tdate,startno,endno,tid,seat_type,start_station,end_station):
    b_url = post_param % (tid,startno,endno,seat_type)
    item_url = b_url + tdate
    content = ''
    num = -1
    while num<10:
        num+=1
        content = http_util.getByProxyNoSSL(item_url,1)
        if content == '':
            d = datetime.datetime.strptime(tdate,'%Y-%m-%d')
            delta=datetime.timedelta(days=1)
            n_days=d+delta
            tdate = n_days.strftime('%Y-%m-%d')
            item_url = b_url + tdate
            content = http_util.getByProxyNoSSL(item_url,1)
        else:
            if content == '500':
                continue
            price_json = json.loads(content)
            if len(price_json['data']) ==2 :
                d = datetime.datetime.strptime(tdate,'%Y-%m-%d')
                delta=datetime.timedelta(days=1)
                n_days=d+delta
                tdate = n_days.strftime('%Y-%m-%d')
                item_url = b_url + tdate
                content = http_util.getByProxyNoSSL(item_url,1)
            else:
                break
    if content == '500':
        # 网络异常
        return ''
    print item_url
    # file_path = base_path % file_name
    # with open(file_path,'w') as f:
    #         f.write(content)
    #         f.flush()
    #         f.close()
    try:
        parseHtml(content,tno,start_station,id,tid,end_station)
        item_sql = update_sql % id
        factory.execute(item_sql)
    except Exception as e:
        print e


# job start
def consume_job(id,tno,tdate,startno,endno,tid,seat_type,start_station,end_station):

    # file_name = '%s.json' % (id)
    try:
        getTrainInfoByStation(id,tno,tdate,startno,endno,tid,seat_type,start_station,end_station)
    except Exception as w:
        print  w

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
                id,tno,tdate,startno,endno,tid,seat_type,start_station,end_station = self.queue.get()
                consume_job(id,tno,tdate,startno,endno,tid,seat_type,start_station,end_station)
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
                    self.queue.put((s[0],s[1],s[2],s[3],s[4],s[5],s[6],s[7],s[8]))
                if length < 1000:
                    break
            else:
                time.sleep(2)

def main():
    # 1.检测可用代理
    global factory
    factory = sqlSessionFactory('172.16.19.203','data','opensesame','img_upload',20)
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