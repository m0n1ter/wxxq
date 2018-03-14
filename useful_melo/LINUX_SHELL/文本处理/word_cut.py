#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import jieba
import jieba.analyse
import re
def sort_by_value(d):
    items=d.items()
    backitems=[[v[1],v[0]] for v in items]
    backitems.sort(lambda a,b :-cmp(a[0],b[0]))
    return [ (backitems[i][0],backitems[i][1]) for i in range(0,len(backitems))]

def extract():
    text = open('E:/ZBSource/zhaobiao17/clean/421351.txt').read()
    # r = '[’!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~]+'
    # text=re.sub(r,'',text)
    words = list(jieba.cut(text, cut_all=False))
    stopwords = [word.strip() for word in open('stopwords.txt')]

    # result = set(words)
    caculator = {}
    #print ",".join(result)
    #print ','.join(words)
    for w in words:
        if w in stopwords:
            continue
        if w in caculator:
            caculator[w]+=1
        else:
            caculator[w]=1

    k_v=sort_by_value(caculator)
    for item in k_v:
        print item[1],item[0]


def extract_use_stopwords():
    jieba.analyse.set_stop_words('stopwords.txt')
    text = open('E:/ZBSource/zhaobiao17/clean/421351.txt').read()
    tags = jieba.analyse.extract_tags(text,10)
    return tags
if __name__ == '__main__':

    for word in extract_use_stopwords():
        print  word
    # extract()