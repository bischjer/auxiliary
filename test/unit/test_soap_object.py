from unittest2 import TestCase
from aux.protocols.soap import soap


class SoapObjectTest(TestCase):


    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_soap_object_from_wsdl(self):
        wsdl_url = "../data/geoipservice.asmx?WSDL"

        wsdl = soap.create_wsdl(wsdl_url)

        wsdl.GetGeoIPCOntext()
