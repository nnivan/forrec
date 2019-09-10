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
            return DebianLike.create_debian_like_from_directory(directory, os_release)
        elif os_release['ID'] == "debian":
            return DebianLike.create_debian_like_from_directory(directory, os_release)
        elif os_release['ID'] == "fedora":
            return FedoraLike.create_fedora_like_from_directory(directory, os_release)

        raise NotImplementedError("Could not recognize the OS family type")

    @staticmethod
    @abstractmethod
    def os_release_to_os_string(os_release):
        pass

    # Returns e.g. ubuntu/xenial64
    @abstractmethod
    def get_os_string(self):
        pass

    @abstractmethod
    def get_packages(self, investigator):
        pass

    @abstractmethod
    def set_packages(self, package_list, reconstructed, archives=False):
        pass

    @abstractmethod
    def do_update(self, virtual_machine):
        pass


class DebianLike(Linux):
    def __init__(self, directory, os_release):
        super().__init__(directory, os_release)

    @staticmethod
    def create_debian_like_from_directory(directory, os_release):
        if os_release['ID'] == "ubuntu":
            return Ubuntu.create_ubuntu_from_directory(directory, os_release)
        elif os_release['ID'] == "debian":
            return Debian.create_debian_from_directory(directory, os_release)

        raise NotImplementedError("Could not recognize the OS family type")

    @staticmethod
    @abstractmethod
    def os_release_to_os_string(os_release):
        pass

    @abstractmethod
    def get_os_string(self):
        pass

    @abstractmethod
    def get_packages(self, investigator):
        pass

    @abstractmethod
    def set_packages(self, package_list, reconstructed, archives=False):
        pass

    @abstractmethod
    def do_update(self, virtual_machine):
        pass


class FedoraLike(Linux):
    def __init__(self, directory, os_release):
        super().__init__(directory, os_release)

    @staticmethod
    def create_fedora_like_from_directory(directory, os_release):
        if os_release['ID'] == "fedora":
            return Fedora.create_fedora_from_directory(directory, os_release)

        raise NotImplementedError("Could not recognize the OS family type")

    @staticmethod
    @abstractmethod
    def os_release_to_os_string(os_release):
        pass

    @abstractmethod
    def get_os_string(self):
        pass

    @abstractmethod
    def get_packages(self, investigator):
        pass

    @abstractmethod
    def set_packages(self, package_list, reconstructed, archives=False):
        pass

    @abstractmethod
    def do_update(self, virtual_machine):
        pass


