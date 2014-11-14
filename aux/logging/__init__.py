from datetime import datetime
import ConfigParser, os
import logging
from aux import base_dir

logger = None

def start(defaultproperties='aux.properties'):
    config = ConfigParser.ConfigParser()
    home = os.path.expanduser("~")
    auxwdir = ".aux"
    propertiesfile = os.path.join(home, auxwdir, defaultproperties)    
    try:
        config.readfp(open(propertiesfile, "r"))
    except IOError, e:
        print e

    # config.read(['aux.properties',
    #              os.path.expanduser('~/.aux/aux.properties')])
    # log_dir = config.get('log', 'directory')
    # log_lvl = config.get('log', 'level')
    # log_vrb = config.get('log', 'verbose')
    # print config.items
    
    logdir = os.path.join(home,
                          auxwdir,
                          "logs",
                          datetime.strftime(datetime.now(), "%Y%m%d-%H%M%S%f"))
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logname = 'aux.log'
    global logger
    logger = logging.getLogger('aux_all')
    fh = logging.FileHandler(filename=os.path.join(logdir, logname))
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)

    
def info(message):
    logger.info(message)

def debug(message):
    logger.debug(message)

def error(message):
    logger.error(message)

def warning(message):
    logger.warning(message)

def critical(message):
    logger.critical(message)
