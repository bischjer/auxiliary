import sys
import device
import plugin
from optparse import OptionParser 
import pkg_resources
import aux

def version():
    return pkg_resources.get_distribution(aux.__package__.title()).version


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
