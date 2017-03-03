import numpy as np                                                                
import os, subprocess, re, shutil
import xml.etree.ElementTree as ET
import errno


parent_directory = os.getcwd()


#-------------------------------------------------#
#    In the preliminary matter, set the parameter #
#    defining the precision of your numerical     #
#    derivative; for instance:                    #
#        dx = d_q20, dy = d_q30, dz = d_q22       #
#    Also list the name of the XML file           #
#-------------------------------------------------#

executable = 'hf268f'
infile = '294Og-all_PES.xml'
batch_script = 'RUN_SCRIPT.pbs'

num_constraints = 2 # Number of constraints in the PES
num_points = 2*num_constraints # Number of neighboring points used in the derivative

dx = 0.001 # This is the amount your multipole constraints will change as you calculate nearby points to numerically compute the derivative of the density with respect to your multipole moments


#-------------------------------------------------#
#    Read in the XML file                         #
#-------------------------------------------------#

tree = ET.parse( infile )
root = tree.getroot()
points = root.findall("./PES/point")  # The xml tree 'points' contains addresses for each individual grid point in the PES

for point in points:

#-------------------------------------------------#
#    From the XML file, extract (for a given      #
#    point) the filename, basis parameters,       #
#    and multipole constraints                    #
#-------------------------------------------------#

    for line in point.iter('file'):
        old_index = line.get('name')    # "nom" typically has the form "hfodd_000002.out"
    old_index = old_index.split('_')[1]
    old_index = old_index.split('.')[0]

    for line in point.iter('HOfrequencies'):
        omega_x = line.get('omega_x')
        omega_x = float(omega_x)
        omega_y = line.get('omega_y')
        omega_y = float(omega_y)
        omega_z = line.get('omega_z')
        omega_z = float(omega_z)

    for line in point.iter('deformation'):
        beta2 = line.get('beta2')
        beta2 = float(beta2)
        omega0 = line.get('omega0')
        omega0 = float(omega0)
        FCHOM0 = line.get('FCHOM0')
        FCHOM0 = float(FCHOM0)

    qtypes = ['q10']
    values = [0.0]

    for line in point.iter('constraint'):
        qtype = line.get('type')
        qtypes.append(qtype)
        value = line.get('val')
        value = re.search('\D\d*\.\d*',value).group(0)
        values.append(value)

#-------------------------------------------------#
#    Make a directory based on the filename or    #
#    the constraints or something, and populate   #
#    it with the requisite subdirectories and     #
#    input files (which we can modify later as    #
#    needed) and a restart file                   #
#-------------------------------------------------#

        if qtype == 'q20':
            q20 = int(round(float(value),0))
        elif qtype == 'q30':
            q30 = int(round(float(value),0))
        else:
            print 'Error!!'

    index = str(q20).zfill(3) + str(q30).zfill(3)

    old_REC = 'rec/HFODD_' + old_index.zfill(8) + '.REC'

    subdirectory = parent_directory + "/HFODD_%s/" %index
    subdir_restart = subdirectory + "/restart/"

    try: 
        os.makedirs(subdir_restart)
    except OSError:
        if not os.path.isdir(subdir_restart):
            raise
#    except OSError as exc:
#        raise exc

# I'm running into too many errors doing things the 'proper' way, so I told it to use the system copy instead of the python copy
#    shutil.copy2('hfodd.d', subdirectory + 'hfodd.d')
#    shutil.copy2('hfodd_mpiio.d', subdirectory + 'hfodd_mpiio.d')
#    shutil.copy2(batch_script, subdirectory + batch_script)
    os.system(" cp hfodd.d hfodd_mpiio.d %s %s %s " %(batch_script, executable, subdirectory) ) ### DO I NEED ANY OTHER FILES?
    shutil.copy2(old_REC, subdir_restart + '/HFODD_00000001.REC')

    os.chdir(subdirectory)

#-------------------------------------------------#
#    Create the file hfodd_path.d, which          #
#    describes your centerpoint                   #
#-------------------------------------------------#

    newLine = ['1 0    0.0  ']

    for i in range( 1, len(qtypes) ):
        lam = qtypes[i][1]
        mu = qtypes[i][2]
        addition='%1s %1s %8s  ' %(lam, mu, values[i] )
        newLine.append(addition)

    data_file = open('hfodd_path.d','w')
    data_file.write("%d %d \n" %(num_constraints+1, 1) ) # This doesn't seem to work if Q_10 is a constraint in your original file
    data_file.write( "".join(word.center(1) for word in newLine) )
    data_file.write('\n')
    data_file.close()

#-------------------------------------------------#
#    Create the file hfodd_path_new.d, which      #
#    describes the neighbors to your centerpoint  #
#-------------------------------------------------#

