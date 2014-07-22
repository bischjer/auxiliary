from aux.scriptengine import ScriptEngine
import paramiko
from aux.protocol.http import HTTPClient
import httplib2

def run(engine, func, *args, **kwargs):
    engine.start()
    try:
        func(*args, **kwargs)
    finally:
        results = engine.stop()
    return results

ssh = paramiko.SSHClient()
#ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
http = HTTPClient()




