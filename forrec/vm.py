import vagrant
import os
import paramiko
from subprocess import CalledProcessError


class VM:
    def __init__(self, location_dir):
        self.vagrant = vagrant.Vagrant(location_dir)

    def create_investigaor(self, os_string, sync_folder):

        try:
            self.vagrant.init(os_string)
        except CalledProcessError:
            raise VMError("Vagrant VM already created! Destroy it first")

        vagrant_file = open("investigator/Vagrantfile", "r")
        content = vagrant_file.readlines()
        vagrant_file.close()

        vagrant_file = open("investigator/Vagrantfile", "w")
        while "end" not in content[len(content) - 1]:
            content.pop()

        content.pop()
        content.append("\tconfig.vm.synced_folder \"" + sync_folder + "\", \"/mnt/image\", type: \"rsync\"\n")
        content.append("end\n")

        for line in content:
            vagrant_file.write(line)

        vagrant_file.close()

        self.vagrant.up()

        ssh_config = self.vagrant.ssh_config().splitlines()

        hostname = '127.0.0.1'
        user = 'vagrant'
        port = ''
        file_key = ''

        for line in ssh_config:
            line = line.split()
            if len(line) > 0:
                if line[0] == 'HostName':
                    hostname = line[1]
                elif line[0] == 'User':
                    user = line[1]
                elif line[0] == 'Port':
                    port = line[1]
                elif line[0] == 'IdentityFile':
                    file_key = line[1]

        print hostname, user, port, file_key

        self.client = paramiko.SSHClient()

        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.client.connect(hostname, username=user, port=port, key_filename=file_key)


    def create(self, os_string):

        try:
            self.vagrant.init(os_string)
        except CalledProcessError:
            raise VMError("Vagrant VM already created! Destroy it first")

        self.vagrant.up()

        ssh_config = self.vagrant.ssh_config().splitlines()

        hostname = '127.0.0.1'
        user = 'vagrant'
        port = ''
        file_key = ''

        for line in ssh_config:
            line = line.split()
            if len(line) > 0:
                if line[0] == 'HostName':
                    hostname = line[1]
                elif line[0] == 'User':
                    user = line[1]
                elif line[0] == 'Port':
                    port = line[1]
                elif line[0] == 'IdentityFile':
                    file_key = line[1]

        print hostname, user, port, file_key

        self.client = paramiko.SSHClient()

        self.client.load_system_host_keys()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.client.connect(hostname, username=user, port=port, key_filename=file_key)

    def execute_command(self, command):

        stdin, stdout, stderr = self.client.exec_command(command)

        return stdin, stdout, stderr

    # def install_packages(self, package_list):
    #
    #     for package in package_list:
    #         print package
    #
    #         stdin, stdout, stderr = self.client.exec_command("sudo apt-get -y install " + package)
    #         print stdout.read()
    #
    #         err = stderr.read()
    #
    #         if err:
    #             print package, "failed"
    #             print err


    def fetch_cksum(self, folders_list):
        cksum_list = []
        for folder in folders_list:
            cksum_folder = self.vagrant.ssh(None, "find " + folder + " -type f -exec cksum {} \;")
            cksum_folder = cksum_folder.splitlines()
            for i in cksum_folder:
                cksum_list.append(i.split())


        return cksum_list

    def popen(self):
        pass
