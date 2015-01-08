class SRDOperationCaller(object):
    def __init__(self, instance, operation):
        self.instance = instance
        self.operation = operation
                
    def __call__(self, kwargs={}):
        raise NotImplementedError()

#ServiceResourceDescription
class SRD(object):

    def __init__(self):
        self.__api_sources = list()
        self.__operations = list()
        self._s_types = list()

    # def __getattr__(self, attr):
    #     operation = [op for op in self.__operations if op.name == attr]
    #     if len(operation) > 0:
    #         return self.__operation_caller(self, operation[0])
    #     else:
    #         emsg = "%s object has no attribute '%s'" % (self.__class__.__name__, attr)
    #         raise AttributeError(emsg)

    def set_operation(self, operation):
        self.__operations.append(operation)
        
    def set_api_source(self, new_api_source_dsn):
        self.__api_sources.append(new_api_source_dsn)

    def get_api_sources(self):
        return self.__api_sources
    
    def update_api(self):
        raise NotImplementedError("update_api() not defined")
