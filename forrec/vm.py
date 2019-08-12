import vagrant
import paramiko
import os
import subprocess
from subprocess import CalledProcessError


class VM:
    def __init__(self, location, vbname):
        os.mkdir(location)
        self.vagrant = vagrant.Vagrant(root=location, quiet_stdout=False, quiet_stderr=False)
        self.client = paramiko.SSHClient()
        self.vbname = vbname

    def __del__(self):
        # self.vagrant.halt()
        self.client.close()

    def get_fs(self, directory):
        self.vagrant.halt()
        vmdk_location = "~/VirtualBox\\ VMs/" + self.vbname + "/*.vmdk"
        sp_args = "vboxmanage clonehd --format VDI " + vmdk_location + " disk_" + self.vbname + ".vdi"
        print(sp_args)
        p = subprocess.Popen(sp_args, stdout=subprocess.PIPE, shell=True, cwd=directory)
        pout, perr = p.communicate()
        print(pout)
        print(perr)

    def mount_image(self, file_location):
        # TODO: FIX
        stdin, stdout, stderr = self.execute_command("sudo mkdir /mnt/reconstructed_fs")
        print(stdout.read().decode())
        print(stderr.read().decode())
        stdin, stdout, stderr = self.execute_command("sudo modprobe nbd")
        print(stdout.read().decode())
        print(stderr.read().decode())
        stdin, stdout, stderr = self.execute_command("sudo qemu-nbd -r -c /dev/nbd1 " + file_location)
        print(stdout.read().decode())
        print(stderr.read().decode())
        stdin, stdout, stderr = self.execute_command("sudo mount -o ro /dev/nbd1p1 /mnt/reconstructed_fs")
        print(stdout.read().decode())
        print(stderr.read().decode())
        stdin, stdout, stderr = self.execute_command("ls /mnt")
        print(stdout.read().decode())
        print(stderr.read().decode())

    def create(self, os_string, sync_folders=[], vbguest=True):

        try:
            self.vagrant.init()
        except CalledProcessError:
            raise Exception("Vagrant VM already created! Destroy it first")

        file = open(self.vagrant.root + "/Vagrantfile", "w")
        file.write("# Created by forrec\n")
        file.write("Vagrant.configure(\"2\") do |config| \n")
        file.write("\tconfig.vm.box = \"" + os_string + "\" \n")
        for folder in sync_folders:
            file.write("\tconfig.vm.synced_folder \"" + folder[0] + "\", \"/mnt/" + folder[1] + "\"\n")
        if not vbguest:
            file.write("\tconfig.vbguest.auto_update = false\n")
        file.write("\tconfig.vm.provider \"virtualbox\" do | vb |\n")
        file.write("\t\tvb.name = \"" + self.vbname + "\"\n")
        file.write("\tend\n")
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

    # TODO: fix const names
    def get_hash(self, folders):

        for folder in folders:

            hash_list_analyzed = []
            hash_list_reconstructed = []

            command_analyzed = "find /mnt/analyzed_fs/" + folder + " -type f -exec sha256sum {} \\;"
            command_reconstructed = "find /mnt/reconstructed_fs/" + folder + " -type f -exec sha256sum {} \\;"

            stdin, stdout_analyzed, stderr_analyzed = self.execute_command(command_analyzed)
            stdin, stdout_reconstructed, stderr_reconstructed = self.execute_command(command_reconstructed)

            stdout_analyzed = stdout_analyzed.read().decode().splitlines()
            stdout_reconstructed = stdout_reconstructed.read().decode().splitlines()

            for i in stdout_analyzed:
                i = i.split()
                i[1] = i[1][len("/mnt/analyzed_fs/"):]
                hash_list_analyzed.append(["0", i[0], i[1]])

            for i in stdout_reconstructed:
                i = i.split()
                i[1] = i[1][len("/mnt/reconstructed_fs/"):]
                hash_list_reconstructed.append(["0", i[0], i[1]])

            return hash_list_analyzed, hash_list_reconstructed

    def popen(self):
        pass
