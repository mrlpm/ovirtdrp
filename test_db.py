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
for lunsa, lunsb in itertools.izip(lun_local, lun_remote):
    print("changing %s by %s " % (lunsa, lunsb))
    lunx = db.storage_server_connections.filter_by(iqn=lunsa).one()
    lunx.iqn = lunsb
    db.commit()
    print("port: %s iqn: %s" % (lunx.port, lunx.iqn))

print("#######################")

print(lun_local[0])

#####
