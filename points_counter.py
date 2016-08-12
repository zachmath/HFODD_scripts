import xml.etree.ElementTree as ET
import numpy as np
import re, os

#-------------------------------------------------#
#               Read in the data                  #
#-------------------------------------------------#

infile = '176Pt-fission_PES.xml'
#infile = raw_input("\n Please list the name of the xml file: \n")

tree = ET.parse( infile )
#tree = ET.parse('pu240_mesh2D_q20q30_NEWinertia_borderNorth1_SKMS_T0.00_PES.xml')
#tree = ET.parse('shorter_sample.xml')
root = tree.getroot()

#-------------------------------------------------#
# Next you should form an array(?) of all the points as independent trees #
#-------------------------------------------------#

points = root.findall("./PES/point")  # The xml tree 'points' contains addresses for each individual grid point

#-------------------------------------------------#
# Then, cycling through points, pick out energy, multipole moments, etc. #
#-------------------------------------------------#

counter = 0
convergenceCriterion = 3.e-2

for point in points:

    for line in point.iter('stability'):
        value = line.get('dE')
        value = re.search('\D\d*\.\d*e-\d*',value).group(0)
        value = float(value)
#        print abs(value)

        if abs(value) <= convergenceCriterion:
#            print abs(value)
            counter = counter + 1
        else:
#            print 'not %f' %abs(value)
            continue

print counter
