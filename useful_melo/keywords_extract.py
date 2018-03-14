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
import re
# 加载数据集，切分数据集70%训练，30%测试
movie_reviews = load_files('E:/ZBSource/zhaobiao17-part2')
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
files_list=movie_reviews.filenames
file_id_list = []
get_id_regex = re.compile('.*(\d+)\.txt')
for file_path in files_list:
    file_id=re.search('[^0-9]*(\d+)\.txt',file_path).group(1)
    file_id_list.append(file_id)
# for keyword in count_vec.get_feature_names():
#     print   keyword
weight = x.toarray()
keywords = count_vec.get_feature_names()
key_words_file = open('key_words_file.txt','w')
for i in range(0,len(weight)):
    tmp_store={}
    for j in range(0,len(keywords)):
        tmp_store[keywords[j]] = weight[i][j]
    keyword_rank_dict=sorted(tmp_store.items(),key=lambda d:d[1], reverse=True  )
    tik = 0
    result = ''
    tmp_file_id = str(file_id_list[i])
    result+=tmp_file_id + '`'
    for item in keyword_rank_dict:
        tik += 1
        if item[1]==0.0 or not item[0].strip():
            continue
        if tik > 20:
            break
        result += item[0].encode("utf-8")+"  "
    result += '\n'
    key_words_file.write(result)
key_words_file.close()