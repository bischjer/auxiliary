from unittest2 import TestCase
from aux.protocols.soap import soap


class WSDLObjectTest(TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_soap_object_from_wsdl(self):
        wsdl_url = "../data/geoipservice.asmx?WSDL"

        wsdl = soap.create_wsdl(wsdl_url)


        print wsdl.GetGeoIPContext()
        print wsdl.GetGeoIP()

    def test_create_soap_object_from_http_wsdl(self):
        wsdl_url = "http://www.webservicex.net/geoipservice.asmx?WSDL"

        wsdl = soap.create_wsdl(wsdl_url)

        # print wsdl.hack()
        print "Wsdl service name:", wsdl.name
        #print wsdl.GetGeoIPContext()
        #print wsdl.GetGeoIP()
