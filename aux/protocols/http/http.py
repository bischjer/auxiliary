from aux.protocols.connection import TCPConnection
from urlparse import urlparse, urlunparse

HTTP_DEFAULT_PORT = 80
TCP_FRAME_BUFFER_SIZE = 1500#bytes

class HTTPProtocol(object):
    __is_persistent = False
    __transport_frame_size = TCP_FRAME_BUFFER_SIZE

    def __init__(self, raw_url):
        self.url = self.set_url_from_string(raw_url)
        self._transport = TCPConnection(self.url.hostname, self.url.port) #TODO: factory with persist scheme
        self._transport.connect()

    def is_persistent(self):
        return self.__is_persistent

    def set_url_from_string(self, raw_url):
        url = urlparse(raw_url)
        if not url.port:
            l = list(url)
            l[1] = l[1] + ":%i" % HTTP_DEFAULT_PORT
            url = urlparse(urlunparse(l))        
        return url

    
    def receive_response(self, response):
        #rx--
        pass
    
    
    def send_request(self, request):
        request.target = self.url.hostname

        #size of transfer
        print request.headers
        #tx--
        self._transport.send(str(request))


        #this needs to wait for response
        #1 blocking
        #2 thread
        #3 async
        
        return "hello"



    
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


