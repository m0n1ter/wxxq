class A:
    cate_map = []
    def __init__(self):
        self.cate_map.append(1212)

if __name__ == "__main__":
    a=A()
    b=A()
    b.cate_map.append("testtest")
    print a.cate_map
