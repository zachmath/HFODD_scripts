import xml.etree.ElementTree as ET
import numpy as np
import re, os, time


current_directory = os.getcwd()
root_name = current_directory.rpartition('/')
fichier_PES = root_name[2] + '_PES.xml'

q20_spacing = 2
q30_spacing = 2
rowMax = 75


#-------------------------------------------------#
#             Read in the XML data                #
#-------------------------------------------------#

os.chdir("out-archive")

#infile = raw_input("\n Please list the name of the xml file: \n")
#tree = ET.parse( infile )
tree = ET.parse('%s' %fichier_PES)
root = tree.getroot()

os.chdir(os.pardir)

#-------------------------------------------------#
#             Some useful modules                 #
#-------------------------------------------------#

def not_empty(chaine): return chaine != ''

def breakLine(element):
    currentLine  = re.split("\n",element)
    brokenLine   = re.split(" ",currentLine[0])
    strippedLine = filter(not_empty, brokenLine)
    return strippedLine

#-------------------------------------------------------------------------#
# Next you should form an array(?) of all the points as independent trees #
#-------------------------------------------------------------------------#

points = root.findall("./PES/point")  # The xml tree 'points' contains addresses for each individual grid point
numPoints = len(points)

#----------------------------------------------------------------#
#        Then, cycling through points, pick out multipole        #
#            moments, etc., and write to hfodd_path.d            #
#----------------------------------------------------------------#

print_array = ['Old file is being moved to new file']

for point in points:

    for line in point.iter('file'):
        oldindex = line.get('name')     # "nom" typically has the form "hfodd_000002.out"
#    print(oldindex)
    oldindex = oldindex.split('_')[1]
    oldindex = oldindex.split('.')[0]
    oldindex = int(oldindex)

    for line in point.iter('constraint'):
        qtype = line.get('type')
        value = line.get('val')
        value = re.search('\D\d*\.\d*',value).group(0)
#        print(qtype, value)
        if qtype == 'q20':
            q20 = int(round(float(value),0))
        elif qtype == 'q22':
            q22 = int(round(float(value),0))
        elif qtype == 'q30':
            q30 = int(round(float(value),0))
        else:
            print 'Error!!'


#    archiveIndex = (q30 / q30_spacing) * rowMax + (q20 / q20_spacing + 1)
#    q30 = oldindex/rowMax * q30_spacing
#    q20 = (oldindex - 1 - (oldindex/rowMax * rowMax) ) * q20_spacing
    archiveIndex = str(q20).zfill(3) + str(q22).zfill(3) + str(q30).zfill(3)

    oldRec = 'HFODD_' + str(oldindex).zfill(9) + '.REC'
    archiveRec = 'HFODD_' + str(int(archiveIndex)).zfill(9) + '.REC-bak'

    oldOut = 'hfodd_' + str(oldindex).zfill(9) + '.out'
    archiveOut = 'hfodd_' + str(int(archiveIndex)).zfill(9) + '.out-bak'

    oldQP = 'HFODD_' + str(oldindex).zfill(9) + '.QP'
    archiveQP = 'HFODD_' + str(int(archiveIndex)).zfill(9) + '.QP-bak'

    oldLoc = 'local_' + str(oldindex).zfill(9) + '.out'
    archiveLoc = 'local_' + str(int(archiveIndex)).zfill(9) + '.out-bak'

    print oldQP, 'is being moved to', archiveQP

    row = oldQP + ' is being moved to ' + archiveQP

    print_array = np.vstack (( print_array, row ))
#----------------------------------------------------------------#
#        Rename the .REC files, which are currently indexed      #
#        according to hfodd_path_new.d, according to their       #
#                   new indices in hfodd_path.d                  #
#----------------------------------------------------------------#

#    os.system('mv rec-archive/%s rec-archive/%s' %(oldRec, archiveRec))
#    os.system('hsi "cd 294Og/3D/rec-archive/; cput rec-archive/%s : %s"' %(oldRec, oldRec))
    os.system('mv out-archive/%s out-archive/%s' %(oldOut, archiveOut))

# To remove four characters from the end of the string use ${var%????}
print_array = print_array.astype(str) # This converts the whole array back to the string, in case you decide you need it as float for some reason in between

col_width = max(len(word) for row in print_array for word in row) + 1  # padding

data_file = open('post-reindex.out','w')
for row in print_array:
    data_file.write( "".join(word.center(col_width) for word in row) )
    data_file.write('\n')
data_file.close()
