from base import BaseSystem

#TODO: obviously this is just thrown together
class Service(BaseSystem):
    def __init__(self, hostname):
        super(Service, self).__init__(hostname)
        self.hostname = hostname

class Device(BaseSystem):
    def __init__(self, hostname):
        super(Service, self).__init__(hostname)
        self.hostname = hostname
