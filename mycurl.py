# -*- coding: utf-8 -*-
from errors import HostResolvedError, TimeoutError
import StringIO
import pycurl
import re

version_header_regexp = re.compile(r'^(Last-Modified|ETag):\s*(.*)$', re.I)
content_type_regexp = re.compile(r'^Content-Type:\s*([^;]*)($)|(;)', re.I)
charset_header_regexp = re.compile(r'^Content-Type:.*charset=(.+)($)|(;)|(\s)', re.I)

class CurlResponse:

    def __init__(self, curl_instance, url, request_headers=[], proxy=None):
        curl_instance.setopt(pycurl.URL, url)
        self.headers = {} # Response Headers

        curl_instance.setopt(pycurl.HTTPHEADER, request_headers)

        # 跟302/301 redirect
        curl_instance.setopt(pycurl.FOLLOWLOCATION, 1)
        # 最多跟5次跳转
        curl_instance.setopt(pycurl.MAXREDIRS, 5)
        curl_instance.fp = StringIO.StringIO()
        curl_instance.setopt(curl_instance.WRITEFUNCTION, curl_instance.fp.write)
        curl_instance.setopt(curl_instance.HEADERFUNCTION, self.write_header)
        curl_instance.setopt(pycurl.SSL_VERIFYPEER, 0)
        curl_instance.setopt(pycurl.SSL_VERIFYHOST, 0)
        if proxy:
            ip, port = proxy.split(':', 1)
            curl_instance.setopt(pycurl.PROXY, str(ip))
            curl_instance.setopt(pycurl.PROXYPORT, int(port))
            curl_instance.setopt(pycurl.PROXYTYPE, pycurl.PROXYTYPE_HTTP)

        try:
            curl_instance.perform()
        except pycurl.error, e:
            # 47: Maximum (5) redirects followed
            # 56: Failure when receiving data from the peer
            if e[0] in (28, 47, 56):
                raise TimeoutError
            # 1: Protocol not supported or disabled in libcurl
            # 6: Can not resolve host
            # 7: No route to host
            elif e[0] in (1, 6, 7):
                raise HostResolvedError
            else:
                raise e

        self.body = curl_instance.fp.getvalue()
        self.status = curl_instance.getinfo(pycurl.HTTP_CODE)
        self.redirect_count = curl_instance.getinfo(pycurl.REDIRECT_COUNT)

        if self.redirect_count:
            self.effective_url = curl_instance.getinfo(pycurl.EFFECTIVE_URL)
        else:
            self.effective_url = None

    @property
    def current_version(self):
        if 'etag' in self.headers:
            return self.headers['etag']
        else:
            return self.headers.get('last-modified', None)

    def write_header(self, header):
        def match_header(name, pattern):
            match = pattern.match(header)
            if match:
                value = match.groups()[0]
                if value:
                    self.headers[name] = value.strip().lower()

        self.__match_version_header(header)
        match_header('content-type', content_type_regexp)
        match_header('charset', charset_header_regexp)
    
    def __match_version_header(self, header):
        match = version_header_regexp.match(header)
        if match:
            key, value = match.groups()
            self.headers[key.lower()] = value.strip()
    
    def __str__(self):
        return "Response[status=%s, redirect=%s]" % (self.status, self.redirect_count)


def get(url, timeout=15, request_headers=[], debug=False, proxy=None ):
    if type(url) == unicode:
        url = str(url)
    crl = pycurl.Curl()
    if debug:
        crl.setopt(pycurl.VERBOSE,1)
    crl.setopt(pycurl.TIMEOUT, timeout)
    
    response = CurlResponse(crl, url, request_headers, proxy)
    response.request_url = url
    return response

def get_from_link_job(link_job, timeout=15, request_headers=[], debug=False, proxy=None):
    if link_job.ip:
        request_headers.append('Host: %s' % link_job.domain)
    response = get(link_job.ip_based_url, timeout, request_headers, debug, proxy)
    response.request_url = link_job.url
    return response

def post(url, data, debug=False):
    crl = pycurl.Curl()
    if debug:
        crl.setopt(pycurl.VERBOSE,1)
    if type(data) == unicode:
        data = data.encode("utf8")
    crl.fp = StringIO.StringIO()
    crl.setopt(pycurl.POST, 1)
    crl.setopt(pycurl.POSTFIELDS, data)
#    post_data = StringIO.StringIO(data)
#    crl.setopt(crl.READFUNCTION, post_data.read)

    return CurlResponse(crl, url)



# if __name__ == "__main__":
#     response = get("http://www.cnblogs.com/UncleFreak/p/5720996.html",proxy='203.156.198.138:80')
#     print response.body,response.status