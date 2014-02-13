from socket import (AF_INET, SOCK_DGRAM, SOL_SOCKET,
                    SO_REUSEADDR, SHUT_RDWR)
from multiprocessing import Process
from ssl import wrap_socket
import ssl
import socket
import time

#TODO: This server needs to be written using aux itself, listening service.
#but this is not implemented yet.

http_response ='''\
HTTP/1.1 200 OK
Date: Sun, 18 Oct 2009 08:56:53 GMT
Server: AuxMockHTTPServer (Unix)
Last-Modified: Sat, 20 Nov 2004 07:16:26 GMT
ETag: "10000000565a5-2c-3e94b66c2e680"
Accept-Ranges: bytes
Content-Length: 44
Connection: close
Content-Type: text/html
  
<html><body><h1>It works!</h1></body></html>
'''

def authenticate(request):
    if 'Authorization: Basic' in request:
        print "verify with htdoc"
        return True
    return False

def handle_request(cls, request):
    
    if 'basic' in cls._MockHTTPServer__authScheme.lower() :
        if not authenticate(request):
            return '''
HTTP/1.1 401
WWW-Authenticate: Basic realm="aux realm"
Content-Type: text/xml;charset=utf-8
Connection: keep-alive

'''
    
    if 'SOAPAction' in request:
        return '''
HTTP/1.1 200 OK
Server: nginx/1.5.4
Date: Wed, 12 Feb 2014 09:58:13 GMT
Content-Type: text/xml;charset=utf-8
Content-Length: 4734
Connection: keep-alive
Set-Cookie: JSESSIONID=oijoij6E0C7479C4CF531A5842241F47; Path=/; HttpOnly
X-Request-Received: 1392199092003
SOAPAction: ""

<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
<SOAP-ENV:Header/><SOAP-ENV:Body></SOAP-ENV:Body></SOAP-ENV:Envelope>
'''
    
    if '__GET /basic_authenticated' in request:
        return '''
HTTP/1.1 403 OK

basic auth'''
#         https_response = '''\
# HTTP/1.1 401
# WWW-Authenticate: Basic realm="AUX-test"
# '''
    
    return http_response


class MockHTTPServer(object):
    def __init__(self, port=8989):
        self.port = port
        self.host = '127.0.0.1'
        self.__socket = socket.socket()
        self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.__authScheme = None
        
    def start(self):
        self.__socket.bind((self.host, self.port))
        self.__socket.listen(5)
        while True:
            c, addr = self.__socket.accept()
            
            c.send(handle_request(self, c.recv(4096)))
            c.close()

    def start_thread(self):
        self.p = Process(target=self.start)
        self.p.daemon = True
        self.p.start()
        time.sleep(.01)

    def stop(self):
        self.p.terminate()
        self.__socket.close()

    def set_authentication(self, authentication):
        self.__authScheme = authentication
        

class MockHTTPSServer(MockHTTPServer):
    def __init__(self, port=8443):
        self.parent = super(MockHTTPSServer, self)
        self.parent.__init__(port=port)
        self.__socket = socket.socket()
        self.__socket = socket.socket()
        self.__socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)


    def start(self):
        self.__socket.bind((self.host, self.port))
        self.__socket.listen(5)
        while True:
            ssl_sock, addr = self.__socket.accept()
            sock = wrap_socket(
                ssl_sock,
                server_side=True,
                certfile='../data/certs/unit-test.crt',
                keyfile='../data/certs/unit-test.key',
                ssl_version=ssl.PROTOCOL_TLSv1)

            sock.send(handle_request(self, sock.read()))
            sock.close()


    def stop(self):
        self.__socket.shutdown(SHUT_RDWR)
        self.parent.stop()


    def set_authenticatoin(self, authentication):
        self.parent.__authScheme = authentication