# When writing the file hfodd_path_new.d, one has to relate somehow the line number to the constraint being modified for that point, and whether you are adding or subtracting ( x -> x +/- dx ). The convention here is that all lines which are even have dx added (and odd lines, subtracted). Furthermore, you'll use the line number to decide which particular constraint gets modified (since there are two neighboring points, hence two path_file lines per constraint, the first two lines will refer to constraint 1, the next two to constraint 2, etc.


    data_file = open('hfodd_path_new.d','w')
    data_file.write("%d %d \n" %(num_constraints+1, num_points) )

    for line in range( 1, num_points+1 ):
        newLine = ['1 0    0.0  ']

        for i in range( 1, len(qtypes) ):
            lam = qtypes[i][1]
            mu = qtypes[i][2]

            if( (line-1)/2 == (i-1) ):

                if( line % 2 == 0):
                    addition='%1s %1s %8s  ' %(lam, mu, str(float(values[i])+dx) )
                else:
                    addition='%1s %1s %8s  ' %(lam, mu, str(float(values[i])-dx) )
            else:
                addition='%1s %1s %8s  ' %(lam, mu, values[i] )

            newLine.append(addition)

        data_file.write( "".join(word.center(1) for word in newLine) )
        data_file.write('\n')

    data_file.close()

#-------------------------------------------------#
#    Also create the file toto.txt which will     #
#    be used as an input for the inertia code,    #
#    as described in the comments to that code    #
#-------------------------------------------------#

# Actually, that'll be pretty similar between runs, I think. You might have to rename some QP files after the neighbors finish computing and put them together in a folder somewhere, but that shouldn't be too difficult. You can probably automate that in the batch script template



#-------------------------------------------------#
#    Read and modify the file hfodd.d, to set the #
#    basis constant and to set the restart flags  #
#-------------------------------------------------#

    fichier = 'hfodd.d'

	# Read the file and store all lines in a list
    fread = open( fichier, 'r' )
    allLines = fread.readlines()
    fread.close()

    # Find and replace the fields which define the basis (IBASIS, etc.)

    chaine = 'BASISAUTOM   IBASIS\n'
    position = [k for k, x in enumerate(allLines) if x == chaine]
    allLines[position[0]+1] = '               0\n'

    chaine = 'SURFAC_DEF   LAMBDA   MIU    ALPHAR\n'
    position = [k for k, x in enumerate(allLines) if x == chaine]
    allLines[position[0]+1] = '              -2       0      '+ str(beta2) +'\n'
    allLines[position[0]+2] = '               4       0      0.00\n'

    chaine = 'HOMEGAZERO   FCHOM0\n'
    position = [k for k, x in enumerate(allLines) if x == chaine]
    allLines[position[0]+1] = '              '+ str(FCHOM0) +'\n'

    chaine = 'FREQBASIS    HBARIX  HBARIY  HBARIZ  INPOME\n'
    position = [k for k, x in enumerate(allLines) if x == chaine]
    allLines[position[0]+1] = '              ' + str(omega_x) + '     ' \
                                               + str(omega_y) + '     ' \
                                               + str(omega_z) + '      1\n'


    # Find and replace the fields which restart the calculation (IF_THO, ICONTI, etc)

    chaine = 'HFBTHOISON   IF_THO  CBETHO\n'
    position = [k for k, x in enumerate(allLines) if x == chaine]
    allLines[position[0]+1] = '               0      0.0\n'

    chaine = 'RESTART      ICONTI\n'
    position = [k for k, x in enumerate(allLines) if x == chaine]
    allLines[position[0]+1] = '               1\n'

    chaine = "CONT_PAIRI   IPCONT\n"
    position = [k for k, x in enumerate(allLines) if x == chaine]
    allLines[position[0]+1] = '               1\n'

# I was trying to do the matching using regular expressions, in case a space sneaks its way onto the end of the keyword line or something, but it was giving me a lot of trouble so I set it aside for now.
#    chaine = r'CONT_PAIRI.*\n'
#    line = [string for string in allLines if re.match(string, chaine)]
#    print line
#    position = [k for k, x in enumerate(allLines) if re.match(x, chaine)]
#    print k
#    allLines[position[0]+1] = '               1\n'

    # Write the lines to file
    fwrite = open( fichier, 'w' )
    for lines in allLines:
        fwrite.write(lines)
    fwrite.close()

#-------------------------------------------------#
#    Read and modify the batch script file, to    #
#    first compute the neighboring points and     #
#    then to run the inertia code at this point   #
#-------------------------------------------------#

    fread = open( batch_script, 'r' )
    allLines = fread.readlines()
    fread.close()

    # Find and replace the fields which define the run
    fwrite = open (batch_script, 'w')
    for line in allLines:
        line = re.sub(r'#MSUB -l nodes=[0-9]*', '#MSUB -l nodes=1', line)
        line = re.sub(r'#MSUB -N .*', '#MSUB -N ' + index, line)
        line = re.sub(r'#MSUB -l walltime=.*', '#MSUB -l walltime=10:00:00', line)
        line = re.sub(r'srun -n [0-9]*', 'srun -n ' + str(num_points), line)
        line = re.sub(r'SCRATCH_DIR=.*', 'SCRATCH_DIR=\'' + subdirectory + '\'', line)
        fwrite.write(line)

    fwrite.close()

# Do I want to add something about running the inertia script automatically? That might be a good thing once I know roughly how long it takes

    os.chdir(parent_directory)
