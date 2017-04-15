# -*- coding:utf-8  -*-
import MySQLdb
from DBUtils.PooledDB import PooledDB
# 5为连接池里的最少连接数

class sqlSessionFactory(object):
    pool = None

    def __init__(self,host,user,password,db,num =5):
        self.host = host
        self.user = user
        self.passwd = password
        self.db = db
        self.num = num
        self.__initPool__()

    def __initPool__(self):
        global pool
        pool = PooledDB(MySQLdb,self.num,host=self.host,user=self.user,passwd=self.passwd,db=self.db,port=3306,charset="utf8")
        # pool = PooledDB(MySQLdb,5,host='192.100.2.31',user='data',passwd='opensesame',db='traincrawler',port=3306)

    @classmethod
    def execute(self,sql):
        conn = pool.connection()
        cur = conn.cursor()
        cur.execute(sql)
        cur.close()
        conn.commit()
        conn.close()

    @classmethod
    def select(self,sql):
        conn = pool.connection()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()
        return result

if __name__ == '__main__':
    print 'start init '
    sqlSessionFactory('192.100.2.31','data','opensesame','traincrawler',10)