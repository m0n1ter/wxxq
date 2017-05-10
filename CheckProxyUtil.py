# -*- coding:utf-8 -*-
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# 检查代理工具

import threading
import Queue
from httpUtil import httpUtil
from MysqlUtil import sqlSessionFactory

sql_proxy = 'select * from train_proxy  group by ip'
ist_proxy = "replace into use_proxy(ip,port)value('%s','%s')"
lock = threading._Condition(threading.Lock())
file_proxy = open('proxy_list.txt','w')
class ProxyUtil(object):
    proxyNum = 0
    def __init__(self,checkUrl,threadNum=10):
        self.checkUrl = checkUrl
        self.queue = Queue.Queue()
        self.threadNum = threadNum
        self.threadPool = []
        self.useful_proxy = []
        self.proxyNum = 0

    def setProxyNum(self,n):
        ProxyUtil.proxyNum = n

    def jobStart(self,sqlUtil):
        proxy_data = sqlUtil.select(sql_proxy)
        self.setProxyNum(len(proxy_data))
        for item in proxy_data:
            self.queue.put(item)
        for i in range(self.threadNum):
            self.threadPool.append(checkProxy(self.queue,self.checkUrl,self.useful_proxy))
        for i in range(self.threadNum):
            self.threadPool[i].join()
        for t in self.threadPool:
            del t

        print '代理检查完毕，可用代理数量:%s' % len(self.useful_proxy)

    def getProxy(self):
        return self.useful_proxy



class checkProxy(threading.Thread):
    def __init__(self,ip_queue,url,useful_proxy):
        threading.Thread.__init__(self)
        self.ip_queue = ip_queue
        self.url = url
        self.useful_proxy = useful_proxy
        self.start()


    def run(self):
        while True:
                if ProxyUtil.proxyNum == 0:
                    break
                item = None
                try:
                    item = self.ip_queue.get(block=False)
                except Exception as e:
                    print  e
                    break
                response = httpUtil.getByProxyParam(self.url,item[1],item[2])
                if response == '' or response == '500':
                    print '%s:%s代理不可用' % (item[1],item[2])
                else:
                    print '%s:%s代理可用' % (item[1],item[2])
                    # sqlSessionFactory.execute(ist_proxy%(item[1],item[2]))
                    self.useful_proxy.append(item)
                with lock:
                    ProxyUtil.proxyNum -= 1
        print  '%s执行完毕' % threading.current_thread()


if __name__ == '__main__':
    sqlSessionFactory('172.16.19.203','data','opensesame','img_upload',30)
    util = ProxyUtil('http://www.ly.com/huochepiao/Handlers/TrainListSearch.ashx?to=baigou&from=tielingxi&trainDate=2017-04-22&PlatId=1&callback=jQuery183004485401697308511',20)
    util.jobStart(sqlSessionFactory)
    file = open('proxy_list','a')
    for item in  util.useful_proxy:
        file.write('%s%s'% (item[1],item[2]))





