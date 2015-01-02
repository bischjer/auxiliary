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
from aux.logging import LogController
from datetime import datetime
import json
from aux.internals.configuration import config
from aux.engine import engine_factory

logcontroller = LogController(config)

def run():

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
    #start engine
    engine = engine_factory('reactor')
    engine.start()
    #run
    # print config.options
    exec(script_to_run)
    #do teardown


__all__ = ['device',
           'plugin',
           'run']

def exit_hook():
    logcontroller.pprint_summary_on_exit()
sys.exitfunc = exit_hook
