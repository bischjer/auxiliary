
class DefaultController(object):

    def __init__(self, disposition, raw_body):
        self.data = raw_body

    def handle(self):
        return self.data

class ZIPController(object):

    def __init__(self, disposition, raw_body):
        self.disposition = disposition
        self.data = raw_body

    def handle(self):
        tmp_dir = "/tmp/aux"
        
        return self.data


def mimeFactory(headers):
    content_type = headers.get('Content-Type', None)
    if content_type != None:
        if 'application/zip' in content_type:
            return ZIPController
    return DefaultController
