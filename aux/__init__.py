import sys
import os
import device
import plugin
from optparse import OptionParser 
import pkg_resources
import aux

print "-"*70

def version():
    return pkg_resources.get_distribution(aux.__package__.title()).version

def base_dir():
    return os.path.abspath(os.path.dirname(aux.__file__))

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

def exit_hook():
    print "-"*70
    print "- AUX %s - Summary" % version()
    print "-"*70
    print "-"
    print "-"*70
sys.exitfunc = exit_hook
