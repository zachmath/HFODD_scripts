##########################################################
# Right now this script is only configured to index QP   #
# files according to their Q20 and Q30 multipole values, #
# so if you were to probe, say, the Q22 direction, this  #
# script would create a lot of files with redundant      #
# (indistinguishable) filenames. It should be fairly     #
# straightforward to adapt, but just be aware.           #
# It also assumes that the satellite points are equally- #
# spaced from the centerpoint in all cases and in all    #
# directions. This primarily affects the calculation of  #
# the Lagrange coefficients.                             #
##########################################################

import numpy as np                                                                
import os, subprocess, re, shutil
import xml.etree.ElementTree as ET
import errno, math


parent_directory = os.getcwd()

num_constraints = 2 # Number of constraints in the PES (not counting Q10 - just the ones that get varied to calculate the inertia)
nNeighbors = 2*num_constraints # Number of neighboring points used in the derivative

dx = 0.001 # This is the amount your multipole constraints will change as you calculate nearby points to numerically compute the derivative of the density with respect to your multipole moments
lagcoeff = 1/(2*dx)

dir_centerpoints = parent_directory + 'qp-archive'
dir_satellites =  parent_directory + 'qp-archive'
dir_inertia = parent_directory + 'test_qp_folder'
try: 
    os.makedirs(dir_inertia)
except OSError:
    if not os.path.isdir(dir_inertia):
        raise


data_file = open('toto.txt','w')
for i in range(0, num_constraints):
    data_file.write("%10.3f  000.000000  %10.3f \n" %(-lagcoeff, lagcoeff) )

#######################################################
#   Right now the satellite points are listed         #
#   sequentially, but you WANT them listed by their   #
#   multipole constraints. Do that by reading the     #
#   hfodd_path_new.d file. The line number in that    #
#   file should correspond to the index of the QP     #
#   file.                                             #
#######################################################


#-------------------------------------------------#
#           Read in hfodd_path_new.d              #
#-------------------------------------------------#

# Read the file and store all lines in a list
fread = open('hfodd_path_new.d','r')
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
numSatellites = int( breakLine( newPathLines[0] )[1] ) 

for j in range(1, numSatellites+1):
    flag = ''
    for i in range(0,numConstraints):
        lam = int( breakLine( newPathLines[j] )[3*i] )
        mu = int( breakLine( newPathLines[j] )[3*i+1] )
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
                q20 = float( breakLine( newPathLines[j] )[3*i + 2] )
                q20_root = int(round(q20, 0))
                if q20 > float(q20_root):
                    flag = 'q20plus'
                elif q20 < q20_root:
                    flag = 'q20minus'
                else:
                    pass
            elif lam==3:
                constraint = 'q30'
                q30 = float( breakLine( newPathLines[j] )[3*i + 2] )
                q30_root = int(round(q30, 0))
                if q30 > float(q30_root):
                    flag = 'q30plus'
                elif q30 < q30_root:
                    flag = 'q30minus'
                else:
                    pass
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

#######################################################
#   Once you've selected a particular line from the   #
#   path file, you can break it apart to determine    #
#   the coordinates of the center point (by rounding  #
#   the constraints to the nearest integer). This'll  #
#   be enough to write the root filename              #
#######################################################

    root_index = str(q20_root).zfill(3) + str(q30_root).zfill(3) 
    root_file = 'HFODD_' + str( root_index ).zfill(8) + '.QP'
    sat_file = root_file + flag 

#######################################################
#   Move all the centerpoint QP files to some folder  #
#   and record them in the inertia input file         #
#######################################################

    if j % nNeighbors == 0: # We only need to do this once, per centerpoint, not for every single satellite
        data_file.write(root_file + '\n')
        shutil.copy2(root_file, dir_inertia)

#######################################################
# Move all the satellite QP files to that same folder #
#######################################################

    shutil.copy2(sat_file, dir_inertia)

data_file.close()
shutil.copy2('toto.txt', dir_inertia)
