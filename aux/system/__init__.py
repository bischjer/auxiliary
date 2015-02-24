#these imports should be kept in a system pool and only be instantiated once.

def get_system(systemjson):

    systemtype = systemjson.get('systemtype', False)
    if systemtype:
        if systemtype == 'TODO: do system lookup from this point, must include external modules, figure it out':
            print "do it"
    
    return None
