from aux.system.base import BaseSystem
from aux.authentication import BaseCredentials
from aux.api import ssh

class LinuxDevice(BaseSystem):
    def __init__(self, identifier):
        super(LinuxDevice, self).__init__(identifier)

        self.ssh = ssh
        # self.ssh.set_hostname(self.identifier)

