import os
import sys
import fileinput

#prompts user for molecule name
arg = raw_input('Enter the molecule name: ')

path1 = '/ihome/jkeith/ssa35/work/MP2_Orca/' + arg + '/final' + arg + '.xyz'
path2 = '/ihome/jkeith/ssa35/work/ABCluster/ABCluster-Linux/' + arg + '/' + arg + '.str'
path3 = '/ihome/jkeith/miv22/ABC-solomon/ABCgen/para.rtf'
path4 = '/ihome/jkeith/ssa35/work/ABCluster/ABCluster-Linux/' + arg + '/' + arg + 'charm.xyz'

#opens up xyz file and reads data from it
filedata = ''
f = open(path1, 'r')
lines = iter(f)

#gets number of atoms string from xyz data
num_atoms = lines.next()
#skips over blank line
lines.next()

#creates string with all of the xyz data
for line in lines:
	filedata = filedata + line

f.close()

#opens up str file
f2 = open(path2, 'r')

#creates array of strings from str file lines
lines2 = iter(f2)

#for each line in str file
for line in lines2:
	#if the keyword GROUP is in the line, stop iterating
	if 'RESI' in line:
		lines2.next()
		break
	#if it didn't break out, skip next line
	lines2.next()

#makes two arrays for atom types and charges
atomtypes = []
charges = []

#for every line in the important data
for line in range(int(num_atoms)):
	#creates an array of strings by splitting the file line
	tokens = lines2.next().split()
	#appends parts of the file line to their respective arrays
	atomtypes.append(tokens[2])
	charges.append(tokens[3])

f2.close()

#opens file that contains sigma and epsilon values for atom codes
f3 = open(path3, 'r')
filedata3 = f3.readlines()

sigma = []
epsilon = []
#for each atom type
for i in range(len(atomtypes)):
	#for each line in the file
	for line in filedata3:
		#if the line contains the name of the atom type
		if atomtypes[i] in line:
			#append the sigma and epsilon values to their arrays
			tokens = line.split()
			epsilon.append(tokens[2])
			sigma.append(tokens[3])
			break
f3.close()

#creates new epsilon and sigma arrays and casts strings from old array into floats (NOT WORKING)
epsilonfloat = []
sigmafloat = []
for i in range(len(epsilon)):
	epsilonfloat.append(float(epsilon[i]))
	sigmafloat.append(float(sigma[i]))

#Note to Minh -- For some reason, the block of code above this comment is changing the values when it casts the strings into floats

#multiplies the epsilon and sigma values by constants
for i in range(len(epsilonfloat)):
	epsilonfloat[i] = epsilonfloat[i] * -4.184
	sigmafloat[i] = sigmafloat[i] * 1.781797

#creates a file to write to in the appropriate directory
f4 = open(path4, 'w')
#writes number of atoms at the top
f4.write(num_atoms)
#writes the name of the compound
f4.write(arg + '\n')
#writes the xyz coordinates
f4.write(filedata)
#writes comment in code for easy reading
f4.write('all36_cgenff  q  epsilon (kJ/mol) sigma (AA) \n')

#for each atom type
for i in range(len(atomtypes)):
	#writes the charge, epsilon value, sigma value, and atom type to the file
	f4.write(charges[i] + ' ' + str(epsilonfloat[i]) + ' ' + str(sigmafloat[i]) + ' # ' + atomtypes[i] + '\n')

f4.close()
