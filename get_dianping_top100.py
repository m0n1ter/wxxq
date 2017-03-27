#-*- coding: utf-8 -*-
# import mycurl
import time
import json
import urllib
import codecs
import re
import sys
from city_xp_dic import city_code_dict, city_telno_code, city_list, city_province_dic
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
channel_dict = {
    10: "餐饮",
    15: "KTV",
    25: "电影",
    45: "健身",
    60: "酒店",
}
'''
10：餐饮
15：KTV
25：电影
45：健身:
60：酒店

http://www.dianping.com/shoplist/search/5_60_0_score
http://www.dianping.com/shoplist/search/{市ID}_{类型ID}_0_score

南京市,5,1
无锡市,13,2
徐州市,92,3
常州市,93,4
苏州市,6,5
南通市,94,6
连云港市,95,7
淮安市,96,8
盐城市,97,9
扬州市,12,10
镇江市,98,11
泰州市,99,12
宿迁市,100,13
'''
top100_url_template = "http://www.dianping.com/mylist/ajax/shoprank?cityId=%s&shopType=%s&rankType=score&categoryId=0"
data_path = "E:/dianping/%s_%s.json"
csv_path = "E:/DianPingCSV/%s_%s.csv"
total_shop100_csv = "E:/total.csv"


class Dianping:
    def __niit__(self):
        pass

    def get_top100_data(self, city_list, channel_list):
        for city_id in city_list:
            for channel_id in channel_list :
                
                top100_url = top100_url_template % (city_id, channel_id)
                response = codecs.open(top100_url, 'r', 'utf-8')
                content = response.read()
                response.close()
                file_name = data_path % (city_id, channel_id)
                with open(file_name, "w") as f:
                    f.write(content)
                time.sleep(20)
          
    def get_top100_data2(self, cid, channel_list):
            for channel_id in channel_list :
                top100_url = top100_url_template % (cid, channel_id)
                response = urllib.urlopen(top100_url)
                content = response.read()
                response.close()
                file_name = data_path % (cid, channel_id)
                with open(file_name, "w") as f:
                    f.write(content)
                time.sleep(20)
            
    def parse_top100_page(self,city_list, channel_list):
        total = 0
        with open(total_shop100_csv, "w") as f1:
            for city_id in city_list:
                for channel_id in channel_list :
                    file_name = data_path % (city_id, channel_id)
                    file_csv_name = csv_path % (city_id, channel_id)
                    with open(file_name, "r") as f:
                        page_content = f.read().decode("utf-8")
                        top100_dict = json.loads(page_content)
                        top100_list = top100_dict["shopBeans"]
                        if not top100_list:
                            # print 'valid json file path :',file_name
                            continue
                        click = 0
                        for top100 in top100_list :
                                total += 1
                                click += 1
                                shop_id = top100["shopId"]
                                name = top100["fullName"]
                                if ',' in name:
                                    name = name.replace(',', '，')
                                    print file_csv_name,click,name
                                address = top100["fullAdress"]
                                if ',' in address:
                                    address = address.replace(',', '，')
                                    print file_csv_name,click,address
                                tel1 = self.add_region_code(city_id, top100["phoneNo"])
                                tel2 = self.add_region_code(city_id, top100["phoneNo2"])
                                telno = ("%s %s" % (tel1, tel2)).strip()
                                if ',' in telno:
                                    telno = telno.replace(',', '，')
                                    print file_csv_name,click,telno
                                item = "%d`%s`%s`%s`19`%d`%s`%s" % (shop_id, name, address, telno,city_code_dict[city_id], channel_dict[channel_id],city_province_dic[city_id])
                                # print item
                                f1.write(item+'\n')
                                # if click != 100:
                                #     print file_csv_name,click
            print total



                        #print "%d,%s" % (shop_id, channel_dict[channel_id])

    @classmethod
    def add_region_code(self, city_id, telno):
        if not telno :
            return ""
        if len(str(telno)) == 10 and str(telno)[:3] == "400":
            return str(telno)
        if len(str(telno)) >= 11:
            return str(telno)
        else:
            return "%s-%s" % (city_telno_code[city_id], str(telno))


def deal(s):
    c = r'[0-9]+'
    a = re.compile(c)
    r = re.findall(a,s)
    return r[0]
if __name__ == "__main__":
    #city_list = [5,13,92,93,6,94,95,96,97,12,98,99,100]
    # conn = MySQLdb.connect(host='172.16.24.151', port=3306, user='root', passwd='',db='dianping')
    # cur = conn.cursor()
    # city_ids = cur.fetchall("select dp_city_id from dianping_area")
    # for id in city_ids:
    #     print id
    channel_list = [10, 15, 25, 45, 60]
    dp = Dianping()
    # city = open('city.txt','r')
    # city_list = [17,177,252]
    # while 1:
    #     line = city.readline()
    #     if not line:
    #         break
    #     cid = deal(line)
    #     city_list.append(int(cid))
    #dp.get_top100_data(city_list, channel_list)
    dp.parse_top100_page(city_list, channel_list)
    
    
    