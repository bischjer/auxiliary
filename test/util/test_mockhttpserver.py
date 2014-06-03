from unittest2 import TestCase
from aux.protocols.http import HTTPResponse
from .mockhttpserver import WebService

class MockHTTPServerTest(TestCase):

    def test_no_service_defined(self):
        ws = WebService()
        response = ws.call_app()
        self.assertTrue(response.status == 500)


    def test_service_defined(self):
        def test_app(environ, start_response):
            return HTTPResponse(200, {'body':'OK'})
        ws = WebService()
        ws.app = test_app
        response = ws.call_app()
        self.assertTrue(response.status == 200)
