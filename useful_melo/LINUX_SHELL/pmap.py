#-*- coding:utf-8 -*-
import struct
import sys
import cPickle as pickle
message=123222321222
outobj = pickle.dumps(message, 2)
int_len = len(outobj)
print outobj
print int_len
structformat="Q"
len_str = struct.pack(structformat,int_len)
