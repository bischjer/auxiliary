from unittest2 import TestCase
from aux.protocol.http.http import HTTP


class FakeTransport(object):

    def __init__(self, message):
        self.fake_message = message

    def recv(self):
        return self.fake_message
    
    def close(self):
        pass


class HTTP_RECEIVE_TEST(TestCase):

    def test_receive_200_startline_only(self):
        message = "HTTP/1.1 200 OK\r\n"
        http = HTTP()
        response = http.receive(FakeTransport(message))
        self.assertEquals(response.status,
                          200)

    def test_receive_200_only_headers(self):
        message = """HTTP/1.1 200 OK
Server: nginx/1.5.13
Date: Sat, 02 Aug 2014 19:40:38 GMT
Content-Type: text/html
Content-Length: 0
Last-Modified: Mon, 14 Apr 2014 08:38:26 GMT
Connection: keep-alive
Expires: Sat, 02 Aug 2014 20:40:38 GMT
Cache-Control: max-age=3600
Accept-Ranges: bytes
"""
        http = HTTP()
        response = http.receive(FakeTransport(message))
        print response
        # self.assertEquals(response.headers == )

