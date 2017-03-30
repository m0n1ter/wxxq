# -*- coding:utf-8 -*-
# 检查代理工具

import threading
import Queue
from httpUtil import httpUtil
from MysqlUtil import sqlSessionFactory

sql_proxy = 'select * from train_proxy where is_use=1 group by ip'
lock = threading._Condition(threading.Lock())

class ProxyUtil(object):
    proxyNum = 0
    def __init__(self,checkUrl,threadNum=10):
        self.checkUrl = checkUrl
        self.queue = Queue.Queue()
        self.threadNum = threadNum
        self.threadPool = []
        self.useful_proxy = Queue.Queue()
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

        print '代理检查完毕，可用代理数量:%s' % self.useful_proxy.qsize()

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
                response = httpUtil.get(self.url)
                if response == '' or response == '500':
                    print '%s:%s代理不可用' % (item[1],item[2])
                else:
                    print '%s:%s代理可用' % (item[1],item[2])
                    self.useful_proxy.put(item)
                lock.acquire()
                try:
                    ProxyUtil.proxyNum -= 1
                finally:
                    lock.release()
        print  '%s执行完毕' % threading.current_thread()


if __name__ == '__main__':
    sqlSessionFactory('192.100.2.31','data','opensesame','traincrawler',10)
    util = ProxyUtil('http://api.sports.sina.com.cn/?p=nba&s=match&a=dateMatches&format=json&callback=NBA_JSONP_CALLBACK&date=2017-03-30&dpc=1')
    util.jobStart(sqlSessionFactory)




