import os
import sys
import fileinput

arg = raw_input('Enter the molecule name: ')

path1 = '/ihome/jkeith/ssa35/work/PM7/' + arg + '/' + arg + '.xyz'
path2 = '/ihome/jkeith/ssa35/work/PM7/' + arg + '/' + arg + '.out'
path3 = '/ihome/jkeith/ssa35/work/PM7/' + arg + '/' + 'final' + arg + '.xyz'

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

f3 = open(path3, 'w')
f3.write(filedata)
f3.close()
