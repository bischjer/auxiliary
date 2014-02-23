from lxml import objectify
from lxml import etree


class WSDLOperation(object):
    def __init__(self, name, soapAction):
        self.name = name
        self.soapAction = soapAction

    def __call__(self):
        print self.name
        print self.soapAction
        return self.name
        

class WSDL(object):

    def __init__(self, wsdl_url):
        #TODO: write stream handler for file or web
        self.resource = etree.XML(open(wsdl_url).read())
        self.tree = etree.ElementTree(self.resource)
        self.operations = dict()
        self.unmarshall_definition()
        
    def __getattr__(self, name):
        print self.operations
        opfound = self.operations.get(name, None)
        if opfound:
            return opfound
        else:
            raise AttributeError

    def wsdl_call(self, a):
        pass
        
    def unmarshall_definition(self):
        root = self.tree.getroot()
        for child in root.getchildren():
            if '{http://schemas.xmlsoap.org/wsdl/}binding' == child.tag:
                for ochild in child.getchildren():
                    if '{http://schemas.xmlsoap.org/wsdl/}operation' == ochild.tag:
                        operationName = ochild.attrib.get('name', None)
                        for l3ch in ochild.getchildren():
                            if '{http://schemas.xmlsoap.org/wsdl/soap/}operation' == l3ch.tag:
                                soapAction = l3ch.attrib.get('soapAction', None)
                                if soapAction:
                                    # self.operations[operationName] = lambda: soapAction
                                    self.operations[operationName] = WSDLOperation(operationName,
                                                                                   soapAction)

        # print dir(child)
        # print etree.tostring(tree)
        # print tree.docinfo.doctype
        # print dir(wsdl_tree)
        # print etree.dump(wsdl_tree)
        # wsdl_obj = objectify.fromstring(wsdl_resource.read())
        # print wsdl_obj.find('binding')
        # print objectify.dump(wsdl_obj)
        
"""        
<wsdl:binding name="GeoIPServiceSoap" type="tns:GeoIPServiceSoap"><soap:binding transport="http://schemas.xmlsoap.org/soap/http"/><wsdl:operation name="GetGeoIP"><soap:operation soapAction="http://www.webservicex.net/GetGeoIP" style="document"/><wsdl:input><soap:body use="literal"/></wsdl:input><wsdl:output><soap:body use="literal"/></wsdl:output></wsdl:operation><wsdl:operation name="GetGeoIPContext"><soap:operation soapAction="http://www.webservicex.net/GetGeoIPContext" style="document"/><wsdl:input><soap:body use="literal"/></wsdl:input><wsdl:output><soap:body use="literal"/></wsdl:output></wsdl:operation></wsdl:binding>
"""


"""
<wsdl:binding name="GeoIPServiceSoap12" type="tns:GeoIPServiceSoap">
<soap12:binding transport="http://schemas.xmlsoap.org/soap/http"/>
<wsdl:operation name="GetGeoIP">
<soap12:operation soapAction="http://www.webservicex.net/GetGeoIP" style="document"/>
<wsdl:input>
<soap12:body use="literal"/>
</wsdl:input>
<wsdl:output>
<soap12:body use="literal"/>
</wsdl:output></wsdl:operation>
<wsdl:operation name="GetGeoIPContext">
  <soap12:operation soapAction="http://www.webservicex.net/GetGeoIPContext" style="document"/>
  <wsdl:input>
    <soap12:body use="literal"/>
  </wsdl:input>
  <wsdl:output>
    <soap12:body use="literal"/>
  </wsdl:output>
</wsdl:operation>
</wsdl:binding>
"""
