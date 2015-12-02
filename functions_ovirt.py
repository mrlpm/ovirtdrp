from ovirtsdk.api import API
import yaml


def read_config(file_config):
    with open(file_config, 'r') as configuration:
        return yaml.load(configuration)


def connect(rhevm_url=None, rhevm_username=None, rhevm_password=None):
    api = API(url=rhevm_url, username=rhevm_username, password=rhevm_password, insecure="True")
    return api


def status_one_host(api, name):
    alone_host = api.hosts.get(name)
    return alone_host.get_status().get_state()
