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
        virtual_machine = LinuxOS(directory)
        virtual_machine.set_packages = vm.install_packages
        return virtual_machine

    @staticmethod
    def analyze_differences(list1, list2):

        list1.sort(key=lambda file: file[2])
        list2.sort(key=lambda file: file[2])

        ok = []
        wr = []
        ex = []
        ms = []

        i = x = 0
        while i < len(list1) and x < len(list2):
            if list1[i][2] == list2[x][2]:
                if list1[i][1] == list2[x][1] and list1[i][0] == list2[x][0]:
                    # print '\033[92m', "[ok] -", list1[i][2]
                    ok.append(list1[i][2])
                else:
                    # print '\033[91m', "[wr] -", list1[i][2]
                    wr.append(list1[i][2])
                i += 1
                x += 1
            elif list1[i][2] < list2[x][2]:
                # print '\033[93m', "[ex] -", list1[i][2]
                ex.append(list1[i][2])
                i += 1
            else:
                # print '\033[94m', "[ms] -", list2[x][2]
                ms.append(list2[x][2])
                x += 1

        while i < len(list1):
            # print '\033[93m', "[ex] -", list1[i][2]
            ex.append(list1[i][2])
            i += 1

        while x < len(list2):
            # print '\033[94m', "[ms] -", list2[x][2]
            ms.append(list2[x][2])
            x += 1

        # print '\033[0m', "\n Statistics: "
        # print '\033[0m', "Total", '\033[92m' + "Okay    -", ok
        # print '\033[0m', "Total", '\033[91m' + "Wrong   -", wr
        # print '\033[0m', "Total", '\033[94m' + "Missing -", ms
        # print '\033[0m', "Total", '\033[93m' + "Extra   -", ex
        # print '\033[0m'

        return [ok, wr, ex, ms]

    @staticmethod
    def print_differences(differences, verbose):
        if verbose >= 3:
            for x in differences[0]:
                print '\033[92m', "[ok] -", x
        if verbose >= 2:
            for x in differences[3]:
                print '\033[94m', "[ms] -", x
            for x in differences[2]:
                print '\033[93m', "[ex] -", x
        if verbose >= 1:
            for x in differences[1]:
                print '\033[91m', "[wr] -", x

        print '\033[0m', "\n Statistics: "
        print '\033[0m', "Total", '\033[92m' + "Okay    -", len(differences[0])
        print '\033[0m', "Total", '\033[91m' + "Wrong   -", len(differences[1])
        print '\033[0m', "Total", '\033[93m' + "Extra   -", len(differences[2])
        print '\033[0m', "Total", '\033[94m' + "Missing -", len(differences[3])
        print '\033[0m'


class LinuxOS(OS):
    def __init__(self, directory):
        self.root_directory = directory
    
    @staticmethod
    def _create_linux_from_directory(directory):
        return LinuxOS(directory)

    # TODO
    @staticmethod
    def get_os_architecture():
        return '64'

    def fetch_os_string(self):
        sp_args = "cat ./etc/os-release" # sp_args = "cat ./etc/*-release"
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
        pass

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
