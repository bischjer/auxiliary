from aux.scriptengine import ScriptEngine
import paramiko
from aux.protocol.http import HTTPClient

def run(engine, func, *args, **kwargs):
    engine.start()
    try:
        func(*args, **kwargs)
    finally:
        results = engine.stop()
    return results

ssh = paramiko.SSHClient()
# ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
http = HTTPClient()






