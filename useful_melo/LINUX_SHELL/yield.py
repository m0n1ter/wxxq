def get():
    for u in range(10):
        yield u

def test():
    a=100
    yield a
for i in get():
    print i
