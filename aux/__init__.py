import sys
import os
import device
import plugin
import pkg_resources

def version():
    return pkg_resources.get_distribution(aux.__package__.title()).version

def base_dir():
    return os.path.abspath(os.path.dirname(aux.__file__))

import aux
from aux.api import http
from aux.logging import LogController
from datetime import datetime
import json

logcontroller = None

def plugin_creator_routine(plugincreator, arguments):
    if 'service' in plugincreator:
        # print plugincreator, arguments
        if len(arguments) > 0:
            packagename = "_".join(['aux', 'service', arguments[0]])
            # print packagename # TODO: template
        os.system('paster create -t basic_package -o %s' % base_dir()+"/..")
        sys.exit(0)
    elif 'device' in plugincreator:
        pass
        sys.exit(0)
    elif 'protocol' in plugincreator:
        pass
        sys.exit(0)

def run():
    from aux.internals.configuration import config

    if config.options.plugincreator is not None:
        plugin_creator_routine(config.options.plugincreator,
                               config.args)
    
    logcontroller = LogController(config)
    #read config file
    mock_config_file = """
proxy: localhost:5791
log_directory: logs/
"""
    ## Setup
    logcontroller.summary['test'] = sys.argv[0]
    logcontroller.summary['started'] = datetime.now()
    logcontroller.summary['testsubject'] = list()
    

        
    scripts_as_args = [script for script in config.args if '.py' in script]
    if len(scripts_as_args) != 1:
        logcontroller.runtime.error('Script args error')
        sys.exit(1)
    else:
        script_to_run = open(scripts_as_args[0], "r").read().strip()
    #initiate backend
    #initiate logger
    #verify endpoints
    print config.options.systems
    
    #run
    exec(script_to_run)
    #do teardown


__all__ = ['device',
           'plugin',
           'run']

def exit_hook():
    if logcontroller is not None:
        logcontroller.pprint_summary_on_exit()
sys.exitfunc = exit_hook
