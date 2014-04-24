from unittest2 import TestCase
from aux.protocols.soap.wsdl import WSDL


class WSDLTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_basic_wsdl_descriptions_no_attrib(self):
        wsdl_data = "<descriptions></descriptions>"
        wsdl_object = WSDL(wsdl_data = wsdl_data)
        self.assertEquals(None, wsdl_object.name)

    def test_basic_wsdl_descriptions_called_definitions(self):
        wsdl_data = "<definitions name=\"TestService\"></definitions>"
        wsdl_object = WSDL(wsdl_data = wsdl_data)
        self.assertEquals(None, wsdl_object.name)

    def test_basic_wsdl_descriptions(self):
        wsdl_data = "<descriptions name=\"TestService\"></descriptions>"
        wsdl_object = WSDL(wsdl_data = wsdl_data)
        self.assertEquals("TestService", wsdl_object.name)

    def test_basic_wsdl_service(self):
        #TODO: might need tag closure preprocessor
        wsdl_data = """
<descriptions name=\"TestService\" 
   targetNamespace="http://www.examples.com/wsdl/HelloService.wsdl"
   xmlns="http://schemas.xmlsoap.org/wsdl/"
   xmlns:soap="http://schemas.xmlsoap.org/wsdl/soap/"
   xmlns:tns="http://www.examples.com/wsdl/HelloService.wsdl"
   xmlns:xsd="http://www.w3.org/2001/XMLSchema">
   <service name="HelloService">
      <documentation>WSDL File for HelloService</documentation>
      <port binding="tns:Hello_Binding" name="Hello_Port">
         <soap:address
            location="http://www.examples.com/SayHello/"/>
      </port>
   </service>
</descriptions>"""
        wsdl_object = WSDL(wsdl_data = wsdl_data)
        self.assertEquals("HelloService", wsdl_object.services[0].name)
        
