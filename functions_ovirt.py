from ovirtsdk.api import API


def connect(rhevm_url=None, rhevm_username=None, rhevm_password=None):
    api = API(url=rhevm_url, username=rhevm_username, password=rhevm_password, insecure="True")
    return api


def status_one_host(api, name):
    alone_host = api.hosts.get(name)
    return alone_host.get_status().get_state()