from unittest2 import TestCase
from aux.protocols.http import HTTPSConnection
from ..util.mockhttpserver import MockHTTPSServer

class HTTPSConnectionTest(TestCase):
    
    def setUp(self):
        self.test_server = MockHTTPSServer(port=8443)
        self.test_server.start_thread()

    def tearDown(self):
        self.test_server.stop()

    def test_connection_success(self):
        conn = HTTPSConnection('127.0.0.1', 8443)
        http_request = '''\
GET / HTTP/1.1
Host: a.a.a
User-Agent: Aux/0.1 (X11; Ubuntu; Linux x86_64; rv:24.0)
Accept: text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Referer: http://abc.abc
Cache-Control: max-stale=0
Connection: Keep-Alive
'''
        response = conn.send_request(http_request)
        self.assertTrue('It works!' in response)



