import codecs
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from settings import new_shop_list, shop_list
# shop_list = [13069819]
# new_shop_list = [72446539]
path_old = 'E:/DPShops1/%s.html'
path_new = 'E:/DPShops2/%s.html'
added_old = []
added_new = []
#parse old html
with open('400.csv','w') as total:
    for sid in shop_list:
        p_old = path_old % sid
        html_old = codecs.open(p_old, 'r', 'utf-8')
        content = html_old.read()
        html_old.close()
        tree = etree.HTML(content)
        nodes_name = tree.xpath("descendant::h1[@class='shop-name']")
        shop_name = ''
        count = 0
        if len(nodes_name)>0:
            shop_name = str(nodes_name[0].text).strip()
        else:
            count += 1
        nodes_address = tree.xpath("descendant::span[@itemprop='street-address']")
        shop_address = ''
        if len(nodes_address)>0:
            shop_address = str(nodes_address[0].text).strip()
        else:
            count += 1
        nodes_tel = tree.xpath("descendant::span[@itemprop='tel']")
        shop_tel = ''
        if(len(nodes_tel) >0):
            for one in nodes_tel:
                shop_tel += str(one.text).strip() + ' '
        else:
            count += 1
        if count == 3:
            added_old.append(sid)
            print added_old
        shop_item = "%s`%s`%s`%s" % (sid,shop_name,shop_address,shop_tel)
        total.write(shop_item+"\n")
    #parse new html
    for sid in new_shop_list:
        p_new = path_new % sid
        html_new = codecs.open(p_new, 'r', 'utf-8')
        content = html_new.read()
        html_new.close()
        tree_new = etree.HTML(content)
        nodes_name = tree_new.xpath("descendant::div[@class='hotel-detail-info']/div/h1")
        shop_name = ''
        if len(nodes_name)>0:
            shop_name = nodes_name[0].text
        nodes_address = tree_new.xpath("descendant::span[@class='hotel-address']")
        shop_address = nodes_address[0].text
        nodes_tel = tree_new.xpath("descendant::div[@class='info-value']")
        shop_tel = nodes_tel[0].text
        shop_item = "%s`%s`%s`%s" % (sid,shop_name,shop_address,shop_tel)
        total.write(shop_item+"\n")