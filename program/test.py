import subprocess 
import os
from subprocess import call
import pexpect


data = subprocess.check_output(['dpkg', '-l']);

data = data.splitlines();

del data[0:5]

directory = os.getcwd()
directory = directory + "/vagrant"

if not os.path.exists(directory):
    os.makedirs(directory)

os.chdir(directory);

#call(["vagrant","init","ubuntu/xenial64"])
call(["vagrant","up"])
#wtf I do now??? - #call(["vagrant","ssh"])


child = pexpect.spawn("vagrant ssh")
child.expect("ubuntu@ubuntu-xenial")
child.sendline("sudo su")
print child.before

child.expect("root", timeout=None)
child.sendline("apt-get update")

print child.before

for line in data:
	line = line.split()
	line = line[1] + '=' + line[2]
	child.expect("root", timeout=None)
	print "sudo apt-get install " + line + " -y"
	child.sendline("apt-get install " + line + " -y")
	print child.before

child.expect("ubuntu", timeout=None)
child.sendline("exit")

call(["vagrant","halt"])