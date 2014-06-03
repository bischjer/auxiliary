from unittest2 import TestCase
from aux.protocols.http import HTTPResponse
from .mockhttpserver import WebService, WebServer


def test_app_ok(environ, start_response):
    return HTTPResponse(200, {'body': 'OK'})


class MockHTTPServerTest(TestCase):
    
    def test_no_service_defined(self):
        ws = WebService()
        response = ws.call_app()
        self.assertTrue(response.status == 500)

    def test_service_defined(self):
        ws = WebService()
        ws.app = test_app
        response = ws.call_app()
        self.assertTrue(response.status == 200)

    def test_web_server(self):
        ws = WebService()
        ws.app = test_app
        
        server = WebServer()
        
