from forrec import vm


class Investigator:
    def __init__(self, directory, vbname, os_string, sync_folders):
        self.directory = directory
        self.vbname = vbname
        self.vm = vm.VM(directory, vbname)
        self.vm.create(os_string, sync_folders)

    def mount_image(self):
        pass

    def get_hash(self):
        pass
