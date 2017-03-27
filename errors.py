import os
class HostResolvedError(Exception):
    def __init__(self,msg):
        self.msg = msg
        pass


class TimeoutError(Exception):
    def __init__(self,msg):
        self.msg = msg
        pass


# raise TimeoutError('reere')
# raise HostResolvedError('reere')

all = os.listdir('D:/Py_workspacce/trains/xc-not-exist')
for i in all:
    print i