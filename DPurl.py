import urllib
import re
import time
from shop_config import new_shop_list, shop_list
#http://www.dianping.com/newhotel/13084157
#http://www.dianping.com/shop/


def get(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html



p1_format = 'http://www.dianping.com/shop/'
p2_format = 'http://www.dianping.com/newhotel/'
u1 = open('url1.txt','r');
path_old = 'E:/DPShops1/%s.html'
path_new = 'E:/DPShops2/%s.html'
for line in shop_list:
    id = str(line).strip()
    url1 = p1_format+id
    content = get(url1)
    path1 = path_old % id
    print id
    with open(path1, "w") as f1:
        f1.write(content)
    time.sleep(10)

for line in new_shop_list:
    id = str(line).strip()
    url2 = p2_format+id
    content = get(url2)
    path2 = path_new % id
    print id
    with open(path2, "w") as f2:
        f2.write(content)
    time.sleep(10)
