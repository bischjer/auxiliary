from lxml import objectify
from lxml import etree
from urlparse import urlparse
from aux.api import http


class WSDLPort(object):
    def __init__(self, e):
        # name, binding, extensibility=None):
        
        self.name = e.get('name')
        self.binding = e.attrib.get('binding')
        # self.extensibility = extensibility

class WSDLElement(object):
    #WIKI: XML Element SimpleType|ComplexType
    name = None

class WSDLSchemas(object):
    pass
    
class WSDLTypes(object):
    #<xs:import schemaLocation="TicketAgent.xsd" namespace="http://example.org/TicketAgent.xsd" />
    #<schema targetNamespace="http://example.com/stockquote.xsd" xmlns="http://www.w3.org/2000/10/XMLSchema">
    def __init__(self):
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
    def __init__(self, e):
        self.name = e.get('name')
        ns = '{%s}' % e.nsmap.get('wsdl') if e.nsmap.get('wsdl') else '{%s}' % e.nsmap.get(None)
        self.documentation = e.find('%sdocumentation' % ns)
        self.ports = [WSDLPort(p) for p in e.findall('%sport' % ns)]
    

class WSDL(object):

    def __init__(self, wsdl_url=None, wsdl_data=None):
        # if wsdl_url:
        #     self.url = wsdl_url
        #     wsdl_data = self.get_wsdl_details(self.url)
        # # print "[%s]" % wsdl_data        # print urlparse(self.url)            

        # #WIKI: descriptions is often called definitions.
        self.name = None
        self.services = []
        self.operations = {}
        self.types = {}
        self.wsdl_tree = None

        self.load_wsdl(wsdl_url, wsdl_data)

    def __attrMethod(self, method):
        class MethodCaller(object):
            def __init__(self, wsdl_instance, method):
                self.wsdl_instance = wsdl_instance
                self.method = method
                
            def __call__(self, kwargs={}):
                request_json = dict()
                print self.method
                rtypes = self.wsdl_instance.types.get(self.method.get('request'))

                # for t in rtypes:
                #     print t.get('name')es
                # print self.wsdl_instance.wsdl_tree

                # print self.wsdl_instance.operations.get(self.method)
                return "nothing"#self.wsdl_instance.operations.get(method)
        return MethodCaller(self, method)
    
    def __getattr__(self, attr):
        method = self.operations.get(attr, None)
        if method is not None:
            return self.__attrMethod(method)
        else:
            emsg = "%s object has no attribute '%s'" % (self.__class__.__name__, attr)
            raise AttributeError(emsg)

    def get_ns(self, element, namespace):
        return '{%s}' % element.nsmap.get('wsdl') if element.nsmap.get(namespace) else '{%s}' % element.nsmap.get(None)        
    def load_wsdl(self, wsdl_url=None, wsdl_data=None):
        if wsdl_url is not None:
            wsdl_string = http.get(wsdl_url,
                                   headers=self.headers).body
        else:
            wsdl_string = wsdl_data
        self.resource = etree.XML(wsdl_string)
        self.marshall_definition(self.resource)

        
    def marshall_definition(self, resource):
        self.wsdl_tree = etree.ElementTree(resource)
        root = self.wsdl_tree.getroot()

        self.name = root.get('name', None)
        self.services = [WSDLService(s) for s in root.findall('%sservice' % self.get_ns(root, 'wsdl'))]
        
        
        # worky
        # porttype = root.find('{%s}portType' % root.nsmap.get('wsdl'))
        # for operation in porttype.findall('{%s}operation' % root.nsmap.get('wsdl')):
        #     key = operation.attrib.get('name')
        #     self.operations[key] = {'request': operation.find('{%s}input' % root.nsmap.get('wsdl')).get('name'),
        #                             'response':operation.find('{%s}output' % root.nsmap.get('wsdl')).get('name')}

        # types = self.wsdl_tree.find('{http://schemas.xmlsoap.org/wsdl/}types')
        # for t in types:
        #     print t
        # schemas = types.findall('{http://www.w3.org/2001/XMLSchema}schema')
        # for schema in schemas:
        #     elements = schema.findall('{%s}element' % schema.nsmap.get('xs'))
        #     for element in elements:
        #         self.types[element.get('name')] = element.find('{%s}complexType' % schema.nsmap.get('xs'))

        # print root.nsmap
        # print types.find('{http://schemas.xmlsoap.org/wsdl/}element')
        # print types.findall('{}schema')
            
        # messages = root.findall('{http://schemas.xmlsoap.org/wsdl/}message')
        # for message in messages:
        #     key = message.attrib.get('name')
        #     self.methods[ key ] = "placeholder for %s" % key
        #     print self.methods
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
        
