from lxml import objectify
from lxml import etree
from urlparse import urlparse
from aux.api import http


class WSDLPort(object):
    def __init__(self, name, binding, extensibility=None):
        self.name = name
        self.binding = binding
        self.extensibility = extensibility

class WSDLElement(object):
    #WIKI: XML Element SimpleType|ComplexType
    name = None
        
class WSDLTypes(object):
    #<xs:import schemaLocation="TicketAgent.xsd" namespace="http://example.org/TicketAgent.xsd" />
    #<schema targetNamespace="http://example.com/stockquote.xsd" xmlns="http://www.w3.org/2000/10/XMLSchema">
    pass
    
class WSDLMessage(object):
    name = None
    part = None

class WSDLOperation(object):
    def __init__(self, name, soapAction):
        self.name = name
        self.soapAction = soapAction

    def __call__(self):
        return self.name

class WSDLBinding(object):
    def __init__(self, name, _type):
        self.name = name
        self.type = _type
        #TODO: impl soap stuff
        self.soap_binding = None
        self.soap_operation = None
        self.soap_body = None
        
class WSDLInterface(object):
    #WIKI: Also reads as PortType in old definition
    name = None
    operations = list()

    
class WSDLService(object):
    def __init__(self, name, documentation=None, ports=list()):
        self.name = name
        self.documentation = documentation
        self.ports = ports
    
    
class WSDL(object):

    def __init__(self, wsdl_url=None, wsdl_data=None):
        pass
        # if wsdl_url:
        #     self.url = wsdl_url
        #     wsdl_data = self.get_wsdl_details(self.url)
        # # print "[%s]" % wsdl_data        # print urlparse(self.url)            

        # #WIKI: descriptions is sometimes defined as definitions.
        # self.name = None
        self.methods = {}
        # self.interfaces = list()
        # self.services = list()
        # self.resource = etree.XML(wsdl_data)
        # self.unmarshall_definition(self.resource)

        
    def __getattr__(self, attr):
        method = self.methods.get(attr, None)
        if method is not None:
            return lambda: method
        else:
            emsg = "%s object has no attribute '%s'" % (self.__class__.__name__, attr)
            raise AttributeError(emsg)

    def get_wsdl_details(self, wsdl_url):
        wsdl_response = http.get(wsdl_url,
                                 headers=self.headers)
        self.resource = etree.XML(wsdl_response.body)
        self.unmarshall_definition(self.resource)

        
    def unmarshall_definition(self, resource):
        self.tree = etree.ElementTree(resource)
        root = self.tree.getroot()
        # print etree.tostring(root), root.tag
        # print root.tag.lower()
        # if "definitions" in root.tag.lower():
        #     self.name = root.attrib.get('name', None)

        messages = root.findall('{http://schemas.xmlsoap.org/wsdl/}message')
        for message in messages:
            key = message.attrib.get('name')
            self.methods[ key ] = "placeholder for %s" % key
            # print self.methods
        # # try:
        # #     service = root.find("service", namespaces=root.nsmap)
        # #     print service
        # # except:
        # #     pass
        # services = root.findall('{http://schemas.xmlsoap.org/wsdl/}service')
        # for service in services:
        #     # print ":: ", service.attrib.get('name', None)
        #     service_name = service.attrib.get('name', None)
        #     service_documentation = service.find('{http://schemas.xmlsoap.org/wsdl/}documentation').text
        #     service_ports = []
        #     for port in service.findall('{http://schemas.xmlsoap.org/wsdl/}port'):
        #         port_name = port.attrib.get('name', None)
        #         port_binding = port.attrib.get('binding', None)
        #         # print port.text
        #         port_extensibility = port.text
        #         # print port_extensibility
        #         service_ports.append(WSDLPort(port_name,
        #                                       port_binding, #WSDLBinding # sort out namespacing
        #                                       port_extensibility))
            
        #     self.services.append(WSDLService(service_name,
        #                                      service_documentation,
        #                                      service_ports))

        # if len(self.services) > 0:
        #     pass
            # print self.services[0].name

        # if service:
        #     print service.tag
        # for child in root.getchildren():
        #     print ":: ", child.tag

            
        # for child in root.getchildren():
        #     if '{http://schemas.xmlsoap.org/wsdl/}service' == child.tag:
        #         print ':::::', child.attrib.get('name', None)
        #         # self.name = child.attrib.get('name', None)
        #     if '{http://schemas.xmlsoap.org/wsdl/}binding' == child.tag:
        #         for ochild in child.getchildren():
        #             if '{http://schemas.xmlsoap.org/wsdl/}operation' == ochild.tag:
        #                 operationName = ochild.attrib.get('name', None)
        #                 for l3ch in ochild.getchildren():
        #                     if '{http://schemas.xmlsoap.org/wsdl/soap/}operation' == l3ch.tag:
        #                         soapAction = l3ch.attrib.get('soapAction', None)
        #                         if soapAction:
        #                             # self.operations[operationName] = lambda: soapAction
        #                             self.operations[operationName] = WSDLOperation(operationName,
        #                                                                            soapAction)

        # print dir(child)
        # print etree.tostring(tree)
        # print tree.docinfo.doctype
        # print dir(wsdl_tree)
        # print etree.dump(wsdl_tree)
        # wsdl_obj = objectify.fromstring(wsdl_resource.read())
        # print wsdl_obj.find('binding')
        # print objectify.dump(wsdl_obj)
        
