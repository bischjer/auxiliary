from base64 import b64encode

class Credentials(object):
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_as_basic_auth(self):
        return "Basic %s" % b64encode(b'%s%s' % (self.username, self.password))


class BaseService(object):
    _connection = None

class HTTPService(BaseService):

    
    def _head(self, request):
        pass
    
    def _post(self, request):
        pass

    def _delete(self, request):
        pass

    def get(self, request):
        if request.method == 'post':
            return self._post(request)
        elif request.method == 'head':
            return self._head(request)
        elif request.method == 'delete':
            return self._delete(request)

        

class HTTPSService(HTTPService):
    def __init__(self, args):
        self.url = args.get('url', None)

class ServiceFactory(object):
    def __init__(self):
        pass

    def get_service(self, service_type, args):
        if 'http' == service_type:
            return HTTPService(args)
        elif 'https' == service_type:
            return HTTPSService(args)
        return None


def service_factory(servicetype, args={}):
    factory = ServiceFactory()
    return factory.get_service(servicetype, args)



"""
class HTTPConnection(object):
    scheme = 'http'
    def __init__(self, url, credentials):

        self.url = url   
        self.credentials = credentials
        self.domain = None
        self.project = None

    def request(self, method, url, headers=None, data=None):
        print method, url, headers, data

    def response(self):
        return "fakedata fake fake fake fake"
        
        
class HTTPSConnection(HTTPConnection):
    scheme = 'https'
    def __init__(self, url, credentials):
        super(HTTPSConnection, self).__init__(url, credentials)
"""
