class OS:
    def __init__(self):
        pass
    
    # Returns e.g. ubuntu/xenial64
    def fetch_os_string(self):
        pass
    
    # Returns a list of installed packages on the OS
    def extract_packages(self):
        pass
    
    # Installs/uninstalls packages from the OS until the current packages match package_list
    def set_packages(self, package_list):
        pass
    
    # Create an OS instasnce from a directory
    @staticmethod
    def create_from_directory(directory):
        pass
    
    def build():
        pass
    
    def analyze_differences(other_os):
        pass
