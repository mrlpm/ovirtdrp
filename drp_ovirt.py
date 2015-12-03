from __future__ import print_function

from functions_ovirt import connect, status_one_host, read_config, clear, menu


def status():
    clear()
    print("status")
    raw_input("Press Enter to continue...")


def iniciar():
    clear()
    print("iniciar")
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

        if option == "3":
            break
        elif option == "1":
            status()
        elif option == "2":
            iniciar()
        else:
            print("no existe la opcion")


if __name__ == '__main__':
    main()
