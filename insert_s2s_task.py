# -*- coding:utf-8 -*-
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
from MysqlUtil import sqlSessionFactory
from pinyin import PinYin
GET_STATION = "select * from station_station where fetched = 0 limit 10000"
INSERT_S2S = "INSERT INTO `station_task_tc` (`begin_stop`, `ctrip_begin_stop`, `end_stop`, `ctrip_end_stop`, `status`, `nice`, `selected`, `fetched_date`, `http_code`) VALUES ( '%s', '%s', '%s', '%s', '0', '0', '0', '2017-05-01', -1);"
GET_ALIA_STATION = "select quanpin from station_name_tc where name = '%s'"
UPDATE_S2S = "update station_station set fetched =1 where id = %s"
py_util = PinYin()
py_util.load_word('word.data')
def main():
    sqlSessionFactory('172.16.19.203','data','opensesame','img_upload',20)
    while True:
        s2ss =sqlSessionFactory.select(GET_STATION)
        if len(s2ss)==0:
            break
        for s in s2ss:
            id = s[0]
            start_station = s[1]
            end_station = s[2]
            s_alia = sqlSessionFactory.select(GET_ALIA_STATION % start_station)
            if len(s_alia)==0:
                s_alia =  py_util.hanzi2pinyin_split(string=start_station, split="", firstcode=False)
            else:
                s_alia = s_alia[0][0]
            e_alia = sqlSessionFactory.select(GET_ALIA_STATION % end_station)
            if len(e_alia)==0:
                e_alia =  py_util.hanzi2pinyin_split(string=end_station, split="", firstcode=False)
            else:
                e_alia = e_alia[0][0]
            try:
                insert_sql =INSERT_S2S % (start_station,s_alia,end_station,e_alia)
                print insert_sql
                sqlSessionFactory.execute(insert_sql)
            except:
                pass
            update = UPDATE_S2S % id
            sqlSessionFactory.execute(update)



def init_trainlist_file():
    f=open('E:/Important/12306/praseJs/train_list.js','a')
    f.write(';')
    f.write('\nexports.train_list = train_list;')


if __name__ == '__main__':
    # main()
    init_trainlist_file()
    print 'finished'


