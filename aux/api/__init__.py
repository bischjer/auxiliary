from aux.scriptengine import ScriptEngine
import paramiko

from aux.protocols.http import HTTPRequest

def run(engine, func, *args, **kwargs):
    engine.start()
    try:
        func(*args, **kwargs)
    finally:
        results = engine.stop()
    return results

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

class _http(object):

    def get(self, url):
        HTTPRequest()
        print url

    def post(self, url, headers={}):
        print url

    def put(self, url):
        print url

http = _http()

