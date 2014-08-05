from aux.protocol.transport import TCP_DEFAULT_FRAME_SIZE
import re

class DefaultController(object):

    def __init__(self, headers, transport, msg):
        self.headers = headers
        self.transport = transport
        self.msg = msg

    def read(self):
        raw_response = "\n".join(self.msg)
        in_buf = ""
        while 1:
            # print "default controller"
            try:
                in_buf = self.transport.recv()
            except Exception, e:
                print e.message
            if len(in_buf) < 1:
                break
            raw_response = raw_response + in_buf
            # print "[", raw_response, "]"
            in_buf = ""
        return raw_response

class NoContentController(object):
    def __init__(self, headers, transport, msg):
        self.headers = headers
        self.transport = transport
        self.message = msg

    def read(self):
        return ""
    
class ChunkedController(object):

    def __init__(self, headers, transport, msg):
        self.headers = headers
        self.transport = transport
        self.msg = msg

    def chunked_parser(self, raw_response):
        re_chunk = re.compile(r'^([a-f|\d]{1,4})\r\n')
        re_end_chunk = re.compile(r'^0\r\n\r\n0')
        #TODO: fix this horrible impl.
        response = ""
        while 1:
            next_chunk = re_chunk.findall(raw_response[0:8])
            end_chunk = re_end_chunk.findall(raw_response[0:8])
            if len(next_chunk) > 0:
                if int(next_chunk[0], 16) == 0 or len(end_chunk) > 0:
                    break
                raw_response = raw_response[len(next_chunk[0])+2:]
                response += raw_response[:int(next_chunk[0], 16)]
                raw_response = raw_response[int(next_chunk[0], 16)+2:]
        return response
        
    def read(self):
        re_chunk = re.compile(r'^([a-f|\d]+){1,4}\r\n')
        raw_response = ""
        in_buf = "\n".join(self.msg)
        raw_response = raw_response + in_buf
        #TODO: Should we read here har do we just take a complete read??
        return self.chunked_parser(raw_response)

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
