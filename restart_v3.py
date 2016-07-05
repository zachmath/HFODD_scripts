import xml.etree.ElementTree as ET
import numpy as np
import re, os, time


current_directory = os.getcwd()
root_name = current_directory.rpartition('/')
fichier_PES = root_name[2] + '_PES.xml'


os.system('mv summary/* %s' % current_directory)

timestamp = time.strftime("%m-%d-%Y")
print timestamp

os.system('OUTDIR="$HOME/outputs/%s"; mkdir $OUTDIR' %timestamp )

#-------------------------------------------------#
#             Read in the XML data                #
#-------------------------------------------------#

os.chdir("out")

#infile = raw_input("\n Please list the name of the xml file: \n")
#tree = ET.parse( infile )
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

listConstraints = []

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

data_file.write("%d %d \n" %(numConstraints, numPoints) ) # This doesn't seem to work if Q_10 is a constraint in your original file

lineCounter=0

for point in points:

    for line in point.iter('fichier'):
        oldindex = line.get('nom')     # "nom" typically has the form "hfodd_000002.out"
    oldindex = oldindex.split('_')[1]
    oldindex = oldindex.split('.')[0]

    qtypes = []
    values = []

    for line in point.iter('constraint'):
        qtype = line.get('type')
        qtypes.append(qtype)
        value = line.get('val')
        value = re.search('\D\d*\.\d*',value).group(0)
        values.append(value)

    newLine = []

    for i in range( 0, len(qtypes) ):
        for j in range(0, len(listConstraints) ):
            if qtypes[i]==listConstraints[j]:
                lam = qtypes[i][1]
                mu = qtypes[i][2]
                addition='%1s %1s %11s ' %(lam, mu, values[i] )
                newLine.append(addition)


    data_file.write( "".join(word.center(1) for word in newLine) )
    data_file.write('\n')
    lineCounter+=1

    oldRec = 'HFODD_' + oldindex.zfill(8) + '.REC'
    newRec = 'HFODD_' + str(lineCounter).zfill(8) + '.REC'

    print oldRec, 'is being moved to', newRec

#----------------------------------------------------------------#
#        Rename the .REC files, which are currently indexed      #
#        according to hfodd_path_new.d, according to their       #
#                   new indices in hfodd_path.d                  #
#----------------------------------------------------------------#

    os.system('cp rec/%s restart/%s' %(oldRec, newRec))

data_file.close()

os.system('cp out/*.xml $HOME/outputs/%s' %(timestamp))
