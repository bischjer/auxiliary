import sys
import os
import device
import plugin
from optparse import OptionParser 
import pkg_resources
def version():
    return pkg_resources.get_distribution(aux.__package__.title()).version

def base_dir():
    return os.path.abspath(os.path.dirname(aux.__file__))

import aux
from aux.api import http
from aux.logging import summary
from datetime import datetime
import json

print "-"*70
summary['test'] = sys.argv[0]
summary['started'] = datetime.now()


def script_runner():
    #read config file
    mock_config_file = """
proxy: localhost:5791
log_directory: logs/
"""
    
    #initiate backend
    #initiate logger
    #verify endpoints
    #do setup
    #run
    #do teardown

    
    print "running"
    print sys.argv

    parser = OptionParser()
    parser.add_option("-v", "--verbose",
                      dest="verbose",
                      action="store_true",
                      default=False,
                      help="verbosity in console")

    (options, args) = parser.parse_args()
    print options, args
                      


__all__ = ['device',
           'plugin',
           'script_runner']

def post_to_server(summary):
    serverendpoint = 'http://192.168.0.135:8080/api/test/result'
    json_data = {'started' : str(summary.get('started')),
                 'ended' : str(summary.get('ended')),
                 'test' : summary.get('test'),
                 'success' : False,
                 'testsubject' : str(summary.get('testsubject')),
                 'tester' : 'auxscript',
                 'logfolder' : summary.get('logfolder')}
    headers = {'Host': '192.168.0.135',
               'User-Agent':'Aux/0.1 (X11;Ubuntu;Linux x86_64;rv:24.0)',
               'Accept':'*/*'}
    print headers
    headers.update(http.basic( ('tester', 'tester')))
    print json_data
    print http.post(serverendpoint,
              headers=headers,
              body=json.dumps(json_data))
    

def exit_hook():
    summary['ended'] = datetime.now()

    # post_to_server(summary)
    
    print "-"*70
    print "- AUX %s - Summary" % version()
    print "-"*70
    for key in summary.keys():
        print "- %s: %s" % (key, summary[key])
    print "-"*70
sys.exitfunc = exit_hook
