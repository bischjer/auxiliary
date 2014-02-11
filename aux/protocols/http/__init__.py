from aux.protocols.connection import Connection
from aux.protocols.http.http import HTTPConnection 
from aux.protocols.http.https import HTTPSConnection


class HTTPRequest(object):
    def __init__(self, request_data):
        self.method = request_data.get('method', 'Get').lower()
        self.headers = request_data.get('headers', {})
        self.data = request_data.get('data', None)

        
class HTTPResponse(object):
    pass



