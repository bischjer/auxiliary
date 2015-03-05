# from aux.internals.pluginhook import PluginImporter
import sys
import os
import imp
import device
import service

#these imports should be kept in a system pool and only be instantiated once.

def get_system(systemjson=None, systemtype=None):
    print systemjson
    print systemtype

    ## NEED TO LOOKUP IN system.device and system.service and aux_device and aux_service
    devicemodule = os.path.dirname(device.__file__)
    servicemodule = os.path.dirname(service.__file__)
    
    r_filters = ['ext', '__init__.py', '__init__.pyc']
    print [r for r in os.listdir(devicemodule) if r not in r_filters]
    print [r for r in os.listdir(servicemodule) if r not in r_filters]

    
    e_d = [p for p in sys.path if 'aux_device_' in p]
    e_s = [p for p in sys.path if 'aux_service_' in p]

    
    print os.path.split(e_s[0])
    extservices = [imp.find_module( os.path.split(m)[1] )[1] for m in e_s]
    print [r for r in os.listdir(extservices[0])]
    
    
    # print sys.path
    # pir = PluginImporter(['aux_service_'],__name__)
    # print pir.find_module('kezzler')
    # print [a for a in sys.path if 'aux_service_' in a]
    
    # systemtype = systemjson.get('systemtype', False)
    # if systemtype:
    #     if systemtype == 'TODO: do system lookup from this point, must include external modules, figure it out':
    #         print "do it"
    
    return None
