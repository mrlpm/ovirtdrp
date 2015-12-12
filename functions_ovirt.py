import platform
import subprocess

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
        return ValueError


def ping(host_alive):
    host_alive = host_alive
    command = subprocess.call("ping -c 1 %s" % host_alive, shell=True, stdout=open('/dev/null', 'w'), stderr=subprocess.STDOUT)
    if command == 0:
        return 1
    else:
        return 0