# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import scipy as sp  
import numpy as np  
from sklearn.datasets import load_files  
from sklearn.cross_validation import train_test_split  
from sklearn.feature_extraction.text import  TfidfVectorizer  
import jieba
  
# 加载数据集，切分数据集70%训练，30%测试
movie_reviews = load_files('E:/study/study/Crawler/File/charpter_13/txt_sentoken')
doc_terms_train, doc_terms_test, y_train, y_test = train_test_split(movie_reviews.data, movie_reviews.target, test_size = 0.3)

f = open('E:/study/study/Crawler/File/charpter_13/stopwords.txt', 'rb')
stop_words_raw = f.read().decode("utf-8")
f.close()

stop_words = stop_words_raw.splitlines()

# BOOL型特征下的向量空间模型
count_vec = TfidfVectorizer(binary = False, decode_error = 'ignore', tokenizer=jieba.cut, stop_words=stop_words)
x_train = count_vec.fit_transform(doc_terms_train)
x_test  = count_vec.transform(doc_terms_test)
x       = count_vec.transform(movie_reviews.data)  
# y       = movie_reviews.target
# print doc_terms_train
for keyword in count_vec.get_feature_names():
    print   keyword
weight = x.toarray()
keywords = count_vec.get_feature_names()
for i in range(0,len(weight)):
    tmp_store={}
    for j in range(0,len(keywords)):
        tmp_store[keywords[j]] = weight[i][j]
    keyword_rank_dict=sorted(tmp_store.items(),key=lambda d:d[1], reverse=True  )
    i = 0
    result = []
    for item in keyword_rank_dict:
        i += 1
        if item[1]==0.0:
            continue
        if i > 5:
            break
        result.append(item[0])
        print '%s %s'%(item[0].encode("utf8"),item[1])
    print '-------'
# print x.toarray()
