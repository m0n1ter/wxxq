import struct
c = (12,"chemye",4.34)
s = struct.Struct("I6sf")
data=s.pack(*c)
unpacked_data = s.unpack(data)

print c
print data
print unpacked_data
