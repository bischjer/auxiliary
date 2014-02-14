from lxml import objectify
from lxml import etree

class WSDL(object):

    def __init__(self, wsdl_url):
        wsdl_resource = open(wsdl_url)

        wsdl_tree = etree.XML(wsdl_resource.read())


        print dir(wsdl_tree)
        
        print etree.dump(wsdl_tree)


        
        # wsdl_obj = objectify.fromstring(wsdl_resource.read())
        # print wsdl_obj.find('binding')
        # print objectify.dump(wsdl_obj)
        
"""        
<wsdl:binding name="GeoIPServiceSoap" type="tns:GeoIPServiceSoap"><soap:binding transport="http://schemas.xmlsoap.org/soap/http"/><wsdl:operation name="GetGeoIP"><soap:operation soapAction="http://www.webservicex.net/GetGeoIP" style="document"/><wsdl:input><soap:body use="literal"/></wsdl:input><wsdl:output><soap:body use="literal"/></wsdl:output></wsdl:operation><wsdl:operation name="GetGeoIPContext"><soap:operation soapAction="http://www.webservicex.net/GetGeoIPContext" style="document"/><wsdl:input><soap:body use="literal"/></wsdl:input><wsdl:output><soap:body use="literal"/></wsdl:output></wsdl:operation></wsdl:binding>
"""


"""
<wsdl:binding name="GeoIPServiceSoap12" type="tns:GeoIPServiceSoap"><soap12:binding transport="http://schemas.xmlsoap.org/soap/http"/><wsdl:operation name="GetGeoIP"><soap12:operation soapAction="http://www.webservicex.net/GetGeoIP" style="document"/><wsdl:input><soap12:body use="literal"/></wsdl:input><wsdl:output><soap12:body use="literal"/></wsdl:output></wsdl:operation><wsdl:operation name="GetGeoIPContext"><soap12:operation soapAction="http://www.webservicex.net/GetGeoIPContext" style="document"/><wsdl:input><soap12:body use="literal"/></wsdl:input><wsdl:output><soap12:body use="literal"/></wsdl:output></wsdl:operation></wsdl:binding>
"""
