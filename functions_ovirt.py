from ovirtsdk.api import API
import yaml


def read_config(file_config):
    with open(file_config, 'r') as configuration:
        return yaml.load(configuration)


def connect(manager_url, manager_password, manager_username):
    api = API(url=manager_url, username=manager_username, password=manager_password, insecure="True")
    return api


def status_one_host(api, name):
    alone_host = api.hosts.get(name)
    return alone_host.get_status().get_state()
