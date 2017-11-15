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
child.logfile = open("python_vagrant.log", "w")
child.sendline("find /analyse/bin /analyse/etc -type f 2>/dev/null | xargs cksum 2>/dev/null")
child.expect("ubuntu-xenial", timeout=None)
child.expect("ubuntu-xenial", timeout=None)
#print "h - 1"

datafile = open('python_vagrant.log', 'r')
cksum_am=datafile.read()
datafile.close()

#print "h - 2.1"
child.expect("ubuntu-xenial", timeout=None)
child.sendline("find /bin /etc -type f | xargs cksum > /vagrant/cksums_vagrant_virtual_machine.log")
#print "h - 2.2"
child.expect("ubuntu-xenial", timeout=None)

#print "h - 3"

datafile = open(directory + "/cksums_vagrant_virtual_machine.log", 'r')
cksum_vm=datafile.read()
datafile.close()

#print "h - 4"

cksum_am = cksum_am.splitlines();
cksum_vm = cksum_vm.splitlines();

del cksum_am[0:3]
del cksum_am[-1]


for i in range(len(cksum_am)):
	cksum_am[i] = cksum_am[i].split()
	cksum_am[i][2] = cksum_am[i][2][8:]

for i in range(len(cksum_vm)):
	cksum_vm[i] = cksum_vm[i].split()

cksum_am.sort(key=lambda x: x[2])
cksum_vm.sort(key=lambda x: x[2])

for line in cksum_am:
	print line

for line in cksum_vm:
	print line

#print "h - 5"

print "Vagrant checksums for \"/bin\", \"/etc\" :"
for cksum in cksum_vm:
	b = 'nf'
	for i in cksum_am:
		if i[2] == cksum[2]:
			b = 'wr'
		if i == cksum:
			b = 'ok'
	if b == 'ok':
		print '\033[92m' + '[' + b + '] ' + '\033[0m' + cksum[2]
	if b == 'wr':
		print '\033[91m' + '[' + b + '] ' + '\033[0m' + cksum[2]
	if b == 'nf':
		print '\033[94m' + '[' + b + '] ' + '\033[0m' + cksum[2]