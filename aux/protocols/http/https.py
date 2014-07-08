from aux.protocols.connection import TLS_TCPConnection
from urlparse import urlparse, urlunparse


class HTTPSConnection(object):

    __is_persistent = False

    def __init__(self, https_url, timeout=60):
        self.url = urlparse(https_url)
        if not self.url.port:
            l = list(self.url)
            l[1] = l[1] + ":443"
            self.url = urlparse(urlunparse(l))
        self.__conn = TLS_TCPConnection(self.url.hostname, self.url.port, timeout=timeout)
        self.__conn.connect()
    
    def is_persistent(self):
        return self.__is_persistent
    
    def send_request(self, request):
        request.target = self.url.hostname
        self.__conn.send(str(request))
        return self.__conn.recv()
