
class BaseSystem(object):
    def __init__(self, identifier):
        self.identifier = identifier

        
class BaseDevice(BaseSystem):
    
    def __init__(self, identifier):
        super(BaseDevice, self).__init__(identifier)
