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
            print "default controller"
            try:
                in_buf = self.transport.recv()
            except Exception, e:
                print e.message
            if len(in_buf) < 1:
                break
            raw_response = raw_response + in_buf
            print "[", raw_response, "]"
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
        re_chunk = re.compile(r'^([a-f|\d]{1,4})\r')
        #TODO: fix this horrible impl.
        print raw_response
        response = ""
        data = raw_response.split('\n')
        curr_line = ""
        # print "chunked_parser_entry"
        for next_line in data:
            is_next_a_chunk = re_chunk.findall(next_line)
            if len(is_next_a_chunk) > 0:
                next_chunk = int(is_next_a_chunk[0], 16)
                curr_line.rstrip()
            else:
                curr_line = next_line                
                response += curr_line
        return response
        
    def read(self):
        re_chunk = re.compile(r'^([a-f|\d]+){1,4}\r\n')
        raw_response = ""
        in_buf = "\n".join(self.msg)

        raw_response = raw_response + in_buf

        while 1:
            try:
                in_buf = self.transport.recv(TCP_DEFAULT_FRAME_SIZE)
            except Exception, e:
                print e.message
            fa = re_chunk.findall(in_buf)
            raw_response += in_buf                
            if len(fa) > 0:
                if fa[0] == '0':
                    raw_response += in_buf                
                    break;
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
