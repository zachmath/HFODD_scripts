import xml.etree.ElementTree as ET
import numpy as np
import re, os, time


current_directory = os.getcwd()
root_name = current_directory.rpartition('/')
fichier_PES = root_name[2] + '_PES.xml'


#-------------------------------------------------#
#             Read in the XML data                #
#-------------------------------------------------#

os.chdir("out")

tree = ET.parse('%s' %fichier_PES)
root = tree.getroot()

os.chdir(os.pardir)

#-------------------------------------------------#
#           Read in hfodd_path_new.d              #
#-------------------------------------------------#

# Read the file and store all lines in a list
fread = open('hfodd_path_new.d','r')
newPathLines = fread.readlines()
fread.close()


#-------------------------------------------------#
#             Some useful functions               #
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

data_file = open('hfodd_path_converged.d','w')

data_file.write("%d %d \n" %(numConstraints+1, numPoints) ) # This doesn't seem to work if Q_10 is a constraint in your original file

rec_file = open('move_recs.sh','w')
out_file = open('move_outs.sh','w')
qp_file  = open('move_qps.sh','w')
safety_file  = open('safety.txt','w')

lineCounter=0

for point in points:

    for line in point.iter('file'):
        oldindex = line.get('name')     # "name" typically has the form "hfodd_000002.out"
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
        if qtype=="q30":
            rawQ30 = float(value)
            q30 = int(round(float(value),0))
        elif qtype=="q20":
            rawQ20 = float(value)
            q20 = int(round(float(value),0))
        elif qtype=="q22":
            rawQ22 = float(value)
            q22 = int(round(float(value),0))
        else:
            pass

    newLine = ['1 0    0.0  ']

    for i in range( 1, len(qtypes) ):
        for j in range(0, len(listConstraints) ):
            if qtypes[i]==listConstraints[j]:
                lam = qtypes[i][1]
                mu = qtypes[i][2]
                valToAdd = str(round(float(values[i]),1))
                addition='%1s %1s %8s  ' %(lam, mu, valToAdd )

                newLine.append(addition)


    data_file.write( "".join(word.center(1) for word in newLine) )
    data_file.write('\n')
    lineCounter+=1

    archiveIndex = str(q20).zfill(3) + str(q22).zfill(3) + str(q30).zfill(3)

    oldRec = 'HFODD_' + oldindex.zfill(8) + '.REC'
    archiveRec = 'HFODD_' + str(int(archiveIndex)).zfill(9) + '.REC'

    oldOut = 'hfodd_' + oldindex.zfill(6) + '.out'
    archiveOut = 'hfodd_' + str(int(archiveIndex)).zfill(9) + '.out'

    oldLocal = 'local_' + oldindex.zfill(6) + '.out'
    archiveLocal = 'local_' + str(int(archiveIndex)).zfill(9) + '.out'

    oldQP = 'HFODD_' + oldindex.zfill(8) + '.QP'
    archiveQP = 'HFODD_' + str(int(archiveIndex)).zfill(9) + '.QP'

#----------------------------------------------------------------#
#        Rename the .REC files, which are currently indexed      #
#        according to hfodd_path_new.d, according to their       #
#                   new indices in hfodd_path.d                  #
#----------------------------------------------------------------#

    rec_file.write('hsi "cd 294Og/3D-lambda15/rec-archive/; cput rec/%s : %s"' %(oldRec, archiveRec))
    rec_file.write('\n')

    out_file.write('cp out/%s /usr/workspace/wsb/fission/294Og/3D-lambda15/out-archive/%s' %(oldOut, archiveOut))
    out_file.write('\n')

    out_file.write('hsi "cd 294Og/3D-lambda15/out-archive/; cput out/%s : %s"' %(oldOut, archiveOut))
    out_file.write('\n')

    qp_file.write('hsi "cd 294Og/3D-lambda15/qp-archive/; cput qp/%s : %s"' %(oldQP, archiveQP))
    qp_file.write('\n')

    safety_file.write('%s with (q20,q22,q30)=( %f , %f , %f ) -> %s' %(oldOut, rawQ20, rawQ22, rawQ30, archiveOut))
    safety_file.write('\n')

rec_file.close()
out_file.close()
qp_file.close()
safety_file.close()
data_file.close()
