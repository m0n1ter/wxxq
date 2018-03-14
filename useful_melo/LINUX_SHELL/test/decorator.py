def decorator(func):
    def wrapper():
        print func.__name__
        return func()
    return wrapper

@decorator
def test():
    print "ddddd"



test()


