# -*- coding: UTF-8 -*-
import sys
import os
import json
from train_no_dict import train_no_date,train_no_id
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
import codecs
base_train_list_path = "train-stations-12306/"
import MySQLdb
from DBUtils.PooledDB import PooledDB
# 5为连接池里的最少连接数
# pool = PooledDB(MySQLdb,5,host='192.100.2.31',user='data',passwd='opensesame',db='traincrawler',port=3306)
pool = None
ist_sql_patter = "insert into train_line_stop_test(train_code,name,sequence,arrive_time,staytime,days,duration,depart_time,grade)value('%s','%s',%s,'%s',%s,%s,%s,'%s','%s')"
base_str = "%s,%s,%s,%s,%s,%s,%s,%s,%s\n"
check_added_sql = "select count(*) from train_line_stop_test where train_code = '%s'"
delete_added_sql = "delete from train_line_stop_test where train_code = '%s'"
# ss = open('all-12306-train-stations.csv','w')
log = open('no-all-station-2-12306.csv','w')
total = 0
def insert_train_ss(sql):
     conn = pool.connection()
     cur = conn.cursor()
     sql = sql.encode('utf-8')
     rtn = cur.execute(sql)
     cur.close()
     conn.commit()
     conn.close()
     return rtn

def check_exist(trainNo,size):
    item_check_sql = check_added_sql % trainNo
    count = insert_train_ss(item_check_sql)
    isAdded = 0
    if count == size:
        isAdded = 1
    if count != 0:
        pass
        # insert_train_ss(delete_added_sql % trainNo)
    return isAdded

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

def parse_ss_json(content,no):
    json_ss = json.loads(content.encode('utf-8'))
    if  json_ss['data']:
        data = json_ss['data']['data']
        typeName = data[0]['train_class_name']
        start_time = data[0]['start_time']
        pre_time = start_time
        duration = 0
        name_list = {}
        days = 0
        for i,d in enumerate(data):
            """arrive_time": "17:17",
                "station_name": "乐山",
                "start_time": "17:19",
                "stopover_time": "2分钟",
                "station_no": "02",
                "isEnabled": true
            """
            arrive_time = d['arrive_time']
            depart_time = d['start_time']
            if i==0 and d['arrive_time']=='----':
                arrive_time = 0
            if i != 0:
                if compareSS(pre_time,arrive_time)<0:
                    days +=1
                duration = duration + getDaysSS(start_time,d['arrive_time'],days)
                pre_time = arrive_time
            stayTime = 0
            if i!=0 and i!= len(data)-1 :
                stayTime = d['stopover_time']
                try:
                    stayTime = stayTime[0:str(stayTime).index('分')]
                except Exception as e:
                    stayTime=0
                    print e
            # item_sql = ist_sql_patter % (trainNo,station['stationName'],station['stationNo'],arrive_time,station['overTime'],0,duration,depart_time,typeName)
            # insert_train_ss(item_sql)
            # item_str = base_str % (no,d['station_name'],int(d['station_no']),arrive_time,stayTime,days,duration,depart_time,typeName)
            # ss.write(item_str)
            name_list.update({d['station_no']:d['station_name']})
         # 输出站到站
        num = len(name_list)
        kvs = name_list.items()
        global total
        total +=len(data)
        i = -1
        # print name_list
        for ki,vi in kvs:
            i += 1
            j = -1
            for kj,vj in  kvs:
                j += 1
                if i == j:
                    continue
                log.write('%s,%s,%s,%s,%s,%s,%s\n' % (no,ki,vi,kj,vj,train_no_id[no],train_no_date[no]))
                # print '%s,%s,%s,%s,%s,%s,%s\n' % (no,ki,vi,kj,vj,train_no_id[no],train_no_date[no])

def exist(no,trains):
    e = 0
    for i in trains:
        if i == no :
            e = 1
            break
    return e

def main():
    all = os.listdir(base_train_list_path)
    all.sort()
    for i in all:
        train_no = i[0:i.rindex('.')]
        print train_no
        html_old = codecs.open(base_train_list_path+i, 'r', 'utf-8')
        content = html_old.read()
        html_old.close()
        parse_ss_json(content,train_no)
    print total

def part_main():
    temp_trains = ['6267','6285','C6501','C6505','C6509','D5113','D5517','D6410','D6412','D6418','D6422','D8324','D8386','D932','D936','D942','G1839','G1840','G1855','G1857','K1169','K1321','K1322','K1349','K1351','K1353','K1531','K1533','K1617','K1807','K1808','K1888','K2368','K2615','K2617','K2618','K4332','K4333','K4346','K4347','K5156','K5158','K59','K61','K7222','K7307','K7308','K749','K789','K791','K792','K803','K804','K805','K8483','K861','K863','K9069','K9070','K9505','K9507','K9508','K9510','T153','T283','T8317','T8327','T8711','T9591','T9594']
    for t in temp_trains:
        file_name = '%s%s.html' % (base_train_list_path,t)
        html_old = codecs.open(file_name, 'r', 'utf-8')
        content = html_old.read()
        html_old.close()
        print t
        parse_ss_json(content,t)
if __name__ == '__main__':
    main()

