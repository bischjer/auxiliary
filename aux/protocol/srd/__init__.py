

class SRD(object):
    
    def __init__(self, url):
        self.url = url


    def __attrMethod(self, method):
        class MethodCaller(object):
            def __init__(self, instance, method):
                self.instance = instance
                self.method = method

            def __call__(self, kwargs={}):
                request_json = dict()


                return "NOT IMPLEMENTED"
        return MethodCaller(self, method)

    def __getattr__(self, attr):
        method = [op for op in self.__operations if op.name == attr]
        if len(method) > 0:
            return self.__attrMethod(method[0].name)
        else:
            emsg = "%s object has no attribute '%s'" % (self.__class__.__name__, attr)
            raise AttributeError(emsg)
