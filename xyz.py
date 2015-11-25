'''
This script transformed raw data files for coordinates of molecules in a research paper appendix
into usable .xyz coordinate files.
'''

import os
import sys
import fileinput

arg = raw_input('Please enter the molecule name: ')

path = '/ihome/jkeith/ssa35/work/MP2_Orca/' + arg + '/' + arg + '.xyz'
path2 = '/ihome/jkeith/ssa35/work/MP2_Orca/' + arg + '/' + arg + '2.xyz'

for line in open(path):
	if 'Singleton' in line:
		print 'This file was already converted!'
		sys.exit()

f = open(path, 'r')

f2 = open(path2, 'w')
for line in f:
	if len(line) > 1:
		f2.write(line)
f.close()
f2.close()

f = open(path2, 'r')
filedata = f.read()
f.close()

newdata = filedata.replace(',0,','\t')
newdata = newdata.replace(',0.,','\t0.00000\t')
newdata = newdata.replace(',','\t')

count = 0
for line in open(path2):
	count = count + 1

f = open(path, 'w')
f.write(str(count))
f.write('\n' + arg + ' - from Singleton\'s paper calculated using wB97X-D\n')

f.write(newdata)
f.close()

os.remove(path2)
