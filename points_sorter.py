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
convergenceCriterion = 1

for point in points:
    index = point.get('id')

    for line in point.iter('neck'):
        value = line.get('qN')
        value = re.search('\D\d*\.\d*',value).group(0)
        value = float(value)
#        print abs(value)

        if abs(value) <= convergenceCriterion:
            print index
        else:
#            print 'not %f' %abs(value)
            continue

print counter
