from aux.scriptengine import ScriptEngine
import paramiko
from aux.protocols.http import HTTPClient

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



