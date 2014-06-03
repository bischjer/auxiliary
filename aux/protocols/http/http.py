from aux.protocols.transport import TCPTransport, TCP_DEFAULT_FRAME_SIZE
from urlparse import urlparse, urlunparse

CRLF = "\r\n"
HTTP_DEFAULT_PORT = 80
HTTPS_DEFAULT_PORT = 443
TCP_FRAME_BUFFER_SIZE = 1500#bytes#hmmmm
#TODO: enum wrapper
HTTP_METHODS = ["OPTIONS", "GET","HEAD", "POST", "PUT", "DELETE", "TRACE", "CONNECT"]#extension-method
GET  = 'GET'
POST = 'POST'
PUT  = 'PUT'

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

"""
HTTP

Authentication Type: On Request; Preemptive; SPNEGO/Kerberos; NTLM1|2

"""

class HTTPMessage(object):
    http_version = 1.1
    target = None
    headers = dict()
    body = None

    def __init__(self, headers, body):
        self.headers = headers
        self.body = body
        
    def __str__(self):
        return CRLF.join([CRLF.join([": ".join(item) for item in self.headers.items()]),
                          "",#zero-length-http-message-line
                          self.body])

class HTTPRequest(HTTPMessage):
    url = None
    def __init__(self, url, request_data={}):
        self.method = request_data.get('method', 'GET').upper()
        self.url = urlparse(url)
        if len(self.url.path) == 0:
            l = list(self.url)
            l[2] = l[2] + "/"
            self.url = urlparse(urlunparse(l))
        super(HTTPRequest, self).__init__(request_data.get('headers', {}),
                                          request_data.get('body', ''))

    def __str__(self):
        return CRLF.join(["%s %s HTTP%0.1f" % (self.method, self.url.path, self.http_version),
                          super(HTTPRequest, self).__str__()])

    
class HTTPResponse(HTTPMessage):
    def __init__(self, status, response_data={}):
        self.status = status
        super(HTTPResponse, self).__init__(response_data.get('headers', {}),
                                           response_data.get('body', ''))

    def __str__(self):
        return CRLF.join(["HTTP/%0.1f %s %s" % (self.http_version, self.status, HTTP_RESPONSE_CODES[str(self.status)]),
                          super(HTTPResponse, self).__str__()])
    


class HTTP(object):
    __is_persistent = False
    __transport_frame_size = TCP_DEFAULT_FRAME_SIZE

    def __init__(self):
        self._transport = None
   
    def get_transport(self, url, persist=False):
        # if self._transport != None and persist:
        #     return self._transport
        transport = TCPTransport(url.hostname, url.port)
        transport.connect()
        return transport
    
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
        request.target = request.url.hostname
        print "request to url", request.url.geturl()
        print request

        #TODO: decide size for transfer
        # content-length is only for post and response
        #content-length | Transfer-encoding "chunked" | multipart/byteranges (rare/special) | server closes connection
        print 'has content-length', request.headers.get('Content-length', None)
        self._transport = self.get_transport(request.url)
        self._transport.send(str(request))
        raw_response = self._transport.recv()
        

        # print request.headers
        #tx--
        
        # self._transport.send(str(request))


        #this needs to wait for response
        #1 blocking
        #2 thread
        #3 async
        
        return raw_response


class SimpleHTTPClient(object):
    def get(self, url):
        HTTPRequest(url,
                    {'method':'GET',
                     'headers':{},
                     'body':''})
        # print url

    def post(self, url, headers={}):
        pass
        # print url

    def put(self, url):
        pass
        # print url

    
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


