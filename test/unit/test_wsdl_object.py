from unittest2 import TestCase
from aux.protocols.soap import soap
from ..util.mockhttpserver import MockHTTPSServer

class WSDLObjectTest(TestCase):

    def setUp(self):
        self.test_server = MockHTTPSServer(port=8443)
        self.test_server.start_thread()

    def tearDown(self):
        self.test_server.stop()

    def test_create_soap_object_from_wsdl(self):
        wsdl_url = "../data/geoipservice.asmx?WSDL"

        wsdl = soap.create_wsdl(wsdl_url)


        print wsdl.GetGeoIPContext()
        print wsdl.GetGeoIP()

    def test_create_soap_object_from_http_wsdl(self):
        wsdl_url = "https://127.0.0.1:8443/geoipservice.asmx?WSDL"
        wsdl = soap.create_wsdl(wsdl_url)
        # print wsdl.hack()
        print "Wsdl service name:", wsdl.name
        #print wsdl.GetGeoIPContext()
        #print wsdl.GetGeoIP()
