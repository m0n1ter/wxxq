# -*- coding: utf-8 -*-

import csv
import string
from PIL import Image
import pytesseract
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)

def ocr(img):
    # 获取图片的像素数组
    pixdata = img.load()
    colors = {}
    # 统计字符颜色像素情况
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if colors.has_key(pixdata[x,y]):
                colors[pixdata[x, y]] += 1
            else:
                colors[pixdata[x,y]] = 1

    # 排名第一的是背景色，第二的是主要颜色
    colors = sorted(colors.items(), key=lambda d:d[1], reverse=True)
    color_map = {}
    for i,co in enumerate(colors):
        if i%2:
            color_map[co[0]]=1
        else:
            color_map[co[0]]=0

    significant = colors[0][0]
    for y in range(img.size[1]):
        for x in range(img.size[0]):
            if color_map[pixdata[x,y]]:
                pixdata[x,y] = (255,255,255)
            else:
                pixdata[x,y] = (0,0,0)
    img.save('bw.jpg')
    # threshold the image to ignore background and keep text
    # gray = img.convert('L')
    # bw = gray.point(lambda x: 0 if x < 1 else 255, '1')
    # bw.save('captcha_gray.png')

files = ('test.jpg',)

def test_samples():
    for file in files:
        img = Image.open(file)
        print '%s is recognized as %s' %(file,ocr(img))

test_samples()
