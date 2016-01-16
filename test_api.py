from __future__ import print_function

import sys
import os
from time import sleep
from progress.spinner import Spinner
from functions_ovirt import connect, read_config


path = os.path.dirname(os.path.abspath(__file__))
config = read_config(file_config=path + '/config.yml')
manager = config['manager']
url_manager = 'https://' + manager
username = 'admin@internal'
password = 'S0p0rt32015.'
api = connect(url_manager,password,username)


clusters = api.clusters.list()
hosts = api.hosts.list()

#for data_center in data_centers:
#    print("DataCenter Name: %s Status: %s" % (data_center.name, data_center.get_status().get_state()))


for cluster in clusters:
    print("Cluster Name: %s " % (cluster.name))


def spm_status(host):
    if host.storage_manager.valueOf_ == 'true':
            return 1
    else:
            return 0

spinner = Spinner("Waiting ")
terminate = 0
while terminate != '1':
    data_centers = api.datacenters.list()
    count = 0
    for data_center in data_centers:
        if data_center.get_status().get_state() == 'up':
            count += 1
        if count == len(data_centers):
            terminate = 1
    if terminate == 1:
        break
    spinner.next()

sys.stdout.flush()
api.disconnect()
print("\nFinished...")