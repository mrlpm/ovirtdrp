from __future__ import print_function

from functions_ovirt import *


def status(api, hosts):
    clear()
    local_no_hosts = len(hosts['local'])
    count_non_responsive = 0
    count_maintenance = 0
    for locate in 'local', 'remote':
        for host in hosts[locate]:
            status_host = status_one_host(api, host)
            if locate == 'local':
                if status_host == 'non_responsive':
                    count_non_responsive += 1
            elif locate == 'remote':
                if status_host == 'maintenance':
                    count_maintenance += 1
    if count_non_responsive == local_no_hosts:
        if count_maintenance > 0:
            return 1
        else:
            return 0
    else:
        return 0


def start():
    clear()
    print("Init")
    raw_input("Press Enter to continue...")


def main():
    config = read_config(file_config='config.yml')
    username = config['username']
    password = config['password']
    manager = config['manager']
    url_manager = 'https://' + manager
    hosts = config["Hosts"]

    '''
    print(username)
    print(password)
    print(manager)
    print(url_manager)
    print(platform.system())'''

    api = connect(manager_url=url_manager, manager_password=password, manager_username=username)

    while True:
        clear()
        menu()
        option = raw_input("Choice: ")

        if option == "2":
            break
        elif option == "1":
            if status(api=api, hosts=hosts):
                sub_menu()
                sub_option = raw_input("Choice: ")
                if sub_option == "2":
                    break
                elif sub_option == "1":
                    print("Initializing DRP")
                    for host in hosts['local']:
                        print("Fencing host {}".format(host))
                        if do_fence(api, host):
                            print("Fencing host {} OK".format(host))
                        print("Set Maintenance host {}".format(host))
                        if do_maintenance(api, host):
                            print("Maintenance host {} OK".format(host))
            else:
                print("Site A OK")
                print("Not Continue")
            raw_input("Press Enter to continue...")
        else:
            print("{} is not a valid option".format(option))
            raw_input("Press Enter to continue...")


if __name__ == '__main__':
    main()
