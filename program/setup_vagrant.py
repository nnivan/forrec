import subprocess 
import os
from subprocess import call

os_verion = "ubuntu/xenial64"
disk_location = "/home/ivan/Documents/hostrootfolder"

directory = os.getcwd()
directory = directory + "/vagrant_vm"

if not os.path.exists(directory):
    os.makedirs(directory)

os.chdir(directory);

call(["vagrant","init",os_verion])

myfile = open('Vagrantfile', 'r')
data = myfile.read().split('\n')

print data


data[-2] = ""
data[-1] = "\tconfig.vm.synced_folder \"" + disk_location + "\""
data.append("")
data.append("end")
data.append("")

myfile = open('Vagrantfile', 'w')
for line in data:
  myfile.write("%s\n" % line)