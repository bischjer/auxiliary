from aux.protocol.http.https import HTTPSConnection
from aux.protocol.soap.wsdl import WSDL
from urlparse import urlparse


class Soap(HTTPSConnection):

    def __init__(self, url):
        super(Soap, self).__init__(url)

        
def create_wsdl(wsdl_string):
    return WSDL(wsdl_string)

def connection(url):
    return Soap(url)


request = '''
POST https://aux.protojour.com/ws/test-ws HTTP/1.1
Accept-Encoding: gzip,deflate
Content-Type: text/xml;charset=UTF-8
SOAPAction: ""
Authorization: Basic abcdefghijklmnopqrstuvwx
Content-Length: 352
Host: aux.protojour.com
Connection: Keep-Alive
User-Agent: Apache-HttpClient/4.1.1 (java 1.5)

<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns="test" xmlns:com="test">
   <soapenv:Header/>
   <soapenv:Body>
      <ns:ListSomething max="25">
      </ns:ListSomething>
   </soapenv:Body>
</soapenv:Envelope>
'''

response = '''
HTTP/1.1 200 OK
Server: nginx/1.5.4
Date: Wed, 12 Feb 2014 09:58:13 GMT
Content-Type: text/xml;charset=utf-8
Content-Length: 4734
Connection: keep-alive
Set-Cookie: JSESSIONID=oijoij6E0C7479C4CF531A5842241F47; Path=/; HttpOnly
X-Request-Received: 1392199092003
Accept: text/xml, text/html, image/gif, image/jpeg, *; q=.2, */*; q=.2
SOAPAction: ""
X-Src-Nginx: aux.protojour.com

<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
<SOAP-ENV:Header/><SOAP-ENV:Body></SOAP-ENV:Body></SOAP-ENV:Envelope>
'''
