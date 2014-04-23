from unittest2 import TestCase
from aux.protocols.soap.wsdl import WSDL

wsdl_data_ticket_agent = """<?xml version="1.0" encoding="UTF-8"?>
<wsdl:description 
    targetNamespace="http://example.org/TicketAgent.wsdl20" 
    xmlns:xsTicketAgent="http://example.org/TicketAgent.xsd" 
    xmlns:wsdl="http://www.w3.org/ns/wsdl" 
    xmlns:xs="http://www.w3.org/2001/XMLSchema" 
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
    xsi:schemaLocation="http://www.w3.org/ns/wsdl http://www.w3.org/2007/06/wsdl/wsdl20.xsd">
        
    <wsdl:types>
        <xs:import schemaLocation="TicketAgent.xsd" 
                   namespace="http://example.org/TicketAgent.xsd" />
    </wsdl:types>
        
    <wsdl:interface name="TicketAgent">
        <wsdl:operation name="listFlights"
                        pattern="http://www.w3.org/ns/wsdl/in-out">
            <wsdl:input element="xsTicketAgent:listFlightsRequest"/>
            <wsdl:output element="xsTicketAgent:listFlightsResponse"/>
        </wsdl:operation>
                
        <wsdl:operation name="reserveFlight"
                        pattern="http://www.w3.org/ns/wsdl/in-out">
            <wsdl:input element="xsTicketAgent:reserveFlightRequest"/>
            <wsdl:output element="xsTicketAgent:reserveFlightResponse"/>
        </wsdl:operation>
    </wsdl:interface>
</wsdl:description>
"""


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
   <service name="Hello_Service">
      <documentation>WSDL File for HelloService</documentation>
      <port binding="tns:Hello_Binding" name="Hello_Port">
         <soap:address
            location="http://www.examples.com/SayHello/"/>
      </port>
   </service>
</descriptions>"""
        wsdl_object = WSDL(wsdl_data = wsdl_data)
        self.assertEquals("TestService", wsdl_object.name)
