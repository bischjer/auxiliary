from aux.system import get_system

# systemjson = {"hostname": "192.168.0.193",
#                        "systemtype": "SSPService",                       
#                        # "systemtype": "aux.system.service.ext.kezzler.SSPService", #TODO: should probably specify
#                        "username": "rduser",
#                        "password": "yggdrasil"}
# ssp = get_system(systemjson)

# print 'ssp', ssp
# ssp.set_scheme('http://')
# ssp.rest.set_credentials((systemjson.get('username'),
#                           systemjson.get('password')))



# print dir(ssp.rest)
# ssp.rest.set_api_source("/ssp/api/kcengine-ws.all.json")
# ssp.rest.set_api_source("/ssp/api/compass-ws.all.json")
# ssp.rest.update_api()

# print ssp.rest.listPackageTypes({})


# systemjson = {"hostname": "192.168.0.130",
#               "systemtype": "LinuxDevice",
#               "username": "rduser",
#               "password": "yggdrasil"}
# vmserver = get_system(systemjson)
vmserver = get_system({"systemtype": "LinuxDevice"})

print vmserver
