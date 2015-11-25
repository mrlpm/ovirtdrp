#!/home/binary/.virtualenvs/drpman/bin/python

from ovirtsdk.xml import params
from ovirtsdk.api import API
from ovirtsdk.infrastructure.errors import ConnectionError

USERNAME_RHEVM="admin@internal"
RHEVM_NAME='nrhevm.itmlabs.local'
RHEVM_URL='https://' + RHEVM_NAME
PASSWORD_RHEVM='S0p0rt32015.'

class drp:
    def __init__(self, manager, username, password):
        self.rhevm_url = 'https://' + manager
        self.rhevm_username = username
        self.rhevm_password = password

    def connect(self):
        try:
            self.api = API(url=self.rhevm_url, username=self.rhevm_username, password=self.rhevm_password, insecure="True")
            print "connect OK"
        except ConnectionError, err:
            print ("Connection failed: %s") % err
            exit(-1)

    def hosts(self):
        self.hosts_lists = self.api.hosts.list()
        return self.hosts_lists

    def status_all_hosts(self):
        self.hosts = self.hosts()
        for self.host in self.hosts:
                print "Host: " + self.host.get_name() + " Status:" + self.host.get_status().get_state()

    def status_one_host(self, name):
        self.alone_host = self.api.hosts.get(name)
        print "Host: " + self.alone_host.get_name() + " Status: " + self.alone_host.get_status().get_state()

    def get_non_responsive(self):
        self.all_hosts = self.hosts()
        for self.host_non in self.all_hosts:
            if self.host_non.get_status().get_state() == 'non_responsive':
                print self.host.get_name()
            else:
                print "host ok"
        

def main():
    drpctrl = drp(RHEVM_NAME, USERNAME_RHEVM, PASSWORD_RHEVM)
    drpctrl.connect()
    drpctrl.status_one_host('nhost2.itmlabs.local')
    drpctrl.get_non_responsive()


if __name__ == '__main__':
    main()
