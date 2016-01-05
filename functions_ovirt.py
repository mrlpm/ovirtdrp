import platform
import subprocess
import sqlsoup
from ovirtsdk.api import API
from ovirtsdk.xml import params
import yaml
import os


def read_config(file_config):
    with open(file_config, 'r') as configuration:
        return yaml.load(configuration)


def connect(manager_url, manager_password, manager_username):
    api = API(url=manager_url, username=manager_username, password=manager_password, insecure="True")
    return api


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
        exit(-1)


def menu():
    print("""
        1.- Hosts Status
        2.- Exit
        """)


def sub_menu():
    print("""
        1.- Iniciar
        """)


def do_fence(api, name):
    try:
        api.hosts.get(name).fence(action=params.Action(fence_type='manual'))
        return 1
    except ValueError:
        return ValueError


def do_maintenance(api, name):
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
    count_non_responsive = 0
    count_maintenance = 0
    for locate in 'local', 'remote':
        for host in hosts[locate]:
            status_host = status_one_host(api, host)
            print("Host {} state {}".format(host, status_host))
            if locate == 'local':
                if status_host != 'up':
                    count_non_responsive += 1
            elif locate == 'remote':
                if status_host == 'maintenance':
                    count_maintenance += 1
    if count_non_responsive > 0:
        if count_maintenance > 0:
            return 1
        else:
            return 0
    else:
        return 0


def change_state_to(api, name):
    try:
        api.hosts.get(name).activate()
    except ValueError:
        return ValueError


def modify_db(db_user, db_password, database, manager):
    db_string = 'postgresql+psycopg2://' + db_user + ':' + db_password + '@' + manager + '/' + database
    db = sqlsoup.SQLSoup(db_string)
    db.execute("UPDATE storage_server_connections SET iqn='iqn.2015-12.local.itmlabs:lun01adrp' WHERE iqn='iqn.2015-12.local.itmlabs:lun01a' ")
    db.execute("UPDATE storage_server_connections SET connection='192.168.113.254' WHERE connection='192.168.113.254'")
    db.commit()
