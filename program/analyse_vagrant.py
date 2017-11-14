import subprocess 
import os
from subprocess import call
import pexpect

print "analyse_vagrant.py"

const_box = "ubuntu/xenial64"
const_synced_folder = "/home/ivan/Documents/lh_project2018/hostrootfolder"

directory = os.getcwd()
directory = directory + "/vagrant_vm"

if not os.path.exists(directory):
    os.makedirs(directory)

os.chdir(directory);

print directory

#child_vagrant = pexpect.spawn("vagrant ssh", timeout=None)
#child_vagrant.expect("ubuntu-xenial", timeout=None)
#child_vagrant.sendline("cat /vagrant/Vagrantfile")
#print child_vagrant.before
#child_vagrant.expect("ubuntu-xenial", timeout=None)
#print child_vagrant.before
#child_vagrant.close()