import sys
from optparse import OptionParser 

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
                      
