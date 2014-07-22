from aux.protocol.transport import TCPTransport, TCP_DEFAULT_FRAME_SIZE, TLS_TCPTransport
from urlparse import urlparse, urlunparse
import logging
import aux
import auth
import re
import os


uname = os.uname()
USER_AGENT = "aux/%s (%s;)" % (aux.version(),
                              " ".join([uname[0], uname[-1]]))
CRLF = "\r\n"
HTTP_DEFAULT_PORT = 80
HTTPS_DEFAULT_PORT = 443
TCP_FRAME_BUFFER_SIZE = 1500#bytes#hmmmm
#TODO: enum wrapper
HTTP_METHODS = ["OPTIONS", "GET","HEAD", "POST", "PUT", "DELETE", "TRACE", "CONNECT"]#extension-method
M_GET  = 'GET'
M_POST = 'POST'
M_PUT  = 'PUT'
M_DELETE  = 'DELETE'
M_HEAD = 'HEAD'

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
RESPONSE_HEADER = [Accept-Ranges, Age, ETag, Location, Proxy-Authenticate, Retry-After, Server, Vary, WWW-Authenticate]

"""
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
        headers = {'Host': self.url.hostname,
                   'User-Agent': USER_AGENT}
        headers.update(request_data.get('headers', {}))
        super(HTTPRequest, self).__init__(headers,
                                          request_data.get('body', ''))

    def __str__(self):
        return CRLF.join(["%s %s HTTP/%0.1f" % (self.method, self.url.path, self.http_version),
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
    __transport_frame_size = TCP_DEFAULT_FRAME_SIZE #TODO: probably not usefull

    def __init__(self):
        self.logger = logging.getLogger('aux.protocol.http')
        self._transport = None
   
    def get_transport(self, url, scheme="http", persist=False, timeout=60):
        # if self._transport != None and persist:
        #     return self._transport
        #TODO: ternary default port assign is a bad idea as traceability is lost in request update url instead
        if "https" == scheme.lower():
            transport = TLS_TCPTransport(url.hostname,
                                         443 if url.port == None else int(url.port),
                                         timeout=timeout)
        else:
            transport = TCPTransport(url.hostname,
                                     80 if url.port == None else int(url.port),
                                     timeout=timeout)
        transport.connect()
        self.logger.debug('Connected to %s:%s' % (url.hostname, url.port))
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

    def default_transport_reader(self, transport, msg, content_length):
        raw_response = "\n".join(msg)
        in_buf = ""
        while 1:
            try:
                in_buf = transport.recv(2048)
            except Exception, e:
                print e.message
            if len(in_buf) < 1:
                break
            raw_response = raw_response + in_buf
        return raw_response

    def chunked_parser(self, raw_response):
        re_chunk = re.compile(r'^([a-f|\d]{1,4})\r')
        #TODO: fix this horrible impl.
        response = ""
        data = raw_response.split('\n')
        curr_line = ""
        # print "chunked_parser_entry"
        for next_line in data:
            is_next_a_chunk = re_chunk.findall(next_line)
            if len(is_next_a_chunk) > 0:
                next_chunk = int(is_next_a_chunk[0], 16)
                curr_line.rstrip()
            else:
                curr_line = next_line                
                response += curr_line

        return response
    
    def chunked_transport_reader(self, transport, msg):
        re_chunk = re.compile(r'^([a-f|\d]+){1,4}\r\n')
        raw_response = ""
        in_buf = "\n".join(msg)

        raw_response = raw_response + in_buf

        while 1:
            try:
                in_buf = transport.recv(TCP_DEFAULT_FRAME_SIZE)
            except Exception, e:
                print e.message
            fa = re_chunk.findall(in_buf)
            raw_response += in_buf                
            if len(fa) > 0:
                if fa[0] == '0':
                    raw_response += in_buf                
                    break;

        return self.chunked_parser(raw_response)

    def parse_message(self, transport, msg):
        #Parse all headers
        re_headline = re.compile(r'^(.*):\s(.*)\r')
        headers = dict()
        body = ""
        h_lines = msg.split("\n")
        line_counter = 0
        for line in h_lines[1:]:
            line_counter += 1
            if ":" in line:
                re_group = re_headline.match(line).groups()
                headers[re_group[0]] = re_group[1]
            else:
                break
        tail_msg = h_lines[line_counter+1:]
        if headers.get('Transfer-Encoding', None) == 'chunked':
            # print headers
            # print "chunked"
            body = self.chunked_transport_reader(transport, tail_msg)
        elif headers.get('Content-Length', None) != None:
            # print "cont length"
            if int(headers.get('Content-Length')) > 0:
                body = self.default_transport_reader(transport, tail_msg, headers.get('Content-Length'))
            else:
                body = ""
        else:
            # print "default"
            body = self.default_transport_reader(transport, tail_msg)
        return headers, body
    
    def parse_response(self, transport):
        #Validate start-line and remove it from buffer
        re_startline = re.compile(r'^HTTP\/\d\.\d\s(\d{3})\s')
        inbuf = transport.recv().split("\n")
        sl = inbuf[0]
        tail_msg = "\n".join(inbuf[1:]) 
        status = re_startline.match(sl).groups()[0]
        headers, body = self.parse_message(transport, tail_msg)
        # print headers, body
        return HTTPResponse(status, {'headers': headers, 'body': body})
    
    def receive(self, transport):
        response = self.parse_response(transport)
        transport.close()
        return response
    
    def send(self, request):
        request.target = request.url.hostname
        print 'request\n', request
        print ''
        #TODO: decide size for transfer
        # content-length is only for post and response
        #content-length | Transfer-encoding "chunked" | multipart/byteranges (rare/special) | server closes connection
        # print 'has content-length', request.headers.get('Content-length', None)
        if request.method == 'POST':
            request.headers.update({'Content-Length': '%i' % len(request.body)})
        transport = self.get_transport(request.url, scheme=request.url.scheme)
        transport.send(str(request))
        return self.receive(transport)

    
class HTTPClient(object):
    auth = auth
    
    def get(self, url=None, headers={}, body="", request=None):
        if request == None:
            request = HTTPRequest(url,
                                  {'method':'GET',
                                   'headers': headers,
                                   'body': body})
        _http = HTTP()
        return _http.send(request)
        

    def post(self, url, headers={}, body="", request=None):
        if request == None:
            request = HTTPRequest(url,
                                  {'method':'POST',
                                   'headers': headers,
                                   'body': body})
        _http = HTTP()
        return _http.send(request)
        
        
        

    def put(self, url):
        print url

        # print url

