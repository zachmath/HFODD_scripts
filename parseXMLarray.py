import xml.etree.ElementTree as ET
import numpy as np
import re, os

#-------------------------------------------------#
#               Read in the data                  #
#-------------------------------------------------#

tree = ET.parse('pu240_mesh2D_q20q30_NEWinertia_borderNorth1_SKMS_T0.00_PES.xml')
#tree = ET.parse('shorter_sample.xml')
root = tree.getroot()

#-------------------------------------------------#
# First you should pick out the global properties #
#-------------------------------------------------#

#Find the EDF, the nucleus, perhaps the temperature?

print_array = []

for line in root[0][1].iter('constraint'):
    print_array.append( line.get('type') )

print_array.append( 'EHFB' )

#-------------------------------------------------#
# Next you should form an array(?) of all the points as independent trees #
#-------------------------------------------------#

points = root.findall("./PES/point")  # The xml tree 'points' contains addresses for each individual grid point


#-------------------------------------------------#
# Then, cycling through points, pick out energy, multipole moments, etc. #
#-------------------------------------------------#

for point in points:

    constraints = []                 # An array containing the multipole moments as strings without units

    for line in point.iter('constraint'):
        value = line.get('val')
        value = re.search('\D\d*\.\d*',value).group(0)
        constraints.append(value)

    energy = 0
    for line in point.iter('energies'):
        EHFB = line.get('EHFB')
        energy = re.search('\D\d*\.\d*',EHFB).group(0)
#        print energy

    row = constraints + [energy] # + [something else]

    print_array = np.vstack (( print_array, row ))


#-------------------------------------------------#
# Figure out what to do with the data you've generated #
#-------------------------------------------------#

#You can save the array as a file, but if you do that you'll have to figure out how to import the metadata from the first line or two separately from the rest of the file.

#OR you can just plug the data into a plot straightway, without saving to a file. This might be faster in the short term, but long-term it might pay off to generate the other file (so that you don't have to parse the whole document every time you want a different projection of the PES).

print_array = print_array.astype(str) # This converts the whole array back to the string, in case you decide you need it as float for some reason in between

col_width = max(len(word) for row in print_array for word in row) + 1  # padding
#for row in print_array:
#    print "".join(word.center(col_width) for word in row)

data_file = open('data.dat','w')
for row in print_array:
    data_file.write( "".join(word.center(col_width) for word in row) )
    data_file.write('\n')
data_file.close()
