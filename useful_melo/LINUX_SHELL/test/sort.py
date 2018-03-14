a = [2,555,23,25,34444]
print sorted(a,key=lambda d:str(d))




d = {'A':1,'F':3,'G':12}



da = ("2323",33,)
print hash(da)
dd = ("2323",33,)
print hash(dd)
print da==dd

import array
s = "mmm"
aaa = array.array('c', s)
aaa2 = array.array('c', s)
print aaa==aaa2


class per:
    def __init__(self):
        pass

c1 = per()
c2 = per()
print c1==c2
