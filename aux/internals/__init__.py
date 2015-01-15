

def plugin_creator_routine(plugincreator, arguments):
    # print plugincreator, arguments    
    if 'service' in plugincreator:
        if len(arguments) > 0:
            packagename = "_".join(['aux', 'service', arguments[0]])
            print packagename
        os.system('paster create -t basic_package -o %s' % base_dir()+"/..")
        sys.exit(0)
    elif 'device' in plugincreator:
        if len(arguments) > 0:
            packagename = "_".join(['aux', 'device', arguments[0]])
            print packagename
        os.system('paster create -t basic_package -o %s' % base_dir()+"/..")
        sys.exit(0)
    elif 'protocol' in plugincreator:
        if len(arguments) > 0:
            packagename = "_".join(['aux', 'protocol', arguments[0]])
            print packagename
        os.system('paster create -t basic_package -o %s' % base_dir()+"/..")
        sys.exit(0)
