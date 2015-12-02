from __future__ import print_function
from functions_ovirt import connect, status_one_host


USERNAME_MANAGER = "admin@internal"
NAME_MANAGER = 'nrhevm.itmlabs.local'
URL_MANAGER = 'https://' + NAME_MANAGER
PASSWORD_MANAGER = 'S0p0rt32015.'


def main():
    api = connect(rhevm_url=URL_MANAGER, rhevm_username=USERNAME_MANAGER, rhevm_password=PASSWORD_MANAGER)
    print(status_one_host(api, 'nhost2.itmlabs.local'))


if __name__ == '__main__':
    main()
