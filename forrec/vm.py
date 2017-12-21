import vagrant

class VM:
    def __init__(self, location_dir):
        self.vagrant = vagrant.Vagrant(location_dir)
    
    def create(self, os_string):
        if vagrant.status()[0].state != "not_created":
            raise VMError("Vagrant VM already created! Destroy it first")
        self.vagrant.init(os_string)
        self.vagrant.up()
    
    def popen(self):
        pass
