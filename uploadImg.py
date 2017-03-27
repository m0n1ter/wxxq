# -*- coding: UTF-8 -*-
import MySQLdb
import os
import json
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from lastIds import last_ids
import urllib2
import datetime
import time
import MySQLdb
from DBUtils.PooledDB import PooledDB
# 5为连接池里的最少连接数
pool = PooledDB(MySQLdb,5,host='172.16.19.203',user='data',passwd='opensesame',db='img_upload',port=3306)
#pool.connection()
register_openers()

node_ips = ['192.100.2.5','192.100.2.7','192.100.2.9']
# sql:check some img has uploaded ? batch
query = "select * from upload_log g where g.shop_id = %s "
# need uploaded img path
img_base_path = "D:/BaiduNetdiskDownload/images/"
# img_base_path = "~/dianpingimg/pics/"
# log = need to insert
add_log_sql = "INSERT INTO `upload_log`(user_id,shop_id,image_name,image_id,ok,error_msg,http_code,batch,md5,ip_node,source,update_time,create_time) VALUE ( %s, %s, '%s', '%s', %s, '%s', %s, '%s', '%s', '%s', %s, NOW(), NOW())"
# api - upload img
base_upload_url = "http://%s:8180/chelsea/image/upload_image.action"
# get random user from tbl_user_info
random_user_sql = "SELECT user_id FROM `tbl_user_info` WHERE user_id >= (SELECT floor( RAND() * ((SELECT MAX(user_id) FROM `tbl_user_info`)-(SELECT MIN(user_id) FROM `tbl_user_info`)) + (SELECT MIN(user_id) FROM `tbl_user_info`))) ORDER BY user_id LIMIT 1"


class uploadUtil:
    def __init__(self):
        pass


    # round node ip
    def round_node_ip(self):
        global p
        if p > 2:
            p = 0
        ip = node_ips[p]
        # print ip
        p += 1
        return ip


    # check img has uploaded ?
    def check_exist(self,shop_id):
        conn = pool.connection()
        cur = conn.cursor()
        is_Exist_sql = query % shop_id
        rtn = cur.execute(is_Exist_sql)
        isExist = 0
        if rtn > 0:
            isExist = 1
        cur.close()
        conn.close()
        return isExist

    def check_exist_byId(self,shop_id):
        isExist = 0
        for item in last_ids:
            if str(item) == shop_id:
                isExist = 1
        return isExist

    def saveLog(self,sql):
        conn = pool.connection()
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()

    # data = cur.fetchall()
    # print len(data)


    def upload_img(self,param):
        response = {}
        http_code = 200
        try:
            # print param['node_ip']
            temp_upload_url = base_upload_url % (param['node_ip'])
            datagen, headers = multipart_encode({"pic": open(param['img_path'], "rb"),"user_id":param['user_id'],"shop_id":param['shop_id'],"source":param['source'],"title":param['title'],"type":param['type'],"duplicate":param['duplicate']})
            request = urllib2.Request(temp_upload_url, datagen, headers)
            res_temp = urllib2.urlopen(request).read()
            print res_temp
            response = json.loads(res_temp)
        except Exception as err:
            print err
            response['status'] = 0
            http_code = 500
        res = {}
        res['status'] = response['status']
        res['http_code'] = http_code
        res['error'] = ''
        if res['status'] == 1:
            res['img_id'] = response['result'][0]['imageId']
        else:
            res['img_id'] = ''
            if 'result' in response.keys():
                for item in response['result']:
                    res['error'] += str(item['errorCode'])+','
        return res

    # get user random
    def getRandomUser(self):
        conn = pool.connection()
        cur = conn.cursor()
        cur.execute(random_user_sql)
        user_id = cur.fetchone()
        cur.close()
        conn.commit()
        conn.close()
        return user_id[0]


    # start upload
    def iter_path(self,path):
        all = os.listdir(path)
        for x in all:
            temp_path = img_base_path + x
            ri = x.rindex('.')
            # name of image
            img_name = x[0:ri]
            if self.check_exist_byId(img_name) == 0:
                continue
            else:
                # upload img
                round_ip = self.round_node_ip()
                temp_user_id = self.getRandomUser()
                param = {'node_ip':round_ip,'img_path':temp_path,'user_id':temp_user_id,'shop_id':img_name,'source':10,'title':x,'type':1,'duplicate':1}
                res = self.upload_img(param)
                # user_id,shop_id,image_name,image_id,ok,http_code,batch,md5,ip_node,source,update_time,create_time
                # today = datetime.date.today()
                # today = today.strftime("%Y%m%d")
                batch = 1
                temp_ist_sql = add_log_sql % (temp_user_id,img_name,x,res['img_id'],res['status'],res['error'],res['http_code'],batch,'',round_ip,10)
                self.saveLog(temp_ist_sql)
                time.sleep(1.5)

if __name__ == "__main__":
    p = 0
    util = uploadUtil()
    # with open('userids','w') as u:
    #     for i in range(100000):
    #         u.write(str(util.getRandomUser())+"\n")
    util.iter_path(img_base_path)
    # for i in range(10):
    #     util.round_node_ip()