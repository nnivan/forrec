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
# child.logfile = open("python_vagrant.log", "w")
# child.sendline("find /analyse/bin /analyse/etc -type f 2>/dev/null | xargs cksum 2>/dev/null")
# child.expect("ubuntu-xenial", timeout=None)
# child.expect("ubuntu-xenial", timeout=None)
# 
# datafile = open('python_vagrant.log', 'r')
# cksum_am=datafile.read()
# print cksum_am
# datafile.close()


process = subprocess.Popen(["find", const_synced_folder+"/bin", const_synced_folder+"/etc", "-type", "f"],stdout=subprocess.PIPE)
cksum_am = process.communicate()[0]

cksum_am = cksum_am.splitlines();
for i in range(len(cksum_am)):
	cksum_am[i] = subprocess.check_output(["cksum", cksum_am[i]])
	cksum_am[i] = cksum_am[i].split()
	cksum_am[i][2] = cksum_am[i][2][len(const_synced_folder):]

cksum_am.sort(key=lambda x: x[2])


child = pexpect.spawn("vagrant ssh", timeout=None)
child.expect("ubuntu-xenial", timeout=None)
child.sendline("sudo find /bin /etc -type f | xargs cksum > /vagrant/cksums_vagrant_virtual_machine.log")
child.expect("ubuntu-xenial", timeout=None)

datafile = open(directory + "/cksums_vagrant_virtual_machine.log", 'r')
cksum_vm=datafile.read()
datafile.close()

cksum_vm = cksum_vm.splitlines();

for i in range(len(cksum_vm)):
	cksum_vm[i] = cksum_vm[i].split()

cksum_vm.sort(key=lambda x: x[2])

print "Vagrant checksums for \"/bin\", \"/etc\" :"
for cksum in cksum_am:
	b = 'nf'
	for i in cksum_vm:
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