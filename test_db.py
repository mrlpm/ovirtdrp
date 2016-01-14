from __future__ import print_function
from functions_ovirt import read_config
import sqlsoup

db_string = 'postgresql+psycopg2://engine:ZvPT0kdDB8qUaWtRnYcmz3@nrhevm.itmlabs.local/engine'
db = sqlsoup.SQLSoup(db_string)

for iscsi in db.storage_server_connections.filter(db.storage_server_connections.iqn != None):
    print("iqn: %s -- connection: %s " % (str(iscsi.iqn), str(iscsi.connection)))

config = read_config(file_config='config.yml')
luns = config['luns']
portals = config['mpath']

#####
# modify DB
import itertools

lun_local = luns['lunIDA']
lun_remote = luns['lunIDB']
portals_local = portals['iscsiportalA']
portals_remote = portals['iscsiportalB']
i=0
#for lunsa, lunsb in itertools.izip(lun_local, lun_remote):
    #print("changing %s by %s " % (lunsa, lunsb))
    #print(db.storage_server_connections.filter_by(iqn=lunsa))
    #lunx = db.storage_server_connections.filter_by(iqn=lunsa).all()
    #i += 1
    #print(i)
    #print(lunx)

for portala, portalb in itertools.izip(portals_local, portals_remote):
    #print(db.storage_server_connections.filter_by(connection=portala))
    portalx = db.storage_server_connections.filter_by(connection=portala).all()
    #print(portalx)
    print("#######################")

print(db.storage_server_connections.filter_by(connection='192.168.113.254'))
dos = db.storage_server_connections.filter_by(connection='192.168.113.254').one()
print(dos)
#####
