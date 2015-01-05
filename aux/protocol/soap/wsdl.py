from lxml import objectify
from lxml import etree
from urlparse import urlparse
from aux.api import http
from aux.protocol.srd import SRD, SRDOperationCaller


class WSDLPort(object):
    def __init__(self, e):
        self.e = e
        self.name = e.get('name')
        self.binding = e.attrib.get('binding')
        self.ext_element = e.getchildren()[0]

class WSDLElement(object):
    #WIKI: XML Element SimpleType|ComplexType
    def __init__(self, e):
        self.e = e
        self.name = self.e.get('name')
        self.subelements = self.e.findall('%scomplexType' % WSDL.get_ns(self.e,
                                                                       'xs'))

class WSDLSchema(object):
    def __init__(self, e):
        self.e = e
        self.elements = [WSDLElement(elem) for elem in e.findall('%selement' % WSDL.get_ns(e, 'xs'))]

    
class WSDLTypes(object):
    def __init__(self, e):
        self.e = e
        self.schemas = [WSDLSchema(s) for s in self.e]
        

class WSDLMessagePart(object):
    def __init__(self, e):
        self.e = e
        if self.e is not None:
            self.name = e.get('name')
            self.element = e.attrib.get('element')
        
class WSDLMessage(object):
    def __init__(self, e):
        self.e = e
        if self.e is not None:
            self.name = self.e.get('name')
            self.part = WSDLMessagePart(self.e.find('%spart' % WSDL.get_ns(self.e,
                                                                           'wsdl')))

class WSDLOperation(object):
    def __init__(self, e):
        self.e = e
        self.name = self.e.get('name')
        self.input = WSDLMessage( self.e.find('%sinput' % WSDL.get_ns(self.e,
                                                                      'wsdl')) )
        self.output = WSDLMessage( self.e.find('%soutput' % WSDL.get_ns(self.e,
                                                                        'wsdl')) )

class WSDLBinding(object):
    def __init__(self, e):
        self.e = e
        self.name = e.get('name')
        self.type = e.get('type')
        self.operations = [WSDLOperation(o) for o in e.findall('%soperation' % WSDL.get_ns(e, 'wsdl'))]
        #self.soap_operation = ?
        
class WSDLInterface(object):
    #WIKI: Also reads as PortType in old definition
    name = None
    operations = list()

    
class WSDLService(object):
    def __init__(self, e):
        self.name = e.get('name')
        ns = '{%s}' % e.nsmap.get('wsdl') if e.nsmap.get('wsdl') else '{%s}' % e.nsmap.get(None)
        self.documentation = e.find('%sdocumentation' % ns)
        self.ports = [WSDLPort(p) for p in e.findall('%sport' % ns)]
    

class WSDLOperationCaller(SRDOperationCaller):
    def __call__(self, kwargs={}):
        print kwargs
        print self.operation.name

        #build wsdl request
        print 'input.name', self.operation.input.name
        for schema in self.instance._s_types[0].schemas:
            for element in schema.elements:
                # print element.name
                if self.operation.input.name in element.name:
                    print etree.tostring(element.e)
                    print 'se:', element.subelements
                    # print 'name', element.name
                    # print element

        # for t in self.instance.__types:
        #     print t
        #build wsdl response
        print self.operation.output.name
        
        return "a"

    
class WSDL(SRD):

    def __init__(self, wsdl_url=None, wsdl_data=None):
        #WIKI: descriptions is often called definitions.        
        super(WSDL, self).__init__(WSDLOperationCaller)
        self.name = None
        self.__services = list()
        # self.wsdl_tree = None

    @classmethod
    def get_ns(cls, element, namespace):
        return '{%s}' % element.nsmap.get(namespace) if element.nsmap.get(namespace) else '{%s}' % element.nsmap.get(None)
    
    def load_wsdl(self, wsdl_url=None, wsdl_data=None):
        wsdl_string = None
        if wsdl_url is not None:
            wsdl_string = http.get(wsdl_url,
                                   headers=self.headers).body
        elif wsdl_data is not None:
            wsdl_string = wsdl_data
        if wsdl_string is not None:
            resource = etree.XML(wsdl_string)
            self.marshall_definition(resource)
        
        
    def marshall_definition(self, resource):
        tree = etree.ElementTree(resource)
        root = tree.getroot()
        self.__name = root.get('name', None)
        self.__services = [WSDLService(s) for s in root.findall('%sservice' % self.get_ns(root, 'wsdl'))]
        
        self._s_types = [WSDLTypes(t) for t in root.findall('%stypes' % self.get_ns(root, 'wsdl')) if t is not None]

        self.__messages = [WSDLMessage(m) for m in root.findall('%smessage' % self.get_ns(root, 'wsdl'))]
        
        porttype = root.find('%sportType' % self.get_ns(root, 'wsdl'))
        if porttype is not None:
            ops = [WSDLOperation(o) for o in porttype.findall('%soperation' % self.get_ns(root,'wsdl'))]
        for op in ops:
            self.set_operation(op)

        # self.__binding = [WSDLBinding(b) for b in root.findall('%sbinding' % self.get_ns(root, 'wsdl')) if b is not None]
        
