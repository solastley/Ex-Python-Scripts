'''
This script served to create .inp files for the ORCA program from .xyz files for individual molecules.
The keywords that are written at the top of the file can be modified for different QM calculations
to allow for calculations such as MP2, DTF, etc.
'''

import os
import sys
import fileinput

arg = raw_input('Enter the molecule name: ')

path = '/ihome/jkeith/ssa35/work/MP2_Orca/' + arg + '/' + arg + '.xyz'
path2 = '/ihome/jkeith/ssa35/work/MP2_Orca/' + arg + '/' + arg + '.inp'

filedata = ''
f = open(path, 'r')
lines = iter(f)
lines.next()
lines.next()
for line in lines:
	filedata = filedata + line
f.close()

f = open(path2, 'w')
f.write('! MP2 def2-SVP TightSCF Grid4 OPT NUMFREQ\n')
f.write('\n* xyz 0 1\n')
f.write(filedata)
f.write('*')
f.close()
