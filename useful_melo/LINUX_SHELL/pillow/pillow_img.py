#-*- coding:utf-8 -*-
from __future__ import print_function	
from PIL import Image
import os
import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)
#im = Image.open(base)
#print(im.format, im.size, im.mode)
