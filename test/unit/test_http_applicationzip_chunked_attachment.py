from unittest2 import TestCase
from aux.protocol.http.mime import ZIPController
import struct

response_data = "hello world"

class ZipControllerTest(TestCase):

    def test_zip_controller(self):
        zc = ZIPController('attachment; filename="zipcontrollertest.zip"',
                           response_data)

        print zc.data

        zc.handle()
