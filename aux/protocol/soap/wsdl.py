from lxml import objectify
from lxml import etree
from urlparse import urlparse
from aux.api import http
from aux.protocol.srd import SRD


class WSDLPort(object):
    def __init__(self, e):
        self.e = e
        self.name = e.get('name')
        self.binding = e.attrib.get('binding')
        self.ext_element = e.getchildren()[0]

class WSDLPortType(object):
    def __init__(self, e):
        self.e = e
        self.name = self.e.get('name')
        self.operations = [WSDLOperation(o) for o in self.e.findall('%soperation' % WSDL.get_ns(self.e, 'wsdl'))]

#WIKI: Also reads as PortType in old definition        
class WSDLInterface(WSDLPortType):pass

class XMLComplexType(object):
    def __init__(self, e):
        self.e = e
        # print etree.tostring(e)
        # print 
        self.seq = self.e.findall('%ssequence' % WSDL.get_ns(self.e, 'xs'))
        elems = None
        if len(self.seq) > 0:
            elems = [e for e in self.seq[0].findall('%selement' % WSDL.get_ns(self.e, 'xs'))]
        if elems is None:
            self.elements = []
        else:
            self.elements = elems
            # for el in elems:
                # print el.get('name')
                # print el.get('type')
                # print etree.tostring(el)
                # print



class XMLSimpleType(object):
    def __init__(self, e):
        self.e = e
        
        
class WSDLElement(object):
    #WIKI: XML Element SimpleType|ComplexType
    def __init__(self, e):
        self.e = e
        self.name = self.e.get('name')
        self.subelements = [XMLComplexType(se) for se in self.e.findall('%scomplexType' % WSDL.get_ns(self.e, 'xs'))]
        self.subelements.extend([XMLSimpleType(se) for se in self.e.findall('%ssimpleType' % WSDL.get_ns(self.e, 'xs'))])

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
        self.soap_binding = e.find('%sbinding' % WSDL.get_ns(e, 'soap'))
        self.operations = [WSDLOperation(o) for o in e.findall('%soperation' % WSDL.get_ns(e, 'wsdl'))]
        #self.soap_operation = ?
        
    
class WSDLService(object):
    def __init__(self, e):
        self.name = e.get('name')
        ns = '{%s}' % e.nsmap.get('wsdl') if e.nsmap.get('wsdl') else '{%s}' % e.nsmap.get(None)
        self.documentation = e.find('%sdocumentation' % ns)
        self.ports = [WSDLPort(p) for p in e.findall('%sport' % ns)]
    

class WSDLDefinitions(object):
    def __init__(self, e):
        self.e = e
        self.types = [WSDLTypes(t) for t in self.e.findall('%stypes' % WSDL.get_ns(self.e, 'wsdl'))]
        self.messages = [WSDLMessage(m) for m in self.e.findall('%smessage' % WSDL.get_ns(self.e, 'wsdl'))]
        self.portType = WSDLPortType(self.e.find('%sportType' % WSDL.get_ns(self.e, 'wsdl')))
        self.binding = WSDLBinding(self.e.find('%sbinding' % WSDL.get_ns(self.e, 'wsdl')))
        # print etree.tostring(self.e)
        self.service = WSDLService(self.e.find('%sservice' % WSDL.get_ns(self.e, 'wsdl')))
        
        
class WSDL(SRD):

    def __init__(self, wsdl_url=None, wsdl_data=None):
        #WIKI: descriptions is often called definitions.        
        super(WSDL, self).__init__()
        self.name = None
        self.__services = list()
        self.channels = dict()
        # self.wsdl_tree = None

    @classmethod
    def get_ns(cls, element, namespace):
        return '{%s}' % element.nsmap.get(namespace) if element.nsmap.get(namespace) else '{%s}' % element.nsmap.get(None)
    
    def load_wsdl(self, channel_name, wsdl_url=None, wsdl_data=None):
        wsdl_string = None
        if wsdl_url is not None:
            wsdl_string = http.get(wsdl_url,
                                   headers=self.headers).body
        elif wsdl_data is not None:
            wsdl_string = wsdl_data
        if wsdl_string is not None:
            resource = etree.XML(wsdl_string)
            self.channels[channel_name] = WSDLDefinitions(resource)
            # self.marshall_definition(resource)

    @classmethod
    def send_request(cls, url, soap_body):
        print url
        print soap_body
        return http.post(url,
                         body=soap_body)
        # return "fakeresponse"
        
        
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
        