class Debian(DebianLike):
    def __init__(self, directory, os_release, os_string):
        super().__init__(directory, os_release)
        self.os_string = os_string

    @staticmethod
    def create_debian_from_directory(directory, os_release):
        os_string = Debian.os_release_to_os_string(os_release)
        return Debian(directory, os_release, os_string)

    @staticmethod
    def os_release_to_os_string(os_release):
        if '9' in os_release['VERSION_ID']:
            return 'debian/stretch64'
        else:
            raise NotImplementedError("Could not find the os string")

    def get_os_string(self):
        return self.os_string

    def get_packages(self, investigator):
        # TODO: FIX const --root=...
        stdin, stdout, stderr = investigator.execute_command("dpkg --list --root=/mnt/analyzed_fs/")
        packages_h = stdout.read().decode().splitlines()[5:]

        packages = []
        for p in packages_h:
            p = p.split()
            packages.append(p[1] + '=' + p[2])

        return packages

    def set_packages(self, package_list, reconstructed, archives=False):

        if archives:
            archives_dep_command = "sudo bash -c \"echo -e '\ndeb http://archive.debian.org/debian/ etch main non-free contrib\ndeb-src http://archive.debian.org/debian/ etch main non-free contrib\ndeb http://archive.debian.org/debian-security/ etch/updates main non-free contrib\ndeb-src http://archive.debian.org/debian-security/ etch/updates main non-free contrib\n\ndeb http://archive.debian.org/debian/ bo main non-free contrib\ndeb-src http://archive.debian.org/debian/ bo main non-free contrib\ndeb http://archive.debian.org/debian-security/ bo/updates main non-free contrib\ndeb-src http://archive.debian.org/debian-security/ bo/updates main non-free contrib\n\ndeb http://archive.debian.org/debian/ rex main non-free contrib\ndeb-src http://archive.debian.org/debian/ rex main non-free contrib\ndeb http://archive.debian.org/debian-security/ rex/updates main non-free contrib\ndeb-src http://archive.debian.org/debian-security/ rex/updates main non-free contrib\n\ndeb http://archive.debian.org/debian/ buzz main non-free contrib\ndeb-src http://archive.debian.org/debian/ buzz main non-free contrib\ndeb http://archive.debian.org/debian-security/ buzz/updates main non-free contrib\ndeb-src http://archive.debian.org/debian-security/ buzz/updates main non-free contrib\n\ndeb http://archive.debian.org/debian/ hamm main non-free contrib\ndeb-src http://archive.debian.org/debian/ hamm main non-free contrib\ndeb http://archive.debian.org/debian-security/ hamm/updates main non-free contrib\ndeb-src http://archive.debian.org/debian-security/ hamm/updates main non-free contrib\n\ndeb http://archive.debian.org/debian/ slink main non-free contrib\ndeb-src http://archive.debian.org/debian/ slink main non-free contrib\ndeb http://archive.debian.org/debian-security/ slink/updates main non-free contrib\ndeb-src http://archive.debian.org/debian-security/ slink/updates main non-free contrib\n\ndeb http://archive.debian.org/debian/ potato main non-free contrib\ndeb-src http://archive.debian.org/debian/ potato main non-free contrib\ndeb http://archive.debian.org/debian-security/ potato/updates main non-free contrib\ndeb-src http://archive.debian.org/debian-security/ potato/updates main non-free contrib\n\ndeb http://archive.debian.org/debian/ woody main non-free contrib\ndeb-src http://archive.debian.org/debian/ woody main non-free contrib\ndeb http://archive.debian.org/debian-security/ woody/updates main non-free contrib\ndeb-src http://archive.debian.org/debian-security/ woody/updates main non-free contrib\n\ndeb http://archive.debian.org/debian/ sarge main non-free contrib\ndeb-src http://archive.debian.org/debian/ sarge main non-free contrib\ndeb http://archive.debian.org/debian-security/ sarge/updates main non-free contrib\ndeb-src http://archive.debian.org/debian-security/ sarge/updates main non-free contrib\n\ndeb http://archive.debian.org/debian/ lenny main non-free contrib\ndeb-src http://archive.debian.org/debian/ lenny main non-free contrib\ndeb http://archive.debian.org/debian-security/ lenny/updates main non-free contrib\ndeb-src http://archive.debian.org/debian-security/ lenny/updates main non-free contrib\n\ndeb http://archive.debian.org/debian/ squeeze main non-free contrib\ndeb-src http://archive.debian.org/debian/ squeeze main non-free contrib\ndeb http://archive.debian.org/debian-security/ squeeze/updates main non-free contrib\ndeb-src http://archive.debian.org/debian-security/ squeeze/updates main non-free contrib\n' >> /etc/apt/sources.list\""
            archives_update_command = "sudo apt-get -o Acquire::Check-Valid-Until=false update"
            stdin, stdout, stderr = reconstructed.execute_command(archives_dep_command)
            print(stdout.read().decode())
            print(stderr.read().decode())
            stdin, stdout, stderr = reconstructed.execute_command(archives_update_command)
            print(stdout.read().decode())
            print(stderr.read().decode())

        count = 0
        for package in package_list:
            count = count + 1

            command = "sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install " + package
            print("Package (", count, "/", len(package_list), "): ", command)

            stdin, stdout, stderr = reconstructed.execute_command(command)
            print(stdout.read().decode())
            print(stderr.read().decode())

    def do_update(self, virtual_machine):
        command = "sudo DEBIAN_FRONTEND=noninteractive apt-get update -yq"
        stdin, stdout, stderr = virtual_machine.execute_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())

        command = "sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -yq"
        stdin, stdout, stderr = virtual_machine.execute_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())


