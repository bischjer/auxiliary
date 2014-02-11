from aux.protocols.connection import TLS_TCPConnection
from urlparse import urlparse


class HTTPSConnection(object):

    __is_persistent = False

    def __init__(self, url, port):
        self.url_path = urlparse(url)
        self.port = port
        self.__conn = TLS_TCPConnection(url, port)
        self.__conn.connect()
        # self.port = self.url_path.netloc.split(':')[1]
        # print self.url_path, self.port
    
    def is_persistent(self):
        return self.__is_persistent
        

    def send_request(self, request):
        self.__conn.send(request)
        return self.__conn.recv()
