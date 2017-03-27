# -*- coding:utf-8 -*-
"""" 抓取去哪儿的每列车的所有站信息"""
import time
import urllib
import urllib2
import os
import json
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
# today = datetime.date.today()
# today = today.strftime("%Y%m%d")
train_url_name = 'train_url_list.txt'
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
    response = urllib.urlopen(p)
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

def save_train_info(train_info):
    # {"trainNum": "D1", "departure": "北京", "arrive": "沈阳","date": "2017-03-25"}
    # p = jn.loads(train_info)
    # train_info = str(train_info).strip('\n').strip(' ')
    p = json.loads(train_info.encode('utf-8'))
    train_file_name = p['trainNum']+".html"
    last_file_path = 'train-stations-qnr/%s'% train_file_name
    if os.path.exists(last_file_path):
        print '%s has exist!' % train_file_name
    else:
        item_train_url = base_url % (p['departure'],p['arrive'],p['trainNum'])
        # content = getByProxy(item_train_url,proxy)
        content = get(item_train_url)
        with open(last_file_path,'w') as f:
            f.write(content)
            f.flush()
            f.close()
        # print '%s has created successfully by %s and ip: %s!' % (train_file_name,threading.current_thread(),proxy)
        # useful_proxy_ips.append(proxy)


if __name__ == "__main__":
    if not os.path.exists('train-stations-qnr'):
        os.mkdir('train-stations-qnr')
    else:
        print 'station info path exists!'
    train_url = open(train_url_name)
    all_url = train_url.readlines()
    # single thread
    for line_param in all_url:
        # print item
        save_train_info(line_param)



