import vagrant

class VM:
    def __init__(self, location_dir):
        self.vagrant = vagrant.Vagrant(location_dir)
    
    def create(self, os_string):
        print self.vagrant.status()
        print self.vagrant.status()[0].state 

        if self.vagrant.status()[0].state != "not_created":
            raise VMError("Vagrant VM already created! Destroy it first")

        self.vagrant.init(os_string)
        self.vagrant.up()

    def install_packages(self,package_list):
        for package in package_list:
            print package
            try:
                print self.vagrant.ssh(None, "sudo apt-get -y install " + package);
            except Exception:
                print package, "failed to install"

    def fetch_cksum(self,folders_list):
        cksum_list = []
        for folder in folders_list:
            cksum_folder = self.vagrant.ssh(None, "find " + folder + " -type f -exec cksum {} \;")
            cksum_folder = cksum_folder.splitlines();
            for i in cksum_folder:
                cksum_list.append(i.split());
                # print i.split()
        return cksum_list

    def popen(self):
        pass
