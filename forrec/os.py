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
        print pout
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
        
    @abstractmethod
    def build(self):
        pass
    
    @abstractmethod
    def analyze_differences(other_os):
        pass


class LinuxOS(OS):
    def __init__(self, directory):
        self.root_directory = directory
    
    @staticmethod
    def _create_linux_from_directory(directory):
        sp_args = "cat ./etc/*-release"
        p = subprocess.Popen(sp_args, stdout=subprocess.PIPE, shell=True, cwd=directory)
        pout, perr = p.communicate()
        print pout