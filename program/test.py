import subprocess 
data = subprocess.check_output(['dpkg', '-l']);

data = data.splitlines();

del data[0:5]

for line in data:
	line = line.split()
	print line[1] , line[2]
