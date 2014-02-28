from aux.protocols.connection import Connection
from aux.protocols.http.http import HTTPConnection 
from aux.protocols.http.https import HTTPSConnection


class HTTPRequest(object):
    def __init__(self, request_data):
        self.target = None
        self.method = request_data.get('method', 'Get').upper()
        self.headers = request_data.get('headers', {})
        self.data = request_data.get('data', None)
        self.path = None

    def __str__(self):
        self.headers['Content-Length'] = str(len(self.data))
        return "%s %s HTTP/1.1\n%s\n\n%s" % (self.method,
                                              self.path,
                                              "\n".join([": ".join(item) for item in self.headers.items()]),
                                              self.data)


class HTTPResponse(object):
    def __init__(self, response_data):
        pass



