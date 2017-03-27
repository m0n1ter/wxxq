# -*- coding: UTF-8 -*-
import codecs
from lxml import etree
import sys
reload(sys)
import os
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

base_dir = 'train-stations-xc-useful/'
ss = open('station-2-xc.csv','w')
# ss = open('xc-train-stations.csv','w')
base_str = "%s,%s,%s,%s,%s,%s,%s,%s,%s\n"
total = 0
train_type_dic ={'C':'城际高速','D':'动车组','G':'高速动车','T':'空调特快','K':'快速','Y':'旅游列车','Z':'直达特快'}

def compareSS(start,end):
    s_min = str(start).split(':')
    e_min = str(end).split(':')
    s_int = int(s_min[0])*60+int(s_min[1])
    e_int = int(e_min[0])*60+int(e_min[1])
    duration = e_int-s_int
    return duration*60

def getDaysSS(start,end,days):
    s_min = str(start).split(':')
    e_min = str(end).split(':')
    s_int = int(s_min[0])*60+int(s_min[1])
    e_int = int(e_min[0])*60+int(e_min[1])
    duration = 0
    if days == 0:
        duration = e_int-s_int
    else:
        duration = e_int+24*60-s_int
    return duration*60

def parseHtml(path,no):
    name_list = []
    try:
        html_io = codecs.open(path, 'r', 'utf-8')
        content = html_io.read()
        html_io.flush()
        html_io.close()
        tree = etree.HTML(content)
        nodes_name = tree.xpath("descendant::div[@class='s_bd']/table")
        if len(nodes_name) != 2:
            return ''
        global total
        total +=1
        trs = nodes_name[1].xpath("tbody/tr")
        i = 0
        start_time = trs[0].xpath('td')[4].text.strip()
        pre_time = start_time
        duration = 0
        days = 0
        for tr in trs:
            tds = tr.xpath('td')
            sequence = tds[1].text.strip()
            td2 = tds[2].xpath('a')
            name =td2[0].text.strip()
            name_list.append(name)
            arriveTime = tds[3].text.strip()
            if i==0:
                arriveTime = 0
            else:
                if compareSS(pre_time,arriveTime)<0:
                    days +=1
                duration = duration + getDaysSS(start_time,arriveTime,days)
                pre_time = arriveTime
            departTime = tds[4].text.strip()
            stayTime = tds[5].text.strip()
            if stayTime :
                stayTime = stayTime[0:str(stayTime).index('分')]
            # print '%s,%s,%s,%s,%s' % (sequence,name,arriveTime,departTime,stayTime)
            pre_char = no[0:1].upper()
            train_type = ''
            if not pre_char in train_type_dic.keys():
                train_type = '普快'
            else:
                train_type = train_type_dic[pre_char]
            item_str = base_str % (no,name,sequence,arriveTime,stayTime,days,duration,departTime,train_type)
            # ss.write( item_str)
            i +=1
    except UnicodeDecodeError,a:
        print no
        # raise a
    except Exception as e :
        pass
        # print e

    # 输出站到站
    num = len(name_list)
    # print name_list
    for i in range(num):
        for j in range(num):
            if i == j:
                continue
            ss.write( '%s,%s\n' % (name_list[i],name_list[j]))
            print '%s,%s' % (name_list[i],name_list[j])

if __name__ == "__main__":
    files = os.listdir(base_dir)
    for f in files:
        item_path = '%s%s' % (base_dir,f)
        train_no = f[0:f.rindex('.')]
        # print item_path
        parseHtml(item_path,train_no)
    ss.flush()
    ss.close()
    print total
