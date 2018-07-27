import vagrant
import paramiko
from subprocess import CalledProcessError

class VM:
    def __init__(self, location_dir):
        self.vagrant = vagrant.Vagrant(location_dir, quiet_stdout=False, quiet_stderr=False)
    
    def create(self, os_string):
        # print self.vagrant.status()
        # print self.vagrant.status()[0].state

        # if file exists (vagrant file):
        #
        #     print self.vagrant.status()
        #     print self.vagrant.status()[0].state
        #
        #     if self.vagrant.status()[0].state != "not_created":
        #         raise VMError("Vagrant VM already created! Destroy it first")

        # TODO: this works
        try:
            self.vagrant.init(os_string)
        except CalledProcessError:
                raise VMError("Vagrant VM already created! Destroy it first")

        self.vagrant.up()

    def install_packages(self, package_list):

        ssh_config = self.vagrant.ssh_config()
        print ssh_config
        ssh_config = ssh_config.splitlines()


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

        client = paramiko.SSHClient()

        client.load_system_host_keys()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        client.connect(hostname, username=user, port=port, key_filename = file_key)

        for package in package_list:
            print package

            stdin, stdout, stderr = client.exec_command("sudo apt-get -y install " + package)
            print stdout.read()

            err = stderr.read()

            if err:
                print package, "failed"
                print err

        client.close()

    def fetch_cksum(self, folders_list):
        cksum_list = []
        for folder in folders_list:
            cksum_folder = self.vagrant.ssh(None, "find " + folder + " -type f -exec cksum {} \;")
            cksum_folder = cksum_folder.splitlines()
            for i in cksum_folder:
                cksum_list.append(i.split())
                # print i.split()
        return cksum_list

    def popen(self):
        pass
