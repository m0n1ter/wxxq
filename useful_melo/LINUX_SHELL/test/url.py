import urlparse
url = "http://weibo.com/melochey/home?topnav=1&wvr=5"
url_parse_result = urlparse.urlparse(url)
print url_parse_result
