from unittest2 import TestCase
from aux.api import http

class WebTest(TestCase):

    def test_get_long_web_page(self):

        url = "http://www.w3.org/Protocols/rfc2616/rfc2616.html"

        response = http.get(url)

        print response
