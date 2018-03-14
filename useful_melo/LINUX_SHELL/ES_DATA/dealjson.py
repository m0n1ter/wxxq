# -*- coding:utf-8 -*-
import yaml
import re
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import codecs
def f1():
    f=open('dp_shop_detail_xj.json')
    i = 0
    result = ''
    for line in f.readlines():
        line = line.strip()
        i+=1
        if i%11 == 0:
            result+="}\n"
        else:
            result+=line
    f.flush()
    f.close()
    w = open('shops.json','w')
    w.write(result)
    w.flush()
    w.close()

def load_as_yaml(s):
    invalid_rep = re.compile(':([^\s])')
    s = invalid_rep.sub(lambda m: ': %s' % m.groups()[0], s)
    # print s
    return yaml.load(s)

def f2(s):
    result=load_as_yaml(s)
    shop_dict = dict()
    shop_dict['shop_id']=result["shop_id"]
    # print result["shop_id"]
    shop_dict['shop_name']=str(result["shop_name"])
    shop_dict['tel']=result["tel"]
    shop_dict['category_name']=str(result["category_name"])
    shop_dict['address'] = str(result['address'])
    shop_dict['city_id']=result["city_id"]
    shop_dict['category_id']=result["category_id"]
    coordinates = dict()
    lat = result["x"]
    lon = result['y']
    if not result['x'] or result['x']=='null':
        lat=0
    if not result['y'] or result['y']=='null':
        lon=0
    coordinates['lat'] = float(lat)
    coordinates['lon'] = float(lon)
    shop_dict['coordinates'] = coordinates
    return json.dumps(shop_dict,ensure_ascii=False)

def main():
    ptn = '{"index":{"_id":"%s"}}'
    f=open('shops.json')
    i = 1
    result = ''
    w = codecs.open('shops-final.json','w','utf-8')
    for line in f.readlines():
        item=ptn % i
        w.write(item + "\n")
        line = line.strip()
        shop_item = f2(line)
        w.write(shop_item + "\n")
        i+=1
        print i
    f.flush()
    f.close()
    w.flush()
    w.close()

if __name__ == '__main__':
    # s='{"shop_id":76940697,"shop_name":"千花澍立体美容养生会所","address":"北京南路556号钻石百信花苑A单元1401","tel":"13579941119 0991-3852842","category_name":null,"x":null,"y":null,"city_id":325,"category_id":159}'
    # print f2(s)
    main()
    # a=u'千花澍立体美容养生会所'
    # print a.encode()