import os
import sys
import fileinput

arg = raw_input('Enter the molecule name: ')

path1 = '/ihome/jkeith/ssa35/work/PM7/' + arg + '/' + arg + '.xyz'
path2 = '/ihome/jkeith/ssa35/work/PM7/' + arg + '/' + arg + '.out'
path3 = '/ihome/jkeith/ssa35/work/PM7/' + arg + '/' + arg + '.str'
path4 = '/ihome/jkeith/miv22/ABC-solomon/ABCgen/para.rtf'
path5 = '/ihome/jkeith/ssa35/work/ABCluster/ABCluster-Linux/charmfiles/' + arg + 'charm.xyz'

f1 = open(path1, 'r')
numAtoms = f1.next()
f1.close()

f2 = open(path2, 'r')
lines = iter(f2)

filedata = '' + numAtoms + arg + '\n'
foundFirst = False
for line in lines:
	try:
		if 'CARTESIAN COORDINATES' in line and not foundFirst:
			foundFirst = True
		elif 'CARTESIAN COORDINATES' in line and foundFirst:
			lines.next()
			for item in range(int(numAtoms)):
				tokens = lines.next().split()
				filedata = filedata + tokens[1] + '\t' + tokens[2] + '\t' + tokens[3] + '\t' + tokens[4] + '\n'
	except (StopIteration):
		pass
f2.close()

filedata = filedata + 'all36_cgenff  q  epsilon (kJ/mol) sigma (AA)\n'

f3 = open(path3, 'r')
lines = iter(f3)

for line in lines:
	if 'RESI' in line:
		lines.next()
		break
	lines.next()

atomtypes = []
charges = []

for line in range(int(numAtoms)):
	tokens = lines.next().split()
	atomtypes.append(tokens[2])
	charges.append(tokens[3])

f3.close()

f4 = open(path4, 'r')
filedata2 = f4.readlines()

sigma = []
epsilon = []
for i in range(len(atomtypes)):
	for line in filedata2:
		if atomtypes[i] in line:
			tokens = line.split()
			epsilon.append(tokens[2])
			sigma.append(tokens[3])
			break
f4.close()

epsilonfloat = []
sigmafloat = []
for i in range(len(epsilon)):
	epsilonfloat.append(float(epsilon[i]))
	sigmafloat.append(float(sigma[i]))

for i in range(len(epsilonfloat)):
	epsilonfloat[i] = epsilonfloat[i] * -4.184
	sigmafloat[i] = sigmafloat[i] * 1.781797

f5 = open(path5, 'w')
f5.write(filedata)
for i in range(len(atomtypes)):
	f5.write(charges[i] + ' ' + str(epsilonfloat[i]) + ' ' + str(sigmafloat[i]) + ' # ' + atomtypes[i] + '\n')
f5.close()
