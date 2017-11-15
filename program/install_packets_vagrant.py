import subprocess 
import os
from subprocess import call
import pexpect

const_box = "ubuntu/xenial64"
const_synced_folder = "/home/ivan/Documents/lh_project2018/hostrootfolder"

directory = os.getcwd()
directory = directory + "/vagrant_vm"

if not os.path.exists(directory):
    os.makedirs(directory)

os.chdir(directory);

print "*vagrant ssh*"

child = pexpect.spawn("vagrant ssh", timeout=None)
child.expect("ubuntu-xenial", timeout=None)
child.sendline("cd /analyse")
child.expect("ubuntu-xenial", timeout=None)
child.sendline("sudo chroot .")
child.expect("root@ubuntu-xenial", timeout=None)
child.logfile = open("python_vagrant.log", "w")
child.sendline("dpkg -l | cat")
child.expect("root@ubuntu-xenial", timeout=None)

datafile = open('python_vagrant.log', 'r')
data=datafile.read()
datafile.close()

child.sendline("exit")
child.expect("ubuntu-xenial", timeout=None)
child.sendline("cd /")
child.expect("ubuntu-xenial", timeout=None)
child.sendline("ls")
child.expect("ubuntu-xenial", timeout=None)

data = data.splitlines();

del data[0:7]
del data[-1]

child.sendline("sudo su")
child.expect("root@ubuntu-xenial", timeout=None)

for line in data:
	
	line = line.split()
	line = line[1] + '=' + line[2]
	print "\033[96msudo apt-get install " + line + " -y\033[0m"
	
	child.sendline("apt-get install " + line + " -y")
	child.expect("root@ubuntu-xenial", timeout=None)
	print child.before

print "\033[92m rdy!"