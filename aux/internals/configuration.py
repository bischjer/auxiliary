import sys        
import os
import logging
from optparse import OptionParser, OptionGroup
from aux import base_dir

def str2loglevel(option, opt_str, value ,parser):
    if value is not None:
        if "DEBUG"==value.upper():
            setattr(parser.values, option.dest, logging.DEBUG)
        elif "ERROR"==value.upper():
            setattr(parser.values, option.dest, logging.ERROR)
        elif "INFO"==value.upper():
            setattr(parser.values, option.dest, logging.INFO)
        elif "WARNING"==value.upper():
            setattr(parser.values, option.dest, logging.WARNING)
        else:
            setattr(parser.values, option.dest, logging.NOTSET)

class Configuration(object):
    def __init__(self):
        self.provision_optargs()

    def provision_optargs(self):
        usage = "usage: aux aux_file.py --option"
        parser = OptionParser(usage=usage)
        parser.add_option("--systems",
                          dest="systems",
                          type="string",
                          help="list of systems")
        parser.add_option("--config",
                          dest="configurationfile",
                          type="string")
        log_group = OptionGroup(parser, "Logging Options")
        log_group.add_option("-v", "--verbose",
                          dest="verbose",
                          action="store_true",
                          default=False,
                          help="verbose to console")
        log_group.add_option("--loglevel",
                          action="callback",
                          callback=str2loglevel,
                          dest="log_level",
                          type="string",
                          default=10,
                          help="[ NOTSET | ERROR | WARNING | INFO | DEBUG ]")
        log_group.add_option("--logconsolelevel",
                          action="callback",
                          callback=str2loglevel,
                          dest="log_console_level",
                          type="string",
                          default=None)
        log_group.add_option("--logfilelevel",
                          action="callback",                          
                          callback=str2loglevel,
                          dest="log_file_level",
                          type="string",
                          default=None)        
        log_group.add_option("--logdir",
                          dest="log_directory",
                          action="store",
                          default=os.path.abspath(os.path.join(base_dir(),
                                                               "..",
                                                               "logs")),
                          type="string")
        log_group.add_option("--logsrv",
                          dest="log_server",
                          type="string")

        tools_group = OptionGroup(parser, "Auxiliary Tools")
        tools_group.add_option("--create_plugin",
                               dest="plugincreator",
                               type="string",
                               help="[ service, device, protocol ]")
        
        parser.add_option("--engine",
                          dest="engine_type",
                          type="string")
        
        parser.add_option_group(log_group)
        parser.add_option_group(tools_group)
        self.options, self.args = parser.parse_args()

    def load_default_properties(self, properties_file):
        #TODO: get the setup from the aux.__init__ file
        pass
        
# print "sysargv", sys.argv
config = Configuration() if 'aux' in sys.argv[0] else None
