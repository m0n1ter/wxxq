# -*- coding:utf-8 -*-
# 抓取http工具
import urllib
import urllib2
import time
import random
import threading
import cookielib
import ssl
context = ssl._create_unverified_context()
class httpUtil(object):
    version = 1.0
    def __init__(self, proxys = []):
        self.proxy_ip = proxys

    @classmethod
    def  get(self,p,charset='utf-8',second = 1):
        time.sleep(second)
        content = ''
        try:
           # p = p.encode('utf-8')
           response = urllib.urlopen(p)
           content = response.read()
           response.close()
           return content.decode(charset)
        except Exception as e :
            print e
            content = '500'
        return content

    @classmethod
    def post(self,req,body,head,charset='utf-8',second = 1):
        time.sleep(second)
        content = ''
        try:
            # cj = cookielib.CookieJar()
            # handler = urllib2.HTTPCookieProcessor(cj)
            # opener = urllib2.build_opener()
            # opener.addheaders.append(('Cookie', 'ASP.NET_SessionSvc=MTAuMTUuMTI4LjI2fDkwOTB8b3V5YW5nfGRlZmF1bHR8MTQ3MDczODMxMTM2OQ; _bfa=1.1490690949980.40f9aq.1.1490690949980.1490690949980.1.1; _bfs=1.1; adscityen=Beijing; page_time=1490690950625'))
            dict = urllib.urlencode(body)
            request = urllib2.Request(req,data = dict)
            for k,v in head.items():
                request.add_header(k,v)
            response = urllib2.urlopen(request)
            # response = opener.open(request)
            content = response.read()
            response.close()
            return content.decode(charset)
        except Exception as e :
            print e
            content = '500'
        return content


    def getByProxy(self ,p,second = 1):
        time.sleep(second)
        content = ''
        random_ip_i = random.randint(0,len(self.proxy_ip)-1)
        item = self.proxy_ip[random_ip_i]
        proxy = '%s:%s' % (item[1],item[2])
        try:
            proxy_handler = urllib2.ProxyHandler({'http': proxy})
            opener = urllib2.build_opener(proxy_handler)
            r = opener.open(p,timeout=10)
            content =  r.read()
        except Exception as e:
            print 'Thread:%swhen catching url`s error:%s'% (threading.currentThread(),e)
            content = '500'
        return content

    def getByProxyNoSSL(self ,p,second = 1):
        time.sleep(second)
        content = ''
        random_ip_i = random.randint(0,len(self.proxy_ip)-1)
        item = self.proxy_ip[random_ip_i]
        proxy = '%s:%s' % (item[1],item[2])
        try:
            proxy_handler = urllib2.ProxyHandler({'http': proxy})
            opener = urllib2.build_opener(proxy_handler)
            urllib2.install_opener(opener)
            r = urllib2.urlopen(p,timeout=10,context=context)
            content =  r.read()
        except Exception as e:
            print 'Thread:%swhen catching url`s error:%s'% (threading.currentThread(),e)
            content = '500'
        return content

    @classmethod
    def getByProxyParam(self ,p,ip,port,second = 1):
        time.sleep(second)
        content = ''
        proxy = '%s:%s' % (ip,port)
        try:
            proxy_handler = urllib2.ProxyHandler({'http': proxy})
            opener = urllib2.build_opener(proxy_handler)
            r = opener.open(p,timeout=5)
            content = r.read()
        except Exception as e:
            print 'Thread:%swhen catching url`s error:%s'% (threading.currentThread(),e)
            content = '500'
        return content


if __name__ == "__main__":
    util = httpUtil()
    # print util.get('http://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getSearchList&value={"IsBus":false,"Filter":"0","Catalog":"","IsGaoTie":false,"IsDongChe":false,"CatalogName":"","DepartureCity":"yimianpo","ArrivalCity":"chenggaozi","HubCity":"","DepartureCityName":"一面坡","ArrivalCityName":"成高子","DepartureDate":"2017-03-29","DepartureDateReturn":"2017-03-31","ArrivalDate":"","TrainNumber":""}','gb2312')
    # req = 'http://trains.ctrip.com/TrainBooking/Ajax/SearchListHandler.ashx?Action=getSearchList'
    # body ={'value':'{"IsBus":false,"Filter":"0","Catalog":"","IsGaoTie":false,"IsDongChe":false,"CatalogName":"","DepartureCity":"wanyuan","ArrivalCity":"xiaohezhen","HubCity":"","DepartureCityName":"万源","ArrivalCityName":"小河镇","DepartureDate":"2017-03-29","DepartureDateReturn":"2017-03-31","ArrivalDate":"","TrainNumber":""}'}
    # # head = { 'If-Modified-Since':'Thu, 01 Jan 1970 00:00:00 GMT','Origin':'http://trains.ctrip.com','Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8','Host':'trains.ctrip.com','Referer':'http://trains.ctrip.com/TrainBooking/Search.aspx?from=quzhou&to=hangzhou&day=2&number=&fromCn=%E1%E9%D6%DD&toCn=%BA%BC%D6%DD'}
    # # head.update({"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36"})
    # head = {'Referer':'http://trains.ctrip.com/TrainBooking/Search.aspx?from=beijing&to=shanghai&day=2&number=&fromCn=%B1%B1%BE%A9&toCn=%C9%CF%BA%A3'}
    # print util.post(req,body,{},'gb2312')
