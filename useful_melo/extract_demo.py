# -*- coding: utf-8 -*-

import re

from lxml import etree
from lxml.html import clean
import pylab
import sys
import os

# req = urllib2.Request('http://www.mafengwo.cn/i/750387.html')
# req = urllib2.Request('http://news.sina.com.cn/china/xlxw/2017-03-12/doc-ifychhuq4136971.shtml')
# req = urllib2.Request('http://bbs.qyer.com/thread-2703424-1.html')

# response = urllib2.urlopen(req)
# content = response.read()
#
# f = open('sina_ifych.html', 'wb+')
# f.write(content)
# f.close()
def demo():
    content=open('locoso323928.html').read()
    #
    # tr = etree.HTML(content)
    #
    # for bad in tr.xpath("//script"):
    #     bad.getparent().remove(bad)
    #
    # for bad in tr.xpath("//style"):
    #     bad.getparent().remove(bad)

    cleaner = clean.Cleaner(style=True, scripts=True, comments=True, javascript=True, page_structure=False, safe_attrs_only=False)
    content = cleaner.clean_html(content.decode('utf-8')).encode('utf-8')

    content=content.replace('<p>','\n<p>')
    content=content.replace('<tr>','\n<tr>')
    content=content.replace('<div>','\n<div>')
    content=content.replace('<span>','\n<span>')
    content=content.replace('<td>','<td>  ')
    reg = re.compile("<[^>]*>")
    content = reg.sub('', content)

    f = open('cleaned.txt', 'wb+')
    counts = []
    lines = content.split('\n')
    count=0
    for line in lines:
        line = line.strip()
        if len(line)!=0:
            count+=1
            counts.append(len(line))
            f.write(line+'\n')
    f.close()
    indexes = range(0, count)

    pylab.plot(indexes, counts,linewidth=1.0)
    pylab.savefig('word_count.png')
    pylab.show()

def cleaner(file_name):
    content=open('E:/ZBSource/zhaobiao16/%s'%file_name).read()
    article_id=re.search('(\d+)\.html',file_name).group(1)

    cleaner = clean.Cleaner(style=True, scripts=True, comments=True, javascript=True, page_structure=False, safe_attrs_only=False)
    content = cleaner.clean_html(content.decode('utf-8')).encode('utf-8')

    content=content.replace('<p>','\n<p>')
    content=content.replace('<tr>','\n<tr>')
    content=content.replace('<div>','\n<div>')
    content=content.replace('<span>','\n<span>')
    content=content.replace('<td>','<td>  ')
    reg = re.compile("<[^>]*>")
    content = reg.sub('', content)
    f = open('E:/ZBSource/zhaobiao16/clean/%s.txt'%article_id, 'wb+')
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if len(line)!=0:
            f.write(line+'\n')
    f.close()

if __name__ == '__main__':
    files=os.listdir('E:/ZBSource/zhaobiao16/')
    for file in files:
        try:
            if file.index('.html')>-1:
                cleaner(file)
        except Exception as e:
            pass
