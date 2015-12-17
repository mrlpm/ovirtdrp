from __future__ import print_function

from functions_ovirt import *


def main():
    config = read_config(file_config='config.yml')
    username = config['username']
    password = config['password']
    manager = config['manager']
    database = config['database']
    db_user = config['userDatabase']
    db_password = config['passDatabase']
    url_manager = 'https://' + manager
    hosts = config["Hosts"]

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
                        if (status_one_host(api,host)) == 'non_responsive':
                            print("Fencing host {}".format(host))
                            if do_fence(api, host):
                                print("Fencing host {} OK".format(host))
                                print("Set Maintenance host {}".format(host))
                                if do_maintenance(api, host):
                                    print("Maintenance host {} OK".format(host))

                                #if ping(manager):
                                #    session = session_db(db_name=database, manager=manager,
                                #                         user=db_user, password=db_password, class_name='Connections')
                                #    res = session.query(Bookmarks).all()
                                #    print(res)
                                else:
                                    print("Error trying to set Maintenance")
                        else:
                            print("Error trying to set Fencing")
            else:
                print("Site A OK")
                print("Not Continue")
            raw_input("Press Enter to continue...")
        else:
            print("{} is not a valid option".format(option))
            raw_input("Press Enter to continue...")


if __name__ == '__main__':
    main()
