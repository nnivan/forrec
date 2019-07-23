import vagrant
import paramiko
from subprocess import CalledProcessError


class VM:
    def __init__(self, location):
        self.vagrant = vagrant.Vagrant(root=location, quiet_stdout=True, quiet_stderr=True)
        self.client = paramiko.SSHClient()

    def __del__(self):
        self.vagrant.halt()
        self.client.close()

    def create(self, os_string):

        try:
            self.vagrant.init(os_string)
        except CalledProcessError:
            raise Exception("Vagrant VM already created! Destroy it first")

        self.vagrant.up()

        hostname = self.vagrant.hostname()
        user = self.vagrant.user()
        port = self.vagrant.port()
        file_key = self.vagrant.keyfile()

        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.client.connect(hostname, username=user, port=port, key_filename=file_key)

    def execute_command(self, command):

        stdin, stdout, stderr = self.client.exec_command(command)

        return stdin, stdout, stderr

    def popen(self):
        pass
