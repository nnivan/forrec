import subprocess 
import os
from subprocess import call
import pexpect
import sys

files_pc = subprocess.check_output(['find', '/bin', '-type', 'f'])
files_pc = files_pc.splitlines()

cksums_pc = [];

for file in files_pc:
	cksums_pc.append(subprocess.check_output(['cksum', file]).split())

#print cksums_pc


directory = os.getcwd()
directory = directory + "/vagrant"

os.chdir(directory);

#call(["vagrant","up"])

child = pexpect.spawn("vagrant ssh")

child.expect("ubuntu@ubuntu-xenial")

child.sendline("find /bin -type f | xargs cksum")

child.expect("ubuntu@ubuntu-xenial")
child.expect("ubuntu@ubuntu-xenial")

files_vagrant = child.before.splitlines();

files_vagrant.pop()
files_vagrant.pop(0)

cksums_vagrant = [];

for file in files_vagrant:
	cksums_vagrant.append(file.split())


cksums_pc.sort(key=lambda x: x[2])
cksums_vagrant.sort(key=lambda x: x[2])

print cksums_pc,cksums_vagrant