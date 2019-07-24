import subprocess
import os
from abc import ABCMeta, abstractmethod
from forrec import vm


def readfile(filename):
    return open(os.path.join(os.path.dirname(__file__), filename)).read()


class OS:
    __metaclass__ = ABCMeta
    
    def __init__(self):
        pass

    @staticmethod
    def _is_linux(directory):
        try:
            readfile(directory + "/etc/os-release").splitlines()
        except FileNotFoundError:
            return False
        return True

    @staticmethod
    def create_from_directory(directory):
        # Check for actual OS families
        if OS._is_linux(directory):
            print("os is linux")
            return Linux.create_linux_from_directory(directory)
        # TODO: Check for other OS families - Windows, BSD, Mac, other Unices?
        raise NotImplementedError("Could not recognize the OS family type")
    
    # # Create an OS instance from a directory
    # @staticmethod
    # def create_from_vm(directory, vm):
    #     pass


class Linux(OS):
    def __init__(self, directory, os_release):
        super().__init__()
        self.os_release = os_release
        self.root_directory = directory

    @staticmethod
    def create_linux_from_directory(directory):
        os_release_content = readfile(directory + "/etc/os-release").splitlines()
        os_release = {}
        for line in os_release_content:
            key, value = line.rstrip("\n").split("=")
            os_release[key] = value

        if os_release['ID'] == "ubuntu":
            print("os is debian like")
            return DebianLike.create_debian_like_from_directory(directory, os_release)
        elif os_release['ID'] == "fedora":
            print("os is fedora like")
            return FedoraLike.create_fedora_like_from_directory(directory, os_release)

        raise NotImplementedError("Could not recognize the OS family type")

    # Returns e.g. ubuntu/xenial64
    @abstractmethod
    def get_os_string(self):
        pass


class DebianLike(Linux):
    def __init__(self, directory, os_release):
        super().__init__(directory, os_release)

    @staticmethod
    def create_debian_like_from_directory(directory, os_release):
        if os_release['ID'] == "ubuntu":
            print("os is ubuntu")
            return Ubuntu.create_ubuntu_from_directory(directory, os_release)

        raise NotImplementedError("Could not recognize the OS family type")

    @abstractmethod
    def get_os_string(self):
        pass


class FedoraLike(Linux):
    def __init__(self, directory, os_release):
        super().__init__(directory, os_release)

    @staticmethod
    def create_fedora_like_from_directory(directory, os_release):
        if os_release['ID'] == "fedora":
            print("os is fedora")
            return Fedora.create_fedora_from_directory(directory, os_release)

        raise NotImplementedError("Could not recognize the OS family type")

    @abstractmethod
    def get_os_string(self):
        pass


class Ubuntu(DebianLike):
    def __init__(self, directory, os_release):
        super().__init__(directory, os_release)

    @staticmethod
    def create_ubuntu_from_directory(directory, os_release):
        return Ubuntu(directory, os_release)

    def get_os_string(self):
        for key in self.os_release:
            print(key + ':', self.os_release[key])
        return self.os_release['VERSION_ID']


class Fedora(FedoraLike):
    def __init__(self, directory, os_release):
        super().__init__(directory, os_release)

    @staticmethod
    def create_fedora_from_directory(directory, os_release):
        return Fedora(directory, os_release)

    def get_os_string(self):
        for key in self.os_release:
            print(key + ':', self.os_release[key])
        return self.os_release['VERSION_ID']

