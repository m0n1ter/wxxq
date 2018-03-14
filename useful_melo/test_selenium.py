# !/usr/bin/python
# -*- coding: utf-8 -*-
from time import sleep
from selenium import webdriver
# 进入浏览器设置
options = webdriver.ChromeOptions()

options.add_argument('--headless')
cons_txt=open('consId.txt','a')
# 设置中文
options.add_argument('lang=zh_CN.UTF-8')
# 更换头部
options.add_argument('user-agent="Mozilla/5.0(WindowsNT6.1;rv:2.0.1)Gecko/20100101Firefox/4.0.1"')
i=0
need_restart = True
browser = None
while i<100000:
    i+=1
    if need_restart:
        browser = webdriver.Chrome(chrome_options=options)
    #url = "file:///C:/Users/Administrator/Desktop/consId.html"
    url = "https://www.ly.com"
    browser.get(url)
    elem=browser.find_element_by_id("resText")
    while not elem.text:
        sleep(1)
        elem=browser.find_element_by_id("resText")
    if  elem.text =="error":
        need_restart = False
        #continue
    else:
        need_restart = True
        cons_txt.write(elem.text+'\n')
        cons_txt.flush()
        browser.quit()

