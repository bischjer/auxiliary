from datetime import datetime
import ConfigParser, os
import logging
from aux import base_dir

def start():
    config = ConfigParser.ConfigParser()
    try:
        config.readfp(open(os.path.join(base_dir(), 'aux.properties')))
    except IOError,e:
        pass

    
    # config.read(['aux.properties',
    #              os.path.expanduser('~/.aux/aux.properties')])
    # log_dir = config.get('log', 'directory')
    # log_lvl = config.get('log', 'level')
    # log_vrb = config.get('log', 'verbose')
    # print config.items
    log_dir = os.path.expanduser('~/.aux/logs/')
    if not os.path.exists(log_dir):
        os.mkdir(log_dir)
    logging.basicConfig(filename=os.path.join(log_dir,
                                              '%s-aux.log' % (datetime.strftime(datetime.now(), "%Y%m%d%H%M%S%f"))),
                        level=logging.DEBUG)


    
