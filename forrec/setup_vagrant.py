import subprocess 
import os
from subprocess import call
import pexpect

const_box = "ubuntu/xenial64"
const_synced_folder = "/home/ivan/Documents/cpHostRootFolder/hostrootfolder"

directory = os.getcwd()

if not os.path.exists(directory + "/vagrant_vm"):
    os.makedirs(directory + "/vagrant_vm")

os.chdir(directory + "/vagrant_vm");

call(["vagrant","init",const_box])

# myfile = open('Vagrantfile', 'r')
# data = myfile.read().split('\n')
# 
# print data
# 
# 
# data[-2] = ""
# data[-1] = "\tconfig.vm.synced_folder \"" + const_synced_folder + "\"" + " , \"/analyse\""
# data.append("")
# data.append("end")
# data.append("")
# 
# myfile = open('Vagrantfile', 'w')
# for line in data:
#   myfile.write("%s\n" % line)
# 
# myfile.close()

call(["vagrant","up"])
