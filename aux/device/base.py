class Device(object):
    def __init__(self, identifier, scriptengine, **extra_kwargs):
        self.identifier = identifier
        self.scriptengine = scriptengine
        self.backend = scriptengine.backend

    def get_protocols(self):
        '''
        Returns the module containing protocol implementation
        '''
        return self.backend.protocols
