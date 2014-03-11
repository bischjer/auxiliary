from aux.protocols.connection import TCPConnection
from urlparse import urlparse, urlunparse

class HTTPConnection(object):

    __is_persistent = False

    def __init__(self, url_path):
        self.url = urlparse(url_path)
        if not self.url.port:
            l = list(self.url)
            l[1] = l[1] + ":80"
            self.url = urlparse(urlunparse(l))
        self.__conn = TCPConnection(self.url.hostname, self.url.port)
        self.__conn.connect()
    
    def is_persistent(self):
        return self.__is_persistent

    def send_request(self, request):
        request.target = self.url.hostname
        self.__conn.send(str(request))
        return self.__conn.recv()


