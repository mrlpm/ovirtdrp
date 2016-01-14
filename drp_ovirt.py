from __future__ import print_function

import time
from getpass import getpass

from functions_ovirt import *


def main():
    config = read_config(file_config='config.yml')
    manager = config['manager']
    url_manager = 'https://' + manager
    hosts = config["Hosts"]

    database = decrypt(config['database'])
    db_user = decrypt(config['userDatabase'])
    db_password = decrypt(config['passDatabase'])
    iscsi_luns = config['luns']
    iscsi_portals = config['mpath']

    if ping(manager):
        api = connect(manager_url=url_manager, manager_password=password, manager_username=username)
        print("Please enter username for %s" % manager)
        username = raw_input("Username: ")
        if not username:
            print("Username must not be empty")
            exit(-3)
        else:
            print("Please enter password for %s (will not be echoed)" % manager)
            password = getpass()
            if not password:
                print("Password must not be empty")
            exit(-3)
    else:
        print("%s is unreacheable" % manager)
        exit(1)

    while True:
        clear()
        menu()
        option = raw_input("Choice: ")

        if option == "2":
            break
        elif option == "1":
            hosts['local'] = (get_local_hosts(api=api, remote=hosts['remote']))
            if status(api=api, hosts=hosts):
                sub_menu()
                sub_option = raw_input("Choice: ")
                if sub_option == "2":
                    break
                elif sub_option == "1":
                    print("Initializing DRP")
                    for host in hosts['local']:
                        if (status_one_host(api, host)) == 'non_responsive':
                            print("Fencing host {}".format(host))
                            if do_fence_host(api, host):
                                print("Fencing host {} OK".format(host))
                                print("Set Maintenance host {}".format(host))
                                if do_maintenance_host(api, host):
                                    print("Maintenance host {} OK".format(host))
                                else:
                                    print("Error trying to set Maintenance")
                        elif (status_one_host(api, host)) == 'maintenance':
                            pass
                        else:
                            print("Error trying to set Fencing")
                        time.sleep(5)
                    print("Update Database")
                    modify_db(db_user=db_user, db_password=db_password,
                              database=database, manager=manager, lunsArray=iscsi_luns, portalsArray=iscsi_portals)
                    for host in hosts['remote']:
                        do_activate_host(api, host)
                    drp_finish(api)
            else:
                print("Not Continue")
            raw_input("Press Enter to continue...")
        else:
            print("{} is not a valid option".format(option))
            raw_input("Press Enter to continue...")


if __name__ == '__main__':
    main()
