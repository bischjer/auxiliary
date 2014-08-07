from aux.protocol.transport import TCP_DEFAULT_FRAME_SIZE
import re

class DefaultController(object):

    def __init__(self, headers, transport, msg):
        self.headers = headers
        self.transport = transport
        self.msg = msg

    def read(self):
        content_length = int(self.headers.get('Content-Length', 0))
        return self.msg[0: content_length]

class NoContentController(object):
    def __init__(self, headers, transport, msg):
        self.headers = headers
        self.transport = transport
        self.msg = msg

    def read(self):
        return self.msg
    
class ChunkedController(object):

    def __init__(self, headers, transport, msg):
        self.headers = headers
        self.transport = transport
        self.msg = msg
        
    def read(self):
        re_chunk = re.compile(r'^([a-f|\d]{1,4})\r\n')
        re_end_chunk = re.compile(r'^0\r\n\r\n0')
        #TODO: this could be better
        raw_response = self.msg
        response = ""
        while 1:
            next_chunk = re_chunk.findall(raw_response[0:8])
            end_chunk = re_end_chunk.findall(raw_response[0:8])
            if int(next_chunk[0], 16) > len(raw_response):
                raw_response += self.transport.recv()
            if len(next_chunk) > 0:
                if int(next_chunk[0], 16) == 0 or len(end_chunk) > 0:
                    break
                raw_response = raw_response[len(next_chunk[0])+2:]
                response += raw_response[:int(next_chunk[0], 16)]
                raw_response = raw_response[int(next_chunk[0], 16)+2:]
        return response

def transferFactory(headers):
    content_length = headers.get('Content-Length', None)
    if content_length != None:
        if int(content_length) < 1:
            return NoContentController
    content_type = headers.get('Transfer-Encoding', None)
    if content_type != None:
        if 'chunked' in content_type.lower():
            return ChunkedController
    return DefaultController
