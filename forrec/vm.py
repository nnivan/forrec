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


    def popen(self):
        pass
