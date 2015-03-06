# from aux.internals.pluginhook import PluginImporter
import sys
import os
import imp
import device
import service

#these imports should be kept in a system pool and only be instantiated once.

def find_systemtype(systemtype):
    ## NEED TO LOOKUP IN system.device and system.service and aux_device and aux_service
    devicemodule = os.path.dirname(device.__file__)
    servicemodule = os.path.dirname(service.__file__)

    # r_filters = ['ext', '__init__.py', '__init__.pyc']
    print systemtype
    print [r for r in os.listdir(devicemodule) if r]
    print [r for r in os.listdir(servicemodule) if r]
    
    # e_d = [p for p in sys.path if 'aux_device_' in p]

    #find service
    e_s = [p for p in sys.path if 'aux_service_' in p]
    # print e_d
    # print e_s

    print e_s
    
    for s in e_s:
        # print os.path.split(s)
        
        modulepath = imp.find_module(os.path.split(s)[1])[1]
        # extservices = [imp.find_module( os.path.split(m)[1] )[1] for m in e_s]

        # print modulepath
        files = [os.path.join(modulepath,r) for r in os.listdir(modulepath)]
        foundfile = None
        for f in files:
            fp = open(f,'r')
            if systemtype in fp.read():
                foundfile = f
                break

        print 'foundfile', foundfile
            
        if foundfile is not None:
            # print foundfile
            module, fx = os.path.split(foundfile)
            mod1 = os.path.split(module)[1]
            fil1 = fx.split('.')[0]
            print '*'*20
            print foundfile
            print module
            print mod1
            print '*'*20            
            if 'aux_' in module:
                modlist = mod1.split('_')
                modlist.insert(1,'system')
                modlist.insert(3, 'ext')            
            # modlist.append(fil1)
            # print ".".join(modlist)
            # print fil1
            # print '*'*20            
            # print imp.find_module(mod1)

            prt = imp.load_module(systemtype, open(foundfile), module, ('','',5))
            return eval("prt.%s" % systemtype)

def get_system(systemjson):
    '''
    systemjson = {"hostname":"some.name.com.or.ip.10.0.0.1",
                  "systemtype": "MyDevice",
                  "username": "username",
                  "password": "password",
                  "properties": [{"a":"2"}]}
    '''

    
    if systemjson.get('hostname') is not None:
        #target with specific hostname        
        if systemjson.get('systemtype') is not None:
            hostname = systemjson.get('hostname')
            systemtype = systemjson.get('systemtype')
            return find_systemtype(systemtype)(systemjson.get('hostname'))
        else:
            #doprobeoftype
            #TODO: this is a bit complex, the probe should be in systemdefinition
            return None
    else:
        if systemjson.get('systemtype') is not None:
            return None

    
    return None
