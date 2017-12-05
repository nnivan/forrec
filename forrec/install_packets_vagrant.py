import subprocess 
import os
from subprocess import call
import pexpect

const_box = "ubuntu/xenial64"
const_synced_folder = "/home/ivan/Documents/cpHostRootFolder/hostrootfolder"

directory = os.getcwd()
directory = directory + "/vagrant_vm"

os.chdir(directory);


# child = pexpect.spawn("vagrant ssh", timeout=None)
# child.expect("ubuntu-xenial", timeout=None)
# child.sendline("cd /analyse")
# child.expect("ubuntu-xenial", timeout=None)
# child.sendline("sudo chroot .")
# child.expect("root@ubuntu-xenial", timeout=None)
# child.logfile = open("python_vagrant.log", "w")
# child.sendline("dpkg -l | cat")
# child.expect("root@ubuntu-xenial", timeout=None)

data = subprocess.check_output(["dpkg", "-l", "--root=" + const_synced_folder])

data = data.splitlines()

del data[0:5]

# datafile = open('python_vagrant.log', 'r')
# data=datafile.read()
# datafile.close()

print "*vagrant ssh*"

child = pexpect.spawn("vagrant ssh", timeout=None)
child.expect("ubuntu-xenial", timeout=None)
child.sendline("cd /")
child.expect("ubuntu-xenial", timeout=None)
child.sendline("sudo su")
child.expect("root@ubuntu-xenial", timeout=None)

for line in data:
	
	line = line.split()
	line = line[1] + '=' + line[2]
	print "\033[96msudo apt-get install " + line + " -y\033[0m"
	
	child.sendline("apt-get install " + line + " -y")
	child.expect("root@ubuntu-xenial", timeout=None)
	print child.before

print "\033[92m -Ready-"