# -*- coding: UTF-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import Queue
import json
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import traceback
import time
import MySQLdb
from DBUtils.PooledDB import PooledDB
import threading
import logging as log
from logging.handlers import RotatingFileHandler
from datetime import datetime
formatter = log.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
file_name = datetime.now().strftime('%Y-%m-%d')

def create_conf(backupCount,level):
    # price log configure
    root_logger = log.getLogger()
    if len(root_logger.handlers)==0:
        root_logger.setLevel(log.INFO)    # Log等级总开关
        category_path = '%s-log-%s.txt' % ('upload-img',file_name)
        category_handler = RotatingFileHandler(category_path, maxBytes=1024*1024*1024,backupCount=backupCount,mode='w')
        category_handler.setLevel(level)
        category_handler.setFormatter(formatter)
        root_logger.addHandler(category_handler)
        ch = log.StreamHandler()
        ch.setLevel(level)
        ch.setFormatter(formatter)
        root_logger.addHandler(ch)

# 5为连接池里的最少连接数
pool = PooledDB(MySQLdb,5,host='172.16.19.203',user='data',passwd='opensesame',db='img_upload',port=3306,charset='utf8')
register_openers()
node_ips = ['192.100.2.5','192.100.2.7','192.100.2.9']
base_upload_url = "http://%s:8180/chelsea/audit/update_image.action"
upt_status_sql = "update upload_log set ok=%s,error_msg='%s',selected=0,ip_node='%s' where id=%s"
get_task_sql = "select id,image_id from upload_log where ok=1 and selected=0 limit 5120"
lock_ip = threading.Lock()
current_ip_index = -1
total_task_queue = Queue.Queue()

class Task(object):
    def __init__(self,tid,shop_id):
        self.tid = tid
        self.shop_id = shop_id

# 审核工作线程
class checkWork(threading.Thread):

    def __init__(self,task_queue):
        threading.Thread.__init__(self)
        self.queue = task_queue
        self.start()
    def run(self):
        while True:
            try:
                task = self.queue.get()
                with lock_ip:
                    global current_ip_index
                    if current_ip_index == 2:
                        current_ip_index = 0
                    else:
                        current_ip_index +=1
                server_ip = node_ips[current_ip_index]
                tid = task.tid
                shop_id = task.shop_id
                result = check_img(server_ip,shop_id)
                execute(upt_status_sql %(result['ok'],deal_msg(result['err_msg']),server_ip,tid))
                time.sleep(1)
            except:
                t, v, tb = sys.exc_info()
                log.info("%s,%s,%s" % ( t, v, traceback.format_tb(tb)))


# 添加任务线程
class addTaskWork(threading.Thread):

    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.task_queue = queue
        self.start()

    def run(self):
        while True:
            size = self.task_queue.qsize()
            log.info('current task queue size:%s.'%size)
            if size<10240:
                data=execute(get_task_sql)
                for id,shop_id in data:
                    task_obj = Task(id,shop_id)
                    self.task_queue.put(task_obj)
                    execute("update upload_log set selected=1 where id=%s"%id)
            time.sleep(10)


def check_img(server_ip,shop_id):
        result = {}
        ok = -1
        err_msg = ''
        try:
            temp_upload_url = base_upload_url % (server_ip)
            datagen, headers = multipart_encode({"image_id":shop_id,"validate":1,"audit_desc":"通过"})
            request = urllib2.Request(temp_upload_url, datagen, headers)
            res_temp = urllib2.urlopen(request).read()
            response = json.loads(res_temp)
            if response['status']==1:
                ok=2
                err_msg = response['result']
            else:
                ok=3
                err_msg = response['result']
        except:
            t, v, tb = sys.exc_info()
            log.info("%s,%s,%s" % ( t, v, traceback.format_tb(tb)))
            ok = 4
            err_msg = '通信失败'
        result['ok']=ok
        result['err_msg']=err_msg
        return result


def execute(sql):
    conn = pool.connection()
    cur = conn.cursor()
    cur.execute(sql)
    data=cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()
    return data

def main():
    create_conf(10,log.INFO)
    addTaskWork(total_task_queue)
    for _ in range(0,3):
        checkWork(total_task_queue)

def deal_msg(msg):
    if len(msg)==0:
        return ''
    if isinstance(msg[0],dict):
        msg = json.dumps(msg[0])
    # msg.replace("'",'‘')
    # msg.replace('"','“')
    # msg.replace(',','，')
    return msg

def test():
    result= check_img('192.100.2.7','58c692ce539a012b5206a8b9')
    execute(upt_status_sql %(result['ok'],deal_msg(result['err_msg']),'192.100.2.7',29))

if __name__ == "__main__":
    main()