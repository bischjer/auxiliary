from unittest2 import TestCase
from aux.api import http

class WebTest(TestCase):

    def xtest_get_long_web_page(self):

        url = "http://www.w3.org/Protocols/rfc2616/rfc2616.html"

        response = http.get(url)

        print response

    def test_get_https_wsdl_page(self):
        url ="https://qa-test.kezzlerssp.com/ssp/kcengine-ws/kcengine.wsdl"
        headers = {"Connection":"keep-alive",
                   "Accept":"text/html"}
        headers.update(http.auth.basic("bischjer", "test")())
        response = http.get(url, headers=headers)

        print response.body
