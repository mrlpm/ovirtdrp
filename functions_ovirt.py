import platform
import subprocess
import sqlsoup
from ovirtsdk.api import API
from ovirtsdk.xml import params
from ovirtsdk.infrastructure.errors import RequestError
import yaml
import os


def read_config(file_config):
    with open(file_config, 'r') as configuration:
        return yaml.load(configuration)


def connect(manager_url, manager_password, manager_username):
    try:
        api = API(url=manager_url, username=manager_username, password=manager_password, insecure="True")
        return api
    except RequestError as e:
        print(e.reason)
        exit(-1)


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
        1.- Start
        2.- Exit
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
            print("Host ({}) {} state {}".format(locate, host, status_host))
            if locate == 'local':
                if status_host != 'up':
                    count_non_responsive += 1
            elif locate == 'remote':
                if status_host == 'maintenance':
                    count_maintenance += 1
    if count_non_responsive > 0:
        if count_maintenance > 0:
            sad_face()
            return 1
        else:
            print 'No remote hosts ready for operation'
            print 'Power up and set maintenance mode for remote hosts'
        sad_face()
        exit(1)
        return 1
    else:
        if count_maintenance <= 0:
            print 'Something is not right, remote host must be in Maintenance mode'
            print 'Remote Site is not ready to start process - FIX and try again'
            sad_face()
            exit(2)
        else:
            happy_face()
            print("Everything seems to be fine")
            return 0


def change_state_to(api, name):
    try:
        api.hosts.get(name).activate()
    except ValueError:
        return ValueError


def modify_db(db_user, db_password, database, manager, lunsArray, portalsArray):
    db_string = 'postgresql+psycopg2://' + db_user + ':' + db_password + '@' + manager + '/' + database
    db = sqlsoup.SQLSoup(db_string)
    change_luns(luns=lunsArray, portals=portalsArray, db=db)
    db.commit()


def change_luns(luns, portals, db):
    try:
        import itertools
        lun_local = luns['lunIDA']
        lun_remote = luns['lunIDB']
        portals_local = portals['iscsiportalA']
        portals_remote = portals['iscsiportalB']
        for lunsa, lunsb in itertools.izip(lun_local, lun_remote):
            lunx = db.storage_server_connections.filter_by(iqn=lunsa).one()
            lunx.iqn = lunsb
        for portala, portalb in itertools.izip(portals_local, portals_remote):
            portalx = db.storage_server_connections.filter_by(connection=portala).one()
            portalx.connection = portalb
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


if __name__ == "__main__":
    print("This file is intended to be used as a library of functions and it's not expected to be executed directly")
