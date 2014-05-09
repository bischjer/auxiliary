from aux.protocols.connection import Connection
from aux.protocols.http.http import (HTTPProtocol, CRLF, HTTP_RESPONSE_CODES)
from aux.protocols.http.https import HTTPSConnection
import re
from urlparse import urlparse, urlunparse

GET  = 'GET'
POST = 'POST'
PUT  = 'PUT'

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
    def __init__(self, status, response_data):
        self.status = status
        super(HTTPResponse, self).__init__(response_data.get('headers', {}),
                                           response_data.get('body', ''))

    def __str__(self):
        return CRLF.join(["HTTP/%0.1f %s %s" % (self.http_version, self.status, HTTP_RESPONSE_CODES[str(self.status)]),
                          super(HTTPResponse, self).__str__()])
    
    
# class HTTPResponse(HTTPMessage):
#     re_HTTP_SIGN = re.compile(r'HTTP\/(\d\.\d)\s(\d{3})\s')
    
#     def __init__(self, raw_response):
#         self.raw_response = raw_response
#         self.headers = ""
#         self.body = ""
#         self.version = None
#         self.code = None
#         self.parse_raw_response()
        
#     def parse_raw_response(self):
#         body_flag = False
#         self.version, self.code = self.re_HTTP_SIGN.findall(self.raw_response.split("\n")[0])[0]
#         for line in self.raw_response.split("\n")[1:]:
#             if len(line) == 0:
#                 body_flag = True
#             if body_flag:
#                 self.body = self.body+"\n"+line
#             else:
#                 self.headers = self.headers+"\n"+line

#         self.body = self.body.strip()
                

