from aux.protocols.connection import TCPConnection
from urlparse import urlparse, urlunparse

CRLF = "\r\n"

HTTP_DEFAULT_PORT = 80
HTTPS_DEFAULT_PORT = 443
TCP_FRAME_BUFFER_SIZE = 1500#bytes#hmmmm

HTTP_METHODS = ["OPTIONS", "GET","HEAD", "POST", "PUT", "DELETE", "TRACE", "CONNECT"]#extension-method
HTTP_RESPONSE_CODES = {"100": "Continue",
                       "101": "Switching Protocols",
                       "200": "OK",
                       "201": "Created",
                       "202": "Accepted",
                       "203": "Non-Authoritative Information",
                       "204": "No Content",
                       "205": "Reset Content",
                       "206": "Partial Content",
                       "300": "Multiple Choices",
                       "301": "Moved Permanently",
                       "302": "Found",
                       "303": "See Other",
                       "304": "Not Modified",
                       "305": "Use Proxy",
                       "307": "Temporary Redirect",
                       "400": "Bad Request",
                       "401": "UnauthorizedRequest",
                       "402": "Payment Required",
                       "403": "Forbidden",
                       "404": "Not Found",
                       "405": "Method Not Allowed",
                       "406": "Not Acceptable",
                       "407": "Proxy Authentication Required",
                       "408": "Request Time-out",
                       "409": "Conflict",
                       "410": "Gone",
                       "411": "Length Required",
                       "412": "Precondition Failed",
                       "413": "Request Entity Too Large",
                       "414": "Request-URI Too Large",
                       "415": "Unsupported Media Type",
                       "416": "Requested range not satisfiable",
                       "417": "Expectation Failed",
                       "500": "Internal Server Error",
                       "501": "Not Implemented",
                       "502": "Bad Gateway",
                       "503": "Service Unavailable",
                       "504": "Gateway Time-out",
                       "505": "HTTP Version not supported"}


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

    
    def receive(self, response):
        #rx--
        pass
    
    
    def send(self, request):
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


class SimpleHTTPClient(object):
    def get(self, url):
        HTTPRequest({'method':'GET',
                     'headers':{},
                     'body':''})
        print url

    def post(self, url, headers={}):
        print url

    def put(self, url):
        print url

    
# class HTTPConnection(object):

#     __is_persistent = False

#     def __init__(self, url_path):
#         self.url = urlparse(url_path)
#         if not self.url.port:
#             l = list(self.url)
#             l[1] = l[1] + ":80"
#             self.url = urlparse(urlunparse(l))
#         self.__conn = TCPConnection(self.url.hostname, self.url.port)
#         self.__conn.connect()
    
#     def is_persistent(self):
#         return self.__is_persistent

#     def send_request(self, request):
#         request.target = self.url.hostname
#         self.__conn.send(str(request))
#         return self.__conn.recv()


