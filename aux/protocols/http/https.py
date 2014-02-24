from aux.protocols.connection import TLS_TCPConnection
from urlparse import urlparse, urlunparse


class HTTPSConnection(object):

    __is_persistent = False

    def __init__(self, https_url):
        url = urlparse(https_url)
        if not url.port:
            l = list(url)
            l[1] = l[1] + ":443"
            url = urlparse(urlunparse(l))
        self.__conn = TLS_TCPConnection(url)
        self.__conn.connect()
    
    def is_persistent(self):
        return self.__is_persistent

    
    def send_request(self, request):
        self.__conn.send(request)
        return self.__conn.recv()
