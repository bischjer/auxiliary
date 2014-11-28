from lxml import objectify
from lxml import etree
from urlparse import urlparse
from aux.api import http


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
        self.name = e.get('name')
        

class WSDLSchema(object):
    def __init__(self, e):
        self.e = e
        self.elements = [WSDLElement(elem) for elem in e.findall('%selement' % WSDL.get_ns(e, 'xs'))]

    
class WSDLTypes(object):
    def __init__(self, e):
        self.schemas = [WSDLSchema(s) for s in e]
        

class WSDLMessagePart(object):
    def __init__(self, e):
        self.e = e
        self.name = e.get('name')
        self.element = e.attrib.get('element')
        
class WSDLMessage(object):
    def __init__(self, e):
        self.e = e
        self.name = e.get('name')
        self.part = WSDLMessagePart(e.find('%spart' % WSDL.get_ns(e, 'wsdl')))

class WSDLOperation(object):
    def __init__(self, e):
        self.e = e
        self.name = e.get('name')
        self.input = e.find('%sinput' % WSDL.get_ns(e, 'wsdl'))
        self.output = e.find('%soutput' % WSDL.get_ns(e, 'wsdl'))


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
    

class WSDL(object):

    def __init__(self, wsdl_url=None, wsdl_data=None):
        #WIKI: descriptions is often called definitions.
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
                # print self.method

                operation = [o for o in self.wsdl_instance._w_binding[0].operations if o.name == self.method]
                if len(operation) > 0:
                    print operation[0].name
                    # print operation[0].input.get('name')
                    # print operation[0].output.get('name')
                    
                    #TODO must find the correct schema in list of schemas
                    for elem in  self.wsdl_instance._w_types[0].schemas[0].elements:
                        print elem.name
                    
                # for m in self.wsdl_instance._w_messages:
                #     print m.name
                # print [m for m in self.wsdl_instance._w_messages if m.name == self.method]

                # method_request
                # method_request_type
                # method_request_type_soap_request_data
                
                # rtypes = self.wsdl_instance.types.get(self.method.get('request'))
                # for t in rtypes:
                #     print t.get('name')es
                # print self.wsdl_instance.wsdl_tree

                # print self.wsdl_instance.operations.get(self.method)
                return "nothing"#self.wsdl_instance.operations.get(method)
        return MethodCaller(self, method)
    
    def __getattr__(self, attr):
        method = [op for op in self._w_operations if op.name == attr]
        if len(method) > 0:
            return self.__attrMethod(method[0].name)
        else:
            emsg = "%s object has no attribute '%s'" % (self.__class__.__name__, attr)
            raise AttributeError(emsg)
        
    @classmethod
    def get_ns(cls, element, namespace):
        return '{%s}' % element.nsmap.get(namespace) if element.nsmap.get(namespace) else '{%s}' % element.nsmap.get(None)
    
    def load_wsdl(self, wsdl_url=None, wsdl_data=None):
        if wsdl_url is not None:
            wsdl_string = http.get(wsdl_url,
                                   headers=self.headers).body
        else:
            wsdl_string = wsdl_data
        self.resource = etree.XML(wsdl_string)
        self.marshall_definition(self.resource)

        
    def marshall_definition(self, resource):
        self._w_wsdl_tree = etree.ElementTree(resource)
        root = self._w_wsdl_tree.getroot()

        self._w_name = root.get('name', None)
        self._w_services = [WSDLService(s) for s in root.findall('%sservice' % self.get_ns(root, 'wsdl'))]
        
        self._w_types = [WSDLTypes(t) for t in root.findall('%stypes' % self.get_ns(root, 'wsdl')) if t is not None]

        self._w_messages = [WSDLMessage(m) for m in root.findall('%smessage' % self.get_ns(root, 'wsdl'))]
        
        porttype = root.find('%sportType' % self.get_ns(root, 'wsdl'))
        if porttype is not None:
            self._w_operations = [WSDLOperation(o) for o in porttype.findall('%soperation' % self.get_ns(root,'wsdl'))]

        self._w_binding = [WSDLBinding(b) for b in root.findall('%sbinding' % self.get_ns(root, 'wsdl')) if b is not None]
            
        # print self.get_ns(root, 'wsdl')
        # types = root.find("%stypes", self.get_ns(root, 'wsdl'))
        # print 'types', types
        # # print [m for m in types.findall('%schema' % self.get_ns(root, 'xs'))]

        # porttype = root.find("%sportType", self.get_ns(root, 'wsdl'))
        # print 'pt', porttype

        # messages = [m for m in root.findall("%message", self.get_ns(root, 'wsdl'))]
        # print 'msg', messages

        
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
        
