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
from aux.internals import plugin_creator_routine
from aux.engine import engine_factory

logcontroller = None
configuration = None


def run():
    from aux.internals.configuration import config
    global configuration 
    global logcontroller
    configuration = config
    if config.options.plugincreator is not None:
        plugin_creator_routine(config.options.plugincreator,
                               config.args)

    ## - read config file
    try:
        config.load_default_properties()
    except Exception, e:
        print 'Falling back to default settings.'
        print e.message

    ## - initiate logger        
    logcontroller = LogController(config)
            
    ## - Setup
    logcontroller.summary['test'] = sys.argv[0]
    logcontroller.summary['started'] = datetime.now()
    logcontroller.summary['testsubject'] = config.options.systems

    scripts_as_args = [script for script in config.args if '.py' in script]
    if len(scripts_as_args) != 1:
        logcontroller.runtime.error('Script args error')
        sys.exit(1)
    ## - initiate backend
    ## -- start engine
    engine = engine_factory('reactor', config)
    engine.start()
    ## - verify systems
    print config.options.systems        
    ## - run
    execfile(scripts_as_args[0])
    ## - do teardown
    engine.stop()
    logcontroller.summary['ended'] = datetime.now()
    
__all__ = ['device',
           'plugin',
           'run']

def exit_hook():
    if logcontroller is not None:
        logcontroller.pprint_summary_on_exit()
sys.exitfunc = exit_hook
