# -*- coding:utf-8 -*-
import sys
import json
import mycurl
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

# 检查代理工具

import threading
import Queue
from httpUtil import httpUtil
from MysqlUtil import sqlSessionFactory

sql_proxy = 'select * from train_proxy_500 where is_use=0'
# ist_proxy = "replace into use_proxy(ip,port)value('%s','%s')"
lock = threading._Condition(threading.Lock())
file_proxy = open('proxy_list.txt','a')
DOWNLOAD_HEADERS = [
    "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language:zh-CN,zh;q=0.8,en;q=0.6"
    "Connection: close",
    "Host: mapi.dianping.com",
    "User-Agent:Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36",
    "Upgrade-Insecure-Requests:1"]

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
                proxy_str = '%s:%s' % (item[1],item[2])
                can_use =False
                try:
                    content = mycurl.get(url=self.url,request_headers=DOWNLOAD_HEADERS,timeout=10,proxy=proxy_str)
                    if content.status == 200:
                        info = json.loads(content.body.decode('utf-8'))
                        if info['recordCount']:
                            can_use = True
                except:
                    pass
                if can_use:
                    print '%s:%s代理可用' % (item[1],item[2])
                    self.useful_proxy.append(item)
                    sqlSessionFactory.execute('update train_proxy_500 set is_use=500 where id=%s'% item[0])
                else:
                    print '%s:%s代理不可用' % (item[1],item[2])
                with lock:
                    ProxyUtil.proxyNum -= 1
        print  '%s执行完毕' % threading.current_thread()


if __name__ == '__main__':
    sqlSessionFactory('172.16.19.203','data','opensesame','img_upload',30)
    util = ProxyUtil('http://mapi.dianping.com/searchshop.json?start=0&regionid=0&categoryid=10&cityid=2',20)
    util.jobStart(sqlSessionFactory)
    # file = open('proxy_list','w')
    for item in  util.useful_proxy:
        file_proxy.write('%s%s'% (item[1],item[2]))
    print util.useful_proxy





