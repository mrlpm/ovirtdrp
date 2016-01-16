from __future__ import print_function

import platform
import subprocess
import sqlsoup
from ovirtsdk.api import API
from ovirtsdk.xml import params
from ovirtsdk.infrastructure.errors import RequestError
import yaml
import os
import sys


def read_config(file_config):
    with open(file_config, 'r') as configuration:
        return yaml.load(configuration)


def connect(manager_url, manager_password, manager_username):
    try:
        api = API(url=manager_url, username=manager_username, password=manager_password, insecure="True")
        return api
    except RequestError as e:
        print(e.reason)
        sys.exit(-1)


def status_one_host(api, name):
    alone_host = api.hosts.get(name)
    return alone_host.get_status().get_state()


def clear():
    if platform.system() == "Linux":
        os.system('clear')
    elif platform.sytem() == "Windows":
        os.system('cls')
    else:
        print("Not Supported Operating System")
        sys.exit(-1)


def menu():
    print("""
        1.- Status
        2.- Exit
        """)


def sub_menu():
    print("""
        1.- Start
        2.- Exit
        """)


def do_fence_host(api, name):
    try:
        api.hosts.get(name).fence(action=params.Action(fence_type='manual'))
        return 1
    except ValueError:
        return ValueError


def do_maintenance_host(api, name):
    try:
        api.hosts.get(name).deactivate()
        return 1
    except ValueError:
        print(ValueError)
        return ValueError


def ping(host_alive):
    host_alive = host_alive
    command = subprocess.call("ping -c 1 %s" % host_alive, shell=True, stdout=open('/dev/null', 'w'),
                              stderr=subprocess.STDOUT)
    if command == 0:
        return 1
    else:
        return 0


def status(api, hosts):
    clear()
    count_local_not_up = 0
    remote_count_maintenance = 0
    count_local_up = 0
    for locate in 'local', 'remote':
        for host in hosts[locate]:
            status_host = status_one_host(api, host)
            print("Host (%s) %s state %s" % (locate, host, status_host))
            if locate == 'local':
                if status_host != 'up':
                    count_local_not_up += 1
                elif status_host == 'up':
                    count_local_up += 1
            elif locate == 'remote':
                if status_host == 'maintenance':
                    remote_count_maintenance += 1
    datacenter_status(api)
    if count_local_up > 0:
        print('All Host must be in Maintenance status, to start controlled DRP process')
        return 0
    if count_local_not_up > 0:
        if remote_count_maintenance == len(hosts['remote']):
            return 1
        else:
            print('Remote hosts not ready for operation')
            print('Power up and set maintenance mode for remote hosts')
            return 0


def do_activate_host(api, name):
    try:
        api.hosts.get(name).activate()
    except ValueError:
        return ValueError


def update_connections(db_user, db_password, database, manager, lunsArray, portalsArray):
    db_string = 'postgresql+psycopg2://' + db_user + ':' + db_password + '@' + manager + '/' + database
    db = sqlsoup.SQLSoup(db_string)
    change_iscsi(luns=lunsArray, portals=portalsArray, db=db)
    db.commit()
    return 1


def change_iscsi(luns, portals, db):
    try:
        import itertools
        iqn_local = luns['lunIDA']
        iqn_remote = luns['lunIDB']
        portals_local = portals['iscsiportalA']
        portals_remote = portals['iscsiportalB']
        for iqn_local_a, iqn_local_b in itertools.izip(iqn_local, iqn_remote):
            iqns = db.storage_server_connections.filter_by(iqn=iqn_local_a).all()
            for iqn in iqns:
                iqn.iqn = iqn_local_b
            print("Change %s for %s OK" % (iqn_local_a,iqn_local_b))

        for portal_a, portal_b in itertools.izip(portals_local, portals_remote):
            portal_x = db.storage_server_connections.filter_by(connection=portal_a).all()
            for one_portal in portal_x:
                one_portal.connection = portal_b
            print("Change portal: %s for portal: %s OK" % (portal_a, portal_b))
        db.commit()
        return 1
    except ValueError:
        return ValueError


def get_local_hosts(api, remote):
    host_lists = api.hosts.list()
    local_hosts = []
    for h in host_lists:
        if h.get_name() not in remote:
            local_hosts.append(h.get_name())
    return local_hosts


def sad_face():
    print('  _________\n /         \\\n |  X   X  |\n |    +    |\n | /\\/\\/\\/ |\n \\_________/');


def happy_face():
    print('  _________\n /         \\\n |  () ()  |\n |    -    |\n |  \\___/  |\n \\_________/');


def decrypt(cipher_password):
    import base64
    not_b64 = base64.b64decode(cipher_password)
    key_encode, pass_encode = not_b64.split('@')
    password_clear_text = base64.b64decode(pass_encode)
    return password_clear_text


def spm_status(host):
    if host.storage_manager.valueOf_ == 'true':
        return 1
    else:
        return 0

def datacenter_status(api):
    data_centers = api.datacenters.list()
    for data_center in data_centers:
        datacenter_state = data_center.get_status().get_state()
        print("Datacenter: %s status: %s" % (data_center.name, datacenter_state))

def wait_datacenter(api):
    dc_up = list()
    while True:
        data_centers = api.datacenters.list()
        for data_center in data_centers:
            datacenter_state = data_center.get_status().get_state()
            datacenter_name = data_center.name
            if datacenter_state == 'up':
                if datacenter_name not in dc_up:
                    dc_up.append(datacenter_name)
                    print("Datacenter: %s status: %s" % (datacenter_name, datacenter_state))
        if len(dc_up) == len(data_centers):
            break

def drp_finish(api):
    import sys
    print("Waiting Datacenters state up")
    wait_datacenter(api)
    api.disconnect()
    print("\nFinished...")
    sys.exit(0)


if __name__ == "__main__":
    print("This file is intended to be used as a library of functions and it's not expected to be executed directly")
