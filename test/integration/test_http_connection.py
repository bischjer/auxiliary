from unittest2 import TestCase
from aux.protocols.http import HTTPConnection, HTTPRequest
from ..util.mockhttpserver import MockHTTPServer


class HTTPConnectionTest(TestCase):

    def setUp(self):
        self.test_server = MockHTTPServer(port=8989)
        self.test_server.start_thread()

    def tearDown(self):
        self.test_server.stop()

    
    def test_connection(self):
        conn = HTTPConnection('http://127.0.0.1:8989')

        http_request = HTTPRequest({'method':'GET',
                                    'headers': {'Host': 'a.a.a',
                                                'User-Agent': 'Aux/0.1 (X11; Ubuntu; Linux x86_64; rv:24.0)',
                                                'Accept':'text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                                                'Accept-Language': 'en-US,en-q=0.5',
                                                'Referer': 'http://abc.abc',
                                                'Cache-Control': 'max-stale=0',
                                                'Connection': 'Keep-Alive',
                                                'Test-Controller': 'short_http_response'
                                                },
                                    'data': 'fakedata'})
        
        response = conn.send_request(http_request)
        print response
        self.assertTrue('200 OK' in response)
        self.assertTrue('<html>' in response)

        
    def test_handle_long_response(self):
        conn = HTTPConnection('http://127.0.0.1:8989')

        http_request = HTTPRequest({'method':'GET',
                                    'headers': {'Host': 'a.a.a',
                                                'User-Agent': 'Aux/0.1 (X11; Ubuntu; Linux x86_64; rv:24.0)',
                                                'Connection': 'Keep-Alive',
                                                'Test-Controller': 'long_http_response'
                                                },
                                    'data': 'fakedata'})
        
        #create a test mock handler http in backend
