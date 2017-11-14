import subprocess 
import os
from subprocess import call

box = "ubuntu/xenial64"
synced_folder = "/home/ivan/Documents/lh_project2018/hostrootfolder"

directory = os.getcwd()
directory = directory + "/vagrant_vm"

if not os.path.exists(directory):
    os.makedirs(directory)

os.chdir(directory);

call(["vagrant","init",box])

myfile = open('Vagrantfile', 'r')
data = myfile.read().split('\n')

print data


data[-2] = ""
data[-1] = "\tconfig.vm.synced_folder \"" + synced_folder + "\"" + " , \"/analyse\""
data.append("")
data.append("end")
data.append("")

myfile = open('Vagrantfile', 'w')
for line in data:
  myfile.write("%s\n" % line)

myfile.close()

call(["vagrant","up"])

