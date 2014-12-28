from aux.device.base import Device
from aux.authentication import BaseCredentials
from aux.protocol.ssh import SSHClient

class LinuxDevice(Device):
    def __init__(self, identifier, **kwargs):
        Device.__init__(self, identifier)

        self.ssh = SSHClient()
        self.ssh.set_hostname(self.identifier)
