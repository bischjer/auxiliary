from unittest2 import TestCase
from aux.protocols.http import HTTPProtocol, HTTPRequest
from ..util.mockhttpserver import MockHTTPServer


class HTTPConnectionTest(TestCase):

    def setUp(self):
        self.test_server = MockHTTPServer(port=8989)
        self.test_server.start_thread()
        self.headers = {'Host': 'a.a.a',
                        'User-Agent': 'Aux/0.1 (X11; Ubuntu; Linux x86_64; rv:24.0)',
                        'Accept':'text/html, application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                        'Accept-Language': 'en-US,en-q=0.5',
                        'Referer': 'http://abc.abc',
                        'Cache-Control': 'max-stale=0',
                        'Connection': 'Keep-Alive'
                        }
        
    def tearDown(self):
        self.test_server.stop()
    
    def test_connection(self):
        http_iface = HTTPProtocol('http://127.0.0.1:8989')
        self.headers['Test-Controller'] = 'short_http_response'
        http_request = HTTPRequest({'method':'GET',
                                    'headers': self.headers,
                                    'data': 'fakedata'})
        
        response = http_iface.send_request(http_request)
        print 'response:', response
        self.assertTrue('200 OK' in response)
        self.assertTrue('<html>' in response)

        
    def test_handle_long_response(self):
        conn = HTTPProtocol('http://127.0.0.1:8989')
        self.headers['Test-Controller'] = 'long_http_response'
        http_request = HTTPRequest({'method':'GET',
                                    'headers': self.headers,
                                    'data': 'fakedata'})
        
        #create a test mock handler http in backend
