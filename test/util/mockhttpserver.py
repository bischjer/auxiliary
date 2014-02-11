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

def handle_request(request):
    # print request
    
    if '__GET /basic_authenticated' in request:
        return '''\
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


    def start(self):
        self.__socket.bind((self.host, self.port))
        self.__socket.listen(5)
        while True:
            c, addr = self.__socket.accept()
            
            c.send(handle_request(c.recv(4096)))
            c.close()

    def start_thread(self):
        self.p = Process(target=self.start)
        self.p.daemon = True
        self.p.start()
        time.sleep(.01)

    def stop(self):
        self.p.terminate()
        self.__socket.close()
    

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

            sock.send(handle_request(sock.read()))
            sock.close()


    def stop(self):
        self.__socket.shutdown(SHUT_RDWR)
        self.parent.stop()



