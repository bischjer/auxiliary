from aux.device.base import Device
from aux.authentication import BaseCredentials

class LinuxDevice(Device):
    def __init__(self, *args, **kwargs):
        Device.__init__(self, *args, **kwargs)
        Http = self.get_protocols().http.Http
        http_creds = self.get_http_credentials()
        self.http = self.backend.make_proxy(
            Http(ip=http_creds.ip,
                 username=http_creds.username,
                 password=http_creds.password,
                 port=http_creds.port)
            )

    def get_http_credentials(self):
        return BaseCredentials(ip=self.identifier,
                               username='',
                               password='',
                               port=80)
