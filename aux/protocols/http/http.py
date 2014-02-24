from aux.protocols.connection import TCPConnection
from urlparse import urlparse, urlunparse

class HTTPConnection(object):

    __is_persistent = False

    def __init__(self, url_path):
        
        url = urlparse(url_path)
        if not url.port:
            l = list(url)
            l[1] = l[1] + ":80"
            url = urlparse(urlunparse(l))
        print url_path, url
        self.__conn = TCPConnection(url)
        self.__conn.connect()
        # self.port = self.url_path.netloc.split(':')[1]
        # print self.url_path, self.port
    
    def is_persistent(self):
        return self.__is_persistent
        

    def send_request(self, request):
        self.__conn.send(request)
        return self.__conn.recv()


