import vagrant
import paramiko
import os
from subprocess import CalledProcessError


class VM:
    def __init__(self, location):
        os.mkdir(location)
        self.vagrant = vagrant.Vagrant(root=location, quiet_stdout=False, quiet_stderr=False)
        self.client = paramiko.SSHClient()

    def __del__(self):
        # self.vagrant.halt()
        self.client.close()

    def create(self, os_string, analyzed_fs="", reconstructed_fs="", vbguest=True):

        try:
            self.vagrant.init()
        except CalledProcessError:
            raise Exception("Vagrant VM already created! Destroy it first")

        file = open(self.vagrant.root + "/Vagrantfile", "w")
        file.write("# Created by forrec\n")
        file.write("Vagrant.configure(\"2\") do |config| \n")
        file.write("\tconfig.vm.box = \"" + os_string + "\" \n")
        if analyzed_fs:
            file.write("\tconfig.vm.synced_folder \"" + analyzed_fs + "\", \"/mnt/analyzed_fs\"\n")
        if reconstructed_fs:
            file.write("\tconfig.vm.synced_folder \"" + reconstructed_fs + "\", \"/mnt/reconstructed_fs\"\n")
        if not vbguest:
            file.write("\tconfig.vbguest.auto_update = false\n")
        file.write("end \n")
        file.close()

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
