###############################################################################
# This script will collect whatever outputs you have recorded in your PES XML #
# file, and generate the hfodd_path files you'll need to generate satellite   #
# points around each point in your PES using HFODD. Once the HFODD run is     #
# completed, use the "post-run" script to collect and rename the output files #
# into a folder where they can be used in the inertia code.                   #
###############################################################################

import xml.etree.ElementTree as ET
import numpy as np
import re, os, time


current_directory = os.getcwd()
root_name = current_directory.rpartition('/')
PES_file = root_name[2] + '_PES.xml'

#-------------------------------------------------#
#    In the preliminary matter, set the parameter #
#    defining the precision of your numerical     #
#    derivative; for instance:                    #
#        dx = d_q20, dy = d_q30, dz = d_q22       #
#    Also list the name of the XML file           #
#-------------------------------------------------#

num_constraints = 2 # Number of constraints in the PES
nNeighbors = 2*num_constraints # Number of neighboring points used in the derivative

dx = 0.001 # This is the amount your multipole constraints will change as you calculate nearby points to numerically compute the derivative of the density with respect to your multipole moments


#-------------------------------------------------#
#             Read in the XML data                #
#-------------------------------------------------#

os.chdir("out-archive")

tree = ET.parse('%s' %PES_file)
root = tree.getroot()

os.chdir(os.pardir)

#-------------------------------------------------#
#           Read in hfodd_path_new.d              #
#-------------------------------------------------#

# Read the file and store all lines in a list
fread = open('hfodd_path_constraints.d','r')
newPathLines = fread.readlines()
fread.close()


#-------------------------------------------------#
#             Some useful modules                 #
#-------------------------------------------------#

def not_empty(chaine): return chaine != ''

def breakLine(element):
    currentLine  = re.split("\n",element)
    brokenLine   = re.split(" ",currentLine[0])
    strippedLine = filter(not_empty, brokenLine)
    return strippedLine

#-------------------------------------------------------------#
#   Make a list of all constraints used in this calculation   #
#-------------------------------------------------------------#

numConstraints = int( breakLine( newPathLines[0] )[0] ) 

listConstraints = ['q10']

for i in range(0,numConstraints):
    lam = int( breakLine( newPathLines[1] )[3*i] )
    mu = int( breakLine( newPathLines[1] )[3*i+1] )
    if mu==2:
        if lam==2:
            constraint = 'q22'
        else:
            print "ERROR: Multipole moment q%s2 not allowed" %lam
    elif mu==0:
        if lam==1:
            constraint = 'q10'
        elif lam==2:
            constraint = 'q20'
        elif lam==3:
            constraint = 'q30'
        elif lam==4:
            constraint = 'q40'
        elif lam==5:
            constraint = 'q50'
        elif lam==6:
            constraint = 'q60'
        elif lam==7:
            constraint = 'q70'
        elif lam==8:
            constraint = 'q80'
        else:
            print "ERROR: Multipole moment q%s0 not allowed" %lam
    listConstraints.append(constraint)

#-------------------------------------------------------------------------#
# Next you should form an array(?) of all the points as independent trees #
#-------------------------------------------------------------------------#

points = root.findall("./PES/point")  # The xml tree 'points' contains addresses for each individual grid point
numPoints = len(points)

#----------------------------------------------------------------#
#        Then, cycling through points, pick out multipole        #
#            moments, etc., and write to hfodd_path.d            #
#----------------------------------------------------------------#

data_file = open('hfodd_path.d','w')
data_file2= open('hfodd_path_new.d','w')

data_file.write("%d %d \n" %(numConstraints, numPoints) ) 
data_file2.write("%d %d \n" %(numConstraints, numPoints*nNeighbors) ) # This doesn't seem to work if Q_10 is a constraint in your original file

lineCounter=0

for point in points:

    for line in point.iter('file'):
        oldindex = line.get('name')     # "nom" typically has the form "hfodd_000002.out"
    oldindex = oldindex.split('_')[1]
    oldindex = oldindex.split('.')[0]

    qtypes = ['q10']
    values = [0.0]

    for line in point.iter('constraint'):
        qtype = line.get('type')
        qtypes.append(qtype)
        value = line.get('val')
        value = re.search('\D\d*\.\d*',value).group(0)
        values.append(value)

    newLine = ['1 0    0.0  ']

    for i in range( 1, len(qtypes) ):
        for j in range(0, len(listConstraints) ):
            if qtypes[i]==listConstraints[j]:
                lam = qtypes[i][1]
                mu = qtypes[i][2]
                valToAdd = str(round(float(values[i]),1))
                addition='%1s %1s %8s ' %(lam, mu, valToAdd )
                newLine.append(addition)

#-----------------------------------------------------------#
# Implicit in these lines is the understanding that you     #
#  are doing a PES in the Q20-Q30 plane                     #
#-----------------------------------------------------------#

                if (lam=='3') & (mu=='0'):
                    q30 = round(float(values[i]))
                elif lam=='2' and mu=='0':
                    q20 = round(float(values[i]))
                else:
                    pass


    data_file.write( "".join(word.center(1) for word in newLine) )
    data_file.write('\n')
    lineCounter+=1
    archiveIndex = str(q20).zfill(3) + str(q30).zfill(3)

    for line in range( 1, nNeighbors+1 ):
        newLine2 = ['1 0    0.0  ']

        for k in range( 1, len(qtypes) ):
            lam = qtypes[k][1]
            mu = qtypes[k][2]

            if( (line-1)/2 == (k-1) ):
                if( line % 2 == 0):
                    addition='%1s %1s %8.3f  ' %(lam, mu, float(values[k])+dx)
                else:
                    addition='%1s %1s %8.3f  ' %(lam, mu, float(values[k])-dx)
            else:
                addition='%1s %1s %8.3f  ' %(lam, mu, float(values[k]) )

            newLine2.append(addition)

        data_file2.write( "".join(word.center(1) for word in newLine2) )
        data_file2.write('\n')

data_file.close()
data_file2.close()

