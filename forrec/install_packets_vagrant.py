import subprocess 
import os
from subprocess import call
import pexpect

const_box = "ubuntu/xenial64"
const_synced_folder = "/home/ivan/Documents/cpHostRootFolder/hostrootfolder"

directory = os.getcwd()
directory = directory + "/vagrant_vm"

os.chdir(directory);

data = subprocess.check_output(["dpkg", "-l", "--root=" + const_synced_folder])

data = data.splitlines()

del data[0:5]

packets = ''

for line in data:
	
	line = line.split()
	line = line[1] + '=' + line[2]
	packets = packets + line + ' '

packets = packets.split();

child = pexpect.spawn("vagrant ssh", timeout=None)
child.expect("ubuntu-xenial", timeout=None)
child.sendline("sudo su")
child.expect("ubuntu-xenial", timeout=None)
child.sendline("control=\"forrec - continue\"")
child.expect("ubuntu-xenial", timeout=None)
child.sendline("cd /")
child.expect("ubuntu-xenial", timeout=None)

for line in packets:
	print "\033[96mapt-get install -y " + line +" << "+ "\033[0m"
	child.sendline("apt-get install -y " + line + "; echo $control")
	output = ""
	while "forrec - continue" not in output:
	    child.expect('\n')
	    output = child.before
	    print output


print "\033[92m -Ready-"