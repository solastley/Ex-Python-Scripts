import sys
import os
import fileinput

arg1 = raw_input('Enter the cluster name: ')
arg2 = raw_input('Enter the number of solvent molecules')

path1 = '/ihome/jkeith/ssa35/work/ABCluster/ABCluster-Linux/' + arg1 + '/' + arg1 + '_' + arg2 + 'ch3oh/' + arg1 + '_' + arg2 + 'ch3oh-PM7/'

path2 = '/ihome/jkeith/ssa35/bin/python/test.txt'
path3 = '/ihome/jkeith/ssa35/bin/python/test2.txt'

for i in range(100):
	fileToRead = path1 + str(i) + '/coord.out'
	with open(fileToRead, 'r') as inFile:
		for line in inFile:
			if 'HEAT OF FORMATION' in line:
				lines = line.split()
				with open(path2, 'a') as outFile:
					outFile.write(str(i) + '\t' + lines[5] + '\n')

class EnergyObject(object):
	index = ""
	energy = 0

def makeEnergyObject(index, energy):
	myObject = EnergyObject()
	myObject.index = index
	myObject.energy = float(energy)
	return myObject

energy_array = []
with open(path2, 'r') as inFile:
	for line in inFile:
		info = line.split()
		newObject = makeEnergyObject(info[0], info[1])
		energy_array.append(newObject)

sorted_array = sorted(energy_array, key=lambda x: x.energy)
with open(path3, 'w') as outFile:
	for item in sorted_array:
		outFile.write(item.index + '\t' + str(item.energy) + '\n')

with open(path3, 'r') as inFile:
	ref_file = inFile.next().split()[0]

os.remove(path2)
os.remove(path3)

path4 = path1 + ref_file + '/' + ref_file + '.xyz'
x_coord_ref = []
y_coord_ref = []
z_coord_ref = []
with open(path4, 'r') as inFile:
	num_atoms = int(inFile.next())
	inFile.next()
	for i in range(num_atoms):
		lines = inFile.next().split()
		x_coord_ref.append(float(lines[1]))
		y_coord_ref.append(float(lines[2]))
		z_coord_ref.append(float(lines[3]))

class RMSDObject(object):
	index = ""
	energy = 0
	rmsd = 0

def makeRMSDObject(index, energy, rmsd):
	myObject = RMSDObject()
	myObject.index = index
	myObject.energy = energy
	myObject.rmsd = float(rmsd)
	return myObject

path5 = path1 + 'unranked.txt'
with open(path5, 'w') as inFile:
	inFile.write('index\tenergy\t\trmsd\n')

rmsd_array = []
for i in range(100):
	x_coord = []
	y_coord = []
	z_coord = []
	fileToRead = path1 + str(i) + '/' + str(i) + '.xyz'
	with open(fileToRead, 'r') as inFile:
		num_atoms = int(inFile.next())
		inFile.next()
		for j in range(num_atoms):
			lines = inFile.next().split()
			x_coord.append(float(lines[1]))
			y_coord.append(float(lines[2]))
			z_coord.append(float(lines[3]))
	total_x = 0
	total_y = 0
	total_z = 0
	for j in range(len(x_coord)):
		total_x = total_x + (x_coord[j] - x_coord_ref[j])**2
		total_y = total_y + (y_coord[j] - y_coord_ref[j])**2
		total_z = total_z + (z_coord[j] - z_coord_ref[j])**2
	x_rmsd = (total_x / len(x_coord)) ** 0.5
	y_rmsd = (total_y / len(y_coord)) ** 0.5
	z_rmsd = (total_z / len(z_coord)) ** 0.5
	RMSD = (x_rmsd + y_rmsd + z_rmsd) / 3
	newObject = makeRMSDObject(i, energy_array[i].energy, RMSD)
	rmsd_array.append(newObject)
	with open(path5, 'a') as inFile:
		inFile.write(energy_array[i].index + '\t' + str(energy_array[i].energy) + '\t' + str(RMSD) + '\n')

path6 = path1 + 'rankedByEnergy.txt'
sorted_array = sorted(rmsd_array, key=lambda x: x.energy)
with open(path6, 'w') as outFile:
	outFile.write('index\tenergy\t\trmsd\n')
	for item in sorted_array:
		outFile.write(str(item.index) + '\t' + str(item.energy) + '\t' + str(item.rmsd) + '\n')

path7 = path1 + 'rankedByRMSD.txt'
sorted_array = sorted(rmsd_array, key=lambda x: x.rmsd)
with open(path7, 'w') as outFile:
	outFile.write('index\tenergy\t\trmsd\n')
	for item in sorted_array:
		outFile.write(str(item.index) + '\t' + str(item.energy) + '\t' + str(item.rmsd) + '\n')

