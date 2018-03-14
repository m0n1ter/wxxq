#-*- coding:utf-8 -*-

class test:

    def __init__(self):
        self.map = {}
        self.num = [1,2,3,4]
    def __getitem__(self, item):
        return self.map[item]

    def __setitem__(self, key, value):
        self.map[key] = value

    def __iter__(self):
        return iter(self.num)

    def next(self):
        pass
    def __abs__(self):

if __name__ == '__main__':
    a=test()
    a['name']='aa'
    a['age']=22
    a['height']=188
    for item in a:
        print item
