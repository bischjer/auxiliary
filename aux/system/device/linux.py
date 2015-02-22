from aux.system.device.base import BaseDevice
from aux.authentication import BaseCredentials
from aux.api import ssh

class LinuxDevice(BaseDevice):
    def __init__(self, identifier, **kwargs):
        super(LinuxDevice, self).__init__(identifier)

        self.ssh = ssh
        # self.ssh.set_hostname(self.identifier)

