from aux.protocols.connection import Connection
from aux.protocols.http.http import (HTTP, HTTPClient, HTTPRequest,
                                     HTTPResponse, CRLF, HTTP_RESPONSE_CODES)




#TODO: deprecated:remove
# class HTTPResponse(HTTPMessage):
#     re_HTTP_SIGN = re.compile(r'HTTP\/(\d\.\d)\s(\d{3})\s')
    
#     def __init__(self, raw_response):
#         self.raw_response = raw_response
#         self.headers = ""
#         self.body = ""
#         self.version = None
#         self.code = None
#         self.parse_raw_response()
        
#     def parse_raw_response(self):
#         body_flag = False
#         self.version, self.code = self.re_HTTP_SIGN.findall(self.raw_response.split("\n")[0])[0]
#         for line in self.raw_response.split("\n")[1:]:
#             if len(line) == 0:
#                 body_flag = True
#             if body_flag:
#                 self.body = self.body+"\n"+line
#             else:
#                 self.headers = self.headers+"\n"+line

#         self.body = self.body.strip()
                

