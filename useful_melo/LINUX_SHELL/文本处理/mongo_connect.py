# -*- coding:utf-8 -*-

from pymongo import MongoClient

#建立MongoDB数据库连接
client = MongoClient('172.16.24.205',27017)

#连接所需数据库,test为数据库名
db=client.PublicHealth

#连接所用集合，也就是我们通常所说的表，test为表名
collection=db.hypertension_fu

#接下里就可以用collection来完成对数据库表的一些操作

#查找集合中所有数据
for item in collection.find():
    print item
