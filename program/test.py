import subprocess 
import os
from subprocess import call


data = subprocess.check_output(['dpkg', '-l']);

data = data.splitlines();

del data[0:5]

for line in data:
	line = line.split()
	line = line[1] + '=' + line[2]
	print line

directory = os.getcwd()
directory = directory + "/vagrant"

if not os.path.exists(directory):
    os.makedirs(directory)

os.chdir(directory);

#call(["vagrant","init","ubuntu/xenial64"])
call(["vagrant","up"])
#wtf I do now??? - #call(["vagrant","ssh"])

import pexpect

child = pexpect.spawn("vagrant ssh")
child.expect("ubuntu")
child.sendline("sudo su")
child.expect("root")
child.sendline("exit")
child.expect("ubuntu")
child.sendline("touch asdf.ivan")
child.expect("ubuntu")
child.sendline("exit")

call(["vagrant","halt"])