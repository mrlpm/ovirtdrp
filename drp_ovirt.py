from __future__ import print_function
from functions_ovirt import connect, status_one_host, read_config


def main():
    config = read_config(file_config='config.yml')
    username = config['username']
    password = config['password']
    manager = config['manager']
    url_manager = 'https://' + manager
    hosts = config["Hosts"]

    print(username)
    print(password)
    print(manager)
    print(url_manager)
    print(hosts["local"])
    print(hosts["remote"])

    api = connect(manager_url=url_manager, manager_password=password, manager_username=username)
    print(status_one_host(api, hosts["remote"]["host1"]))


if __name__ == '__main__':
    main()
