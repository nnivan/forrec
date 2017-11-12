import subprocess 
from subprocess import call
import pexpect

files_pc = subprocess.check_output(['find', '/bin', '-type', 'f'])
files_pc = files_pc.splitlines()

cksums_ps = [];

for file in files_pc:
	cksums_ps.append(subprocess.check_output(['cksum', file]).split())

print cksums_ps


