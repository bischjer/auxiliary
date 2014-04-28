from aux.protocols.connection import Connection
from aux.protocols.http.http import HTTPConnection 
from aux.protocols.http.https import HTTPSConnection
import re


"""
HTTP

Authentication Type: On Request; Preemptive; SPNEGO/Kerberos; NTLM1|2

"""

class HTTPRequest(object):
    def __init__(self, request_data, path=""):
        self.target = None
        self.method = request_data.get('method', 'Get').upper()
        self.headers = request_data.get('headers', {})
        self.body = request_data.get('body', '')
        self.path = path

    def __str__(self):
        self.headers['Content-Length'] = str(len(self.body))
        return "%s %s HTTP/1.1\n%s\n\n%s" % (self.method,
                                              self.path,
                                              "\n".join([": ".join(item) for item in self.headers.items()]),
                                              self.body)


class HTTPResponse(object):
    re_HTTP_SIGN = re.compile(r'HTTP\/(\d\.\d)\s(\d{3})\s')
    
    def __init__(self, raw_response):
        self.raw_response = raw_response
        self.headers = ""
        self.body = ""
        self.version = None
        self.code = None
        self.parse_raw_response()
        
    def parse_raw_response(self):
        body_flag = False
        self.version, self.code = self.re_HTTP_SIGN.findall(self.raw_response.split("\n")[0])[0]
        for line in self.raw_response.split("\n")[1:]:
            if len(line) == 0:
                body_flag = True
            if body_flag:
                self.body = self.body+"\n"+line
            else:
                self.headers = self.headers+"\n"+line

        self.body = self.body.strip()
                
        # print self.version, self.code
        # print self.headers
        # print self.body



