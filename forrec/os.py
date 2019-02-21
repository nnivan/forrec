import subprocess
import os
from abc import ABCMeta, abstractmethod

from forrec import vm

class OS:
    __metaclass__ = ABCMeta
    
    def __init__(self):
        pass

    @staticmethod
    def _is_os_linux(directory):
        sp_args = "ls ./etc/*-release | wc -l"
        p = subprocess.Popen(sp_args, stdout=subprocess.PIPE, shell=True, cwd=directory)
        pout, perr = p.communicate()
        try:
            if p.returncode == 0 and int(pout) > 0:
                return True
        except ValueError:
            pass
        # TODO: Add more methods of recognizing Linux from binary layout
        return False

    # @abstractmethod
    # def build(self):
    #     pass

    @staticmethod
    def create_from_directory(directory):
        # Check for actual OS families
        if OS._is_os_linux(directory):
            return LinuxOS._create_linux_from_directory(directory)
        # TODO: Check for other OS families - Windows, BSD, Mac, other Unices?
        raise NotImplementedError("Could not recognize the OS family type")
    
    # Create an OS instasnce from a directory
    @staticmethod
    def create_from_vm(directory,vm):
        # TODO: fix DebianLikeLinux._create_debian_linux_from_directory
        virtual_machine = DebianLikeLinux._create_debian_linux_from_directory(directory)
        # virtual_machine.set_packages = vm.install_packages
        virtual_machine.execute_command = vm.execute_command
        virtual_machine.fetch_cksum = vm.fetch_cksum    
        return virtual_machine



class LinuxOS(OS):
    def __init__(self, directory):
        self.root_directory = directory
    
    @staticmethod
    def _create_linux_from_directory(directory):
        linux_id = LinuxOS.fetch_os_id(directory)
        print "linux_id:", linux_id
        if linux_id == "debian":
            return DebianLikeLinux._create_debian_linux_from_directory(directory)
        elif linux_id == "ubuntu":
            return DebianLikeLinux._create_debian_linux_from_directory(directory)
        elif linux_id == "fedora":
            return FedoraLikeLinux(directory)

    @staticmethod
    def fetch_os_id(directory):
        sp_args = "cat ./etc/os-release" # sp_args = "cat ./etc/*-release"
        p = subprocess.Popen(sp_args, stdout=subprocess.PIPE, shell=True, cwd=directory)
        pout, perr = p.communicate()

        release = pout

        id_index = release.find("\nID=")
        ID = release[id_index + 4:release.find("\n", id_index + 4)]

        return ID

    # Returns e.g. ubuntu/xenial64
    @abstractmethod
    def fetch_os_string(self):
        pass

    # Returns a list of installed packages on the OS
    @abstractmethod
    def extract_packages(self):
        pass

    # Installs/uninstalls packages from the OS until the current packages match package_list
    @abstractmethod
    def set_packages(self, package_list):
        pass

    @abstractmethod
    def fetch_cksum(self, folders_list):
        pass



