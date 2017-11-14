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
child.sendline("dpkg -l")
child.expect("root@ubuntu-xenial", timeout=None)

data = []

datafile = open('python_vagrant.log', 'r')
data=datafile.read()
datafile.close()

data = data.splitlines();

del data[0:2]
del data[-1]

for line in data:
	line = line.split()
	print line