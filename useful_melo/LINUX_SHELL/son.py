from father import father
class son(father):
    def __init__(self):
	father.__init__(self)

    def print_name(self):
        print self.name
	print self.color

if __name__ == "__main__":
    son_ins = son()
    print son_ins.print_name()
