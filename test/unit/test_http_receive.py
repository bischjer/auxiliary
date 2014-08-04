from unittest2 import TestCase
from aux.protocol.http.http import HTTP


class FakeTransport(object):

    def __init__(self, message):
        self.fake_message = message
        self.bytes_read = 0
        
    def recv(self, nofchar=1200):
        buffer = ""
        for n in xrange(0, nofchar):
            if self.bytes_read >= len(self.fake_message):
                break
            else:
                buffer += self.fake_message[self.bytes_read]
            self.bytes_read += 1
        return buffer
    
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
        message = """HTTP/1.1 200 OK\r\nServer: nginx/1.5.13\r\nDate: Sat, 02 Aug 2014 19:40:38 GMT\r\nContent-Type: text/html\r\nContent-Length: 0\r\nLast-Modified: Mon, 14 Apr 2014 08:38:26 GMT\r\nConnection: keep-alive\r\nExpires: Sat, 02 Aug 2014 20:40:38 GMT\r\nCache-Control: max-age=3600\r\nAccept-Ranges: bytes\r\n\r\n"""
        http = HTTP()
        response = http.receive(FakeTransport(message))
        self.assertEquals(len(response.body), 0)
        self.assertEquals(len(response.headers), 8)
                          
    def test_receive_200_with_json_body(self):
        message = """HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 15\r\n\r\n{{Hello:world}}"""
        http = HTTP()
        response = http.receive(FakeTransport(message))
        self.assertEqual(len(response.body), 15)

    def test_receive_200_with_chunked_body(self):
        message = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nTransfer-Encoding : chunked\r\n\r\n1a\r\nABCDEFGHIJKLMNOPQRSTUVWXYZ\r\n0\r\n\r\n0"""
        http = HTTP()
        response = http.receive(FakeTransport(message))
        # print "[",response.body,"]"
        self.assertEqual(len(response.body), 26)

        