class Ubuntu(DebianLike):
    def __init__(self, directory, os_release, os_string):
        super().__init__(directory, os_release)
        self.os_string = os_string

    @staticmethod
    def create_ubuntu_from_directory(directory, os_release):
        os_string = Ubuntu.os_release_to_os_string(os_release)
        return Ubuntu(directory, os_release, os_string)

    @staticmethod
    def os_release_to_os_string(os_release):
        if '14.' in os_release['VERSION_ID']:
            return 'ubuntu/trusty64'
        elif '16.' in os_release['VERSION_ID']:
            return 'ubuntu/xenial64'
        else:
            raise NotImplementedError("Could not find the os string")

    def get_os_string(self):
        return self.os_string

    def get_packages(self, investigator):
        # TODO: FIX const --root=...
        stdin, stdout, stderr = investigator.execute_command("dpkg --list --root=/mnt/analyzed_fs/")
        packages_h = stdout.read().decode().splitlines()[5:]

        packages = []
        for p in packages_h:
            p = p.split()
            packages.append(p[1] + '=' + p[2])

        return packages

    def set_packages(self, package_list, reconstructed, archives=False):

        count = 0
        for package in package_list:
            count = count + 1

            command = "sudo DEBIAN_FRONTEND=noninteractive apt-get -yq install " + package
            print("Package (", count, "/", len(package_list), "): ", command)

            stdin, stdout, stderr = reconstructed.execute_command(command)
            print(stdout.read().decode())
            print(stderr.read().decode())

    def do_update(self, virtual_machine):
        command = "sudo DEBIAN_FRONTEND=noninteractive apt-get update -yq"
        stdin, stdout, stderr = virtual_machine.execute_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())

        command = "sudo DEBIAN_FRONTEND=noninteractive apt-get upgrade -yq"
        stdin, stdout, stderr = virtual_machine.execute_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())


class Fedora(FedoraLike):
    def __init__(self, directory, os_release, os_string):
        super().__init__(directory, os_release)
        self.os_string = os_string

    @staticmethod
    def create_fedora_from_directory(directory, os_release):
        os_string = Fedora.os_release_to_os_string(os_release)
        return Fedora(directory, os_release, os_string)

    @staticmethod
    def os_release_to_os_string(os_release):
        if '29' in os_release['VERSION_ID']:
            return 'generic/fedora29'
        elif '28' in os_release['VERSION_ID']:
            return 'generic/fedora28'
        elif '27' in os_release['VERSION_ID']:
            return 'generic/fedora27'
        elif '26' in os_release['VERSION_ID']:
            return 'generic/fedora26'
        elif '25' in os_release['VERSION_ID']:
            return 'generic/fedora25'
        else:
            raise NotImplementedError("Could not find the os string")

    def get_os_string(self):
        return self.os_string

    def get_packages(self, investigator):
        stdin, stdout, stderr = investigator.execute_command("rpm -qa --dbpath=/mnt/analyzed_fs/var/lib/rpm")
        packages_h = stdout.read().decode()
        packages = packages_h.splitlines()

        return packages

    def set_packages(self, package_list, reconstructed, archives=False):

        count = 0
        for package in package_list:
            count = count + 1

            command = "sudo yum install -y " + package
            print("Package (", count, "/", len(package_list), "): ", command)

            stdin, stdout, stderr = reconstructed.execute_command(command)
            print(stdout.read().decode())
            print(stderr.read().decode())

    def do_update(self, virtual_machine):
        command = "sudo yum update -y"

        stdin, stdout, stderr = virtual_machine.execute_command(command)
        print(stdout.read().decode())
        print(stderr.read().decode())
