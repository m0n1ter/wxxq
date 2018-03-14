import cPickle as pickle
data = (12,"chemye",4.34)
pickle.dump(data,open("test.pkl","w"))

data=pickle.load(open("test.pkl"))
print data[0] 
