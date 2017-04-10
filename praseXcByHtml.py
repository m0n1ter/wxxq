# -*- coding:utf-8 -*-
# 解析抓取的携程火车价格信息页面
from MysqlUtil import sqlSessionFactory
import Queue
import time
import threading
import codecs
from lxml import etree
import sys
reload(sys)
import os
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
base_path = 'E:/XC/xc-price-html/%s-%s-%s.html'
getPageNameSql = "select * from train_stop__task_xc limit 1"
myDao = sqlSessionFactory('192.100.2.31','data','opensesame','traincrawler',10)
def praseHtml(filePath):
    try:
        html_io = codecs.open(filePath, 'r', 'gb2312')
        content = html_io.read()
        html_io.flush()
        html_io.close()
        tree = etree.HTML(content)
        tbodys = tree.xpath("descendant::table[@class='tb_railway_list']/tbody")
        trs = tbodys[1].xpath("tr")
        for tr in trs:
            tds = tr.xpath("td")
            tds[1].xpath("")

            print tds[2].text
    except Exception as w:
        print w

class PraseCenter(object):
    def __init__(self,num=10):
        self.queue = Queue.Queue()
        self.pool = []
        self.threadNum = num
        self.start()

    def start(self):
        # start Producer
        self.pool.append(Producer(self.queue))
        time.sleep(2)
        # start Consumer
        for i in range(self.threadNum):
            self.pool.append(Consumer(self.queue))

        for i in range(self.threadNum):
            self.pool[i].join()
        print 'prase job have been over!'

class Producer(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.start()

    def run(self):
        while True:
            data = myDao.select(getPageNameSql)
            length = len(data)
            if length == 0:
                break
            if length > 1000:
                time.sleep(2)
            for one in data:
                self.queue.put((one[0],one[2],one(4)))
        print 'produce job has stopped!'

class Consumer(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue = queue
        self.start()

    def run(self):
        while True:
            id,start_alia,end_alia = self.queue.get(block=False)
            file_path = base_path % (id,start_alia,end_alia)
            praseHtml(file_path)
        print '%s has stopped!' % threading.currentThread()



if __name__ == "__main__":
    praseHtml('E:/XC/xc-price-html/714479-abagaqi-xilinhaote.html')