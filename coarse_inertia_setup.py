# If you have a PES and you want to compute the inertia using finite
# differences on the existing mesh, you can use this to set up the input
# files. First put all the files in a single folder, named according to
# "lambdaww_xxxyyyzzz.QP" where ww=10*lambda, xxx=q20, yyy=q22, zzz=q30.
#
# Make a list of all the files
# From bash: ls *.QP >> all_qp.txt


import numpy as np
import re, os, time

lambda_spacing = 5
q20_spacing = 6 
q22_spacing = 3
q30_spacing = 3
temperature = 0.0

#-------------------------------------------------#
#           Read in all_qp.txt                    #
#-------------------------------------------------#

# Read the file and store all lines in a list
fread = open('all_qp.txt','r')
allFiles = fread.readlines()
fread.close()

#-------------------------------------------------#
#             Some useful functions               #
#-------------------------------------------------#

def not_empty(chaine): return chaine != ''

def breakLine(element):
#    currentLine  = re.split("\n",element)
    currentLine = element
    lambda_part   = re.split("_",currentLine)[0]
    mylambda   = re.split("lambda",lambda_part)[1]
    multipole_part   = re.split("_",currentLine)[1]
    multipole_part   = re.split("\.",multipole_part)[0]
    q20 = multipole_part[0:3]
    q22 = multipole_part[3:6]
    q30 = multipole_part[6:9]
    return int(mylambda), int(q20), int(q22), int(q30)

def fileName(mylambda, q20, q22, q30):
    # Function goes here to make a filename, given a set of constraints
    myname = 'lambda' + str(mylambda) + '_' + str(q20).zfill(3) + str(q22).zfill(3) + str(q30).zfill(3) + '.QP'
    return myname

def chooseCoeffs(myfile, file_over, file_under, spacing):
    ifexists_over  = os.path.isfile(file_over)
    ifexists_under = os.path.isfile(file_under)
    if ifexists_over and ifexists_under:
        file1 = file_over + "\n"
        file2 = file_under + "\n"
        coeff1 = 1./(2*spacing)
        coeff2 = 0.0
        coeff3 = -1./(2*spacing)
    elif ifexists_over and not ifexists_under:
        file1 = file_over + "\n"
        file2 = myfile
        coeff1 = 1./(spacing)
        coeff2 = 0.0
        coeff3 = -1./(spacing)
    elif not ifexists_over and ifexists_under:
        file1 = myfile
        file2 = file_under + "\n"
        coeff1 = 1./(spacing)
        coeff2 = 0.0
        coeff3 = -1./(spacing)
    else:
        file1 = myfile
        file2 = myfile
        coeff1 = 0.0 # Or maybe nan
        coeff2 = 0.0
        coeff3 = 0.0
    return file1, file2, coeff1, coeff2, coeff3

#---------------------------------------------#
#   Pick a point from the list to work with   #
#---------------------------------------------#

index = 1
temperature = '{:010.5f}'.format(temperature)

for myfile in allFiles:
    mylambda, q20, q22, q30 = breakLine( myfile )

    file_array = [myfile]
    coeff_array = []

    # Q20
    name_over  = fileName( mylambda , q20 + q20_spacing , q22 , q30 )
    name_under = fileName( mylambda , q20 - q20_spacing , q22 , q30 )

    file1, file2, coeff1, coeff2, coeff3 = chooseCoeffs(myfile, name_over, name_under, q20_spacing)

    file_array.append(file1)
    file_array.append(file2)

    coeff_line = [coeff1, coeff2, coeff3]
    coeff_array.append(coeff_line)

    # Q22
    name_over  = fileName( mylambda , q20 , q22 + q22_spacing , q30 )
    name_under = fileName( mylambda , q20 , q22 - q22_spacing , q30 )

    file1, file2, coeff1, coeff2, coeff3 = chooseCoeffs(myfile, name_over, name_under, q22_spacing)

    file_array.append(file1)
    file_array.append(file2)

    coeff_line = [coeff1, coeff2, coeff3]
    coeff_array.append(coeff_line)

    # Q30
    name_over  = fileName( mylambda , q20 , q22 , q30 + q30_spacing )
    name_under = fileName( mylambda , q20 , q22 , q30 - q30_spacing )

    file1, file2, coeff1, coeff2, coeff3 = chooseCoeffs(myfile, name_over, name_under, q30_spacing)

    file_array.append(file1)
    file_array.append(file2)

    coeff_line = [coeff1, coeff2, coeff3]
    coeff_array.append(coeff_line)

    # Lambda
    name_over  = fileName( mylambda + lambda_spacing , q20 , q22 , q30 )
    name_under = fileName( mylambda - lambda_spacing , q20 , q22 , q30 )

    file1, file2, coeff1, coeff2, coeff3 = chooseCoeffs(myfile, name_over, name_under, lambda_spacing)

    file_array.append(file1)
    file_array.append(file2)

    coeff_line = [coeff1, coeff2, coeff3]
    coeff_array.append(coeff_line)

    # Write to file
    fichier = 'qpmas-lambda' + str(mylambda) + '_' + str(q20).zfill(3) + str(q22).zfill(3) + str(q30).zfill(3) + '.d'
    inertia_file = open(fichier,'w')
    for i in range(0,len(coeff_array)):
        coeff1 = '{:010.5f}'.format(coeff_array[i][0])
        coeff2 = '{:010.5f}'.format(coeff_array[i][1])
        coeff3 = '{:010.5f}'.format(coeff_array[i][2])
        newLine = str(coeff1).zfill(10) + '  ' + str(coeff2).zfill(10) + '  ' + str(coeff3).zfill(10)
        inertia_file.write( "".join(word.center(1) for word in newLine) )
        inertia_file.write('\n')
    for newLine in file_array:
        inertia_file.write(newLine)
#       inertia_file.write('\n')
    newLine = str(temperature).zfill(10)
    inertia_file.write(newLine)
    inertia_file.write('\n')
    inertia_file.close()

    index += 1

