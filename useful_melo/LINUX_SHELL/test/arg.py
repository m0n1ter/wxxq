import sys
print sys.argv[1]
print sys.argv[2]

import hashlib
a="adffdf"
print hashlib.md5(a)
print hashlib.md5(a)
print hashlib.md5(a).hexdigest()
