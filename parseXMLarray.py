#
# For this to work with the new XML files, you'll have to find-replace 
# the 'energies' corresponding to pairing with something else, like 'penergies'
#

import xml.etree.ElementTree as ET
import numpy as np
import re, os

#-------------------------------------------------#
#               Read in the data                  #
#-------------------------------------------------#

infile = 'old_xml/Q30_PES.xml'#raw_input("\n Please list the name of the xml file: \n")

tree = ET.parse( infile )
#tree = ET.parse('pu240_mesh2D_q20q30_NEWinertia_borderNorth1_SKMS_T0.00_PES.xml')
#tree = ET.parse('shorter_sample.xml')
root = tree.getroot()

#-------------------------------------------------#
# First you should pick out the global properties #
#-------------------------------------------------#

#Find the EDF, the nucleus, perhaps the temperature?

#-------------------------------------------------#
#     Label the columns in your output files      #
#-------------------------------------------------#

print_array = []

for line in root[0][1].iter('constraint'):
    print_array.append( line.get('type') )

for line in root[0][1].iter('obs'):
    print_array.append( line.get('name') )

print_array.append( 'EHFB' )

print_array.append( 'qN' )

print_array.append( 'deltaN' )

print_array.append( 'deltaP' )

print_array.append( 'EpairN' )

print_array.append( 'EpairP' )

print_array.append( 'zN' )

print_array.append( 'Z1' )

print_array.append( 'A1' )

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

    for line in point.iter('obs'):
        value = line.get('val')
        value = re.search('\D\d*\.\d*',value).group(0)
        constraints.append(value)

    energy = 0
    for line in point.iter('energies'):
#    for line in point.iter('pairing/energies'): # Oh, but this is the term you DON'T want
        EHFB = line.get('EHFB')
        energy = re.search('\D\d*\.\d*',EHFB).group(0)

    for line in point.iter('neck'):
        neck = line.get('qN')
        qN = re.search('\D\d*\.\d*',neck).group(0)

    for line in point.iter('neck'):
        neck = line.get('zN')
        zN = re.search('\D\d*\.\d*',neck).group(0)

    for line in point.iter('gaps'):
        dN = line.get('deltaN')
        deltaN = re.search('\D\d*\.\d*[de][+-]\d*',dN).group(0)
        dP = line.get('deltaP')
        deltaP = re.search('\D\d*\.\d*[de][+-]\d*',dP).group(0)

    for line in point.iter('penergies'):
        EpN = line.get('EpairN')
        EpairN = re.search('\D\d*\.\d*[de][+-]\d*',EpN).group(0)
        EpP = line.get('EpairP')
        EpairP = re.search('\D\d*\.\d*[de][+-]\d*',EpP).group(0)

    for line in point.iter('identity'):
        z1 = line.get('Z1')
        Z1 = re.search('\D\d*\.\d*',z1).group(0)
        a1 = line.get('A1')
        A1 = re.search('\D\d*\.\d*',a1).group(0)

    row = constraints + [energy] + [qN] + [deltaN] + [deltaP] + [EpairN] + [EpairP] + [zN] + [Z1] + [A1] # + [something else]

    print_array = np.vstack (( print_array, row ))


#-------------------------------------------------#
# Figure out what to do with the data you've generated #
#-------------------------------------------------#

print_array = print_array.astype(str) # This converts the whole array back to the string, in case you decide you need it as float for some reason in between

col_width = max(len(word) for row in print_array for word in row) + 1  # padding
#for row in print_array:
#    print "".join(word.center(col_width) for word in row)

data_file = open('data.dat','w')
for row in print_array:
    data_file.write( "".join(word.center(col_width) for word in row) )
    data_file.write('\n')
data_file.close()
