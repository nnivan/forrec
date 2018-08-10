import subprocess
import os
from abc import ABCMeta, abstractmethod

class OS:
    __metaclass__ = ABCMeta
    
    def __init__(self):
        pass
    
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
    def analyze_differences(self, other_os):
        pass
    
    # @abstractmethod
    # def build(self):
    #     pass

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
    
    # Create an OS instasnce from a directory
    @staticmethod
    def create_from_directory(directory):
        # Check for actual OS families
        if OS._is_os_linux(directory):
            return LinuxOS._create_linux_from_directory(directory)
        # TODO: Check for other OS families - Windows, BSD, Mac, other Unices?
        raise NotImplementedError("Could not recognize the OS family type")
        
    @staticmethod
    def create_from_vm(directory,vm):
        virtual_machine = LinuxOS(directory)
        virtual_machine.set_packages = vm.install_packages
        return virtual_machine


class LinuxOS(OS):
    def __init__(self, directory):
        self.root_directory = directory
    
    @staticmethod
    def _create_linux_from_directory(directory):
        return LinuxOS(directory)

    @staticmethod
    def get_ID_from_release(release):
        start_id = release.find("\nID=")
        end_id = release.find("\n",start_id+4)
        return release[start_id+4:end_id]

    @staticmethod
    def get_VERSION_ID_from_release_and_ID(release, ID):

        start_version_id = release.find("\nVERSION_ID=")
        end_version_id = release.find("\n",start_version_id+11)
        VERSION_ID = release[start_version_id+13:end_version_id-1]

        if ID == 'debian':
            if VERSION_ID == '9':
                return 'stretch'
            elif VERSION_ID == '8':
                return 'jessie'

        if ID == 'ubuntu':
            if VERSION_ID == '14.04':
                return 'trusty'

        return VERSION_ID

    # TODO
    @staticmethod
    def get_os_architecture():
        return '64'

    def fetch_os_string(self):
        sp_args = "cat ./etc/os-release" # sp_args = "cat ./etc/*-release"
        p = subprocess.Popen(sp_args, stdout=subprocess.PIPE, shell=True, cwd=self.root_directory)
        pout, perr = p.communicate()

        ID = self.get_ID_from_release(pout)
        VERSION_ID = self.get_VERSION_ID_from_release_and_ID(pout, ID)
        os_architecture = self.get_os_architecture()

        return ID + '/' + VERSION_ID + os_architecture
 
    
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
        pass
    
    def analyze_differences(self, cksum_list):

        nf = 0
        ok = 0
        wr = 0

        for cksum_file in cksum_list:
            sp_args = "cksum " + self.root_directory + cksum_file[2]
            p = subprocess.Popen(sp_args, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, cwd=self.root_directory)
            pout, perr = p.communicate()
            pout = pout.split()
            if pout == []:
                print '\033[94m', "[nf] -", cksum_file[2]
                nf += 1
            elif pout[1] == cksum_file[1] and pout[0] == cksum_file[0]:
                print '\033[92m', "[ok] -", cksum_file[2]
                ok += 1
            else:
                print '\033[91m', "[wr] -", cksum_file[2]
                wr += 1

        print '\033[0m', "\n Statistics: "
        print '\033[0m', "Total", '\033[94m', "[nf] =", nf
        print '\033[0m', "Total", '\033[92m', "[ok] =", ok
        print '\033[0m', "Total", '\033[91m', "[wr] =", wr
        print '\033[0m'