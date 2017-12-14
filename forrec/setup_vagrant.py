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

call(["vagrant","up"])
