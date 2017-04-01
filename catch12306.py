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
default_encoding = 'utf-8'
from train_no_dict import train_codes
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
# today = datetime.date.today()
# today = today.strftime("%Y%m%d")
train_url_name = '12306-trains.txt'
# base_url = 'http://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getIntermediateStopList&value='
base_url = 'http://train.qunar.com/dict/open/seatDetail.do?dptStation=%s&arrStation=%s&date=2017-03-22&trainNo=%s&user=neibu&source=www&needTimeDetail=true'
useful_proxy_ips = []
# with open(train_list_path) as f:


# for p in train_url.readlines():
#     # print p
#     last_index = p.rindex("/")
#     item_path_name = p[last_index+1:-1]
#     item_path_name = base_train_list_path +item_path_name+".html"
#     print item_path_name
#     response = urllib.urlopen(p)
#     content = response.read()
#     response.close()
#     print content
#     with open(item_path_name, "w") as f:
#         f.write(content)
#         time.sleep(3)

#http://train.qunar.com/dict/open/seatDetail.do?dptStation=北京南&arrStation=上海虹桥&date=2017-03-22&trainNo=G101&user=neibu&source=www&needTimeDetail=true
# get('http://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getIntermediateStopList&value={"trainNum":"K1624","departure":"汉口","arrive":"连云港东","date":"2017-03-22"')
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
    last_file_path = 'added12306/%s'% train_file_name
    if os.path.exists(last_file_path):
        print '%s has exist!' % train_file_name
    else:
        # content = getByProxy(item_train_url,proxy)
        content = get(train_info)
        with open(last_file_path,'w') as f:
            f.write(content)
            f.flush()
            f.close()

class WorkManager(object):
    def __init__(self, all_url,ips):
        self.work_queue = Queue.Queue()
        self.threads = []
        self.__init_work_queue(all_url)
        self.__init_thread_pool(ips)

    """
        初始化线程
    """
    def __init_thread_pool(self,ips):
        length = len(ips)/5
        for i in range(length):
            proxy_ip_list = ips[i*5:(i+1)*5]
            self.threads.append(Work(self.work_queue,proxy_ip_list))

    """
        初始化工作队列
    """
    def __init_work_queue(self, all_url):
        for i in all_url:
            self.work_queue.put(i)#任务入队，Queue内部实现了同步机制

    """
        等待所有线程运行完毕
    """
    def wait_allcomplete(self):
        for item in self.threads:
            if item.isAlive():item.join()

class Work(threading.Thread):
    def __init__(self, work_queue, proxy_ip_list):
        threading.Thread.__init__(self)
        self.work_queue = work_queue
        self.proxy_list = proxy_ip_list
        self.start()

    def run(self):
        i = 0
        rindex = len(self.proxy_list)
        # 死循环，从而让创建的线程在一定条件下关闭退出
        while True:
            try:
                if i==rindex :
                    i =0
                item_param = self.work_queue.get(block=False)#任务异步出队，Queue内部实现了同步机制
                save_train_info(item_param,self.proxy_list[i])
                i += 1
            except Exception as e:
                print e
                break

if __name__ == "__main__":

    if not os.path.exists('added12306'):
        os.mkdir('added12306')
    else:
        print 'station info path exists!'
    train_url = open(train_url_name)
    all_url = train_url.readlines()
    # single thread
    for i,line_param in enumerate(all_url):
        print line_param
        save_train_info(line_param,train_codes[i])
    # more threads
    # start = time.time()
    # work_manager =  WorkManager(all_url,proxy_ip)
    # work_manager.wait_allcomplete()
    # end = time.time()
    # print useful_proxy_ips
    # print "cost all time: %s" % (end-start)


