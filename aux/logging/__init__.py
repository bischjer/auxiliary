from datetime import datetime
import ConfigParser, os
import logging

logger = None
summary = dict()
post_to_server = False

def start(defaultproperties='aux.properties'):
    global summary
    global logger
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

    logger = logging.getLogger('aux_all')
    logfile = os.path.join(logdir, logname)
    summary['logfolder'] = logdir
    fh = logging.FileHandler(filename=logfile)
    fh.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)
    logger.addHandler(fh)
    logger.addHandler(ch)
    summary['testsubject'] = list()

    
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
