import hashlib
import urlparse
def get_sign_and_sharding(str):
    md5 = hashlib.md5()
    md5.update(str)
    md5_digest = md5.hexdigest()
    print md5_digest[::2]
    sharding = md5_digest[0]
    return int(md5_digest[::2], 16), sharding

print get_sign_and_sharding("werwejwlkrfjwe")