class DebianLikeLinux(LinuxOS):
    def __init__(self, directory):
        self.root_directory = directory

    @staticmethod
    def _create_debian_linux_from_directory(directory):
        return DebianLikeLinux(directory)

    # TODO
    @staticmethod
    def get_os_architecture():
        return '64'

    def fetch_os_string(self):
        sp_args = "cat ./etc/os-release"  # sp_args = "cat ./etc/*-release"
        p = subprocess.Popen(sp_args, stdout=subprocess.PIPE, shell=True, cwd=self.root_directory)
        pout, perr = p.communicate()

        release = pout

        id_index = release.find("\nID=")
        ID = release[id_index + 4:release.find("\n", id_index + 4)]

        version_index = release.find("\nVERSION_ID=")
        VERSION_ID = release[version_index + 13:release.find("\n", version_index + 11) - 1]

        if ID == 'debian':
            if VERSION_ID == '9':
                return 'debian/stretch' + self.get_os_architecture()
            elif VERSION_ID == '8':
                return 'debian/jessie' + self.get_os_architecture()
        elif ID == 'ubuntu':
            if VERSION_ID == '14.04':
                return 'ubuntu/trusty' + self.get_os_architecture()

    # Returns a list of installed packages on the OS
    def extract_packages(self):
        sp_args = "dpkg -l --root=" + self.root_directory
        p = subprocess.Popen(sp_args, stdout=subprocess.PIPE, shell=True, cwd=self.root_directory)
        pout, perr = p.communicate()

        pout = pout.splitlines()[5:]
        packages = []
        for i in pout:
            i = i.split()
            packages.append(i[1] + '=' + i[2])

        return packages

    # Installs/uninstalls packages from the OS until the current packages match package_list
    def set_packages(self, package_list):

        for package in package_list:
                print package

                stdin, stdout, stderr = self.execute_command("sudo apt-get -y install " + package)
                print stdout.read()

                err = stderr.read()

                if err:
                    print package, "failed"
                    print err

    def fetch_cksum(self, folders_list):

        cksum_list = []

        for folder in folders_list:

            sp_args = "find " + self.root_directory + folder + " -type f -exec cksum {} \;"
            p = subprocess.Popen(sp_args, stdout=subprocess.PIPE, shell=True, cwd=self.root_directory)
            pout, perr = p.communicate()

            cksum_folder = pout.splitlines()

            for i in cksum_folder:
                i = i.split()
                i[2] = i[2][len(self.root_directory):]
                cksum_list.append(i)

        return cksum_list


class FedoraLikeLinux(LinuxOS):
    def __init__(self, directory):
        self.root_directory = directory

    @staticmethod
    def _create_fedora_linux_from_directory(directory):
        return FedoraLikeLinux(directory)

    # TODO
    @staticmethod
    def get_os_architecture():
        return '64'

    def fetch_os_string(self):
        sp_args = "cat ./etc/os-release"  # sp_args = "cat ./etc/*-release"
        p = subprocess.Popen(sp_args, stdout=subprocess.PIPE, shell=True, cwd=self.root_directory)
        pout, perr = p.communicate()

        release = pout

        # id_index = release.find("\nID=")
        # ID = release[id_index + 4:release.find("\n", id_index + 4)]

        version_index = release.find("\nVERSION_ID=")
        VERSION_ID = release[version_index + 12:release.find("\n", version_index + 11)]

        return 'generic/fedora' + VERSION_ID


    def extract_packages(self):
        investigator_os = vm.VM('./investigator')

        if not os.path.exists(self.root_directory):
            os.mkdir("investigator")

        investigator_os.create_investigaor(self.fetch_os_string(), self.root_directory)
        raise Exception("debug")



        # sp_args = "dpkg -l --root=" + self.root_directory
        # p = subprocess.Popen(sp_args, stdout=subprocess.PIPE, shell=True, cwd=self.root_directory)
        # pout, perr = p.communicate()
        #
        # pout = pout.splitlines()[5:]
        # packages = []
        # for i in pout:
        #     i = i.split()
        #     packages.append(i[1] + '=' + i[2])
        #
        # return packages

    # Installs/uninstalls packages from the OS until the current packages match package_list
    def set_packages(self, package_list):

        for package in package_list:
                print package

                stdin, stdout, stderr = self.execute_command("sudo yum -y install" + package)
                print stdout.read()

                err = stderr.read()

                if err:
                    print package, "failed"
                    print err

    def fetch_cksum(self, folders_list):

        cksum_list = []

        for folder in folders_list:

            sp_args = "find " + self.root_directory + folder + " -type f -exec cksum {} \;"
            p = subprocess.Popen(sp_args, stdout=subprocess.PIPE, shell=True, cwd=self.root_directory)
            pout, perr = p.communicate()

            cksum_folder = pout.splitlines()

            for i in cksum_folder:
                i = i.split()
                i[2] = i[2][len(self.root_directory):]
                cksum_list.append(i)

        return cksum_list


# # TODO: Ubuntu
# class Ubuntu(DebianLikeLinux):
#     pass
#
# # TODO: Debian
# class Debian(DebianLikeLinux):
#     pass