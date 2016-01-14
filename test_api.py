from __future__ import print_function

import sys
import os

from time import sleep

from functions_ovirt import connect, read_config
from tqdm import tqdm

path = os.path.dirname(os.path.abspath(__file__))
config = read_config(file_config=path + '/config.yml')
manager = config['manager']
url_manager = 'https://' + manager
username = 'admin@internal'
password = 'S0p0rt32015.'
api = connect(url_manager,password,username)

data_centers = api.datacenters.list()
clusters = api.clusters.list()
hosts = api.hosts.list()

for data_center in data_centers:
    print("DataCenter Name: %s Status: %s" % (data_center.name, data_center.get_status().get_state()))
    sys.stdout.flush()

for cluster in clusters:
    print("Cluster Name: %s " % (cluster.name))
    sys.stdout.flush()
    #print("Cluster Name: %s Status: %s" % (cluster.name, cluster.get_status().get_state()))

def spm_status(hosts):
    for host in hosts:
        response = list()
        if host.storage_manager.valueOf_ == 'true':
            response.append(host)
            response.append(1)
            return response
        else:
            response.append(host)
            response.append(0)
            return response
while True:
    spm = spm_status(hosts=hosts)[1]
    spm_host = spm_status(hosts=hosts)[0]
    if spm == 1:
        break
print(spm)
print(spm_host.name)