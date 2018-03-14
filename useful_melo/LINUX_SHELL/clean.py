# -*- coding:utf-8 -*-
from lxml.html import clean
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import re
file_name = "new.html"
file=open(file_name)
content=file.read()
#content = content.replace("</p>","\n")
cleaner = clean.Cleaner(style=True,scripts=True,comments=True,javascript=True,page_structure=False,safe_attrs_only=False)
content = cleaner.clean_html(content.decode('utf-8')).encode('utf-8')
reg = re.compile("<[^>]*>")
content = reg.sub("",content)
len_array = []
x_array = [i for i in range(len(content.split("\n")))]
for line in content.split("\n"):
    len_array.append(len(line))
    print line

import matplotlib.pyplot as plt

plt.plot(x_array,len_array)
plt.show()
