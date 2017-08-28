import numpy as np                                                                
import os, subprocess, re, shutil
import xml.etree.ElementTree as ET
import errno, math
from mpi4py import MPI

# Specify the source directory, which is where your outputs, record files, and qp files are stored

qp_archive = '/usr/workspace/wsb/matheson/rprocess/294Og/qp-archive'
rec_archive = '/usr/workspace/wsb/matheson/rprocess/294Og/rec-archive'
out_archive = '/usr/workspace/wsb/matheson/rprocess/294Og/out-archive'

# Specify the scratch directory, the XML file, the HFODD executable, the inertia executable (all of which should be in the scratch directory, along with the HFODD input files hfodd.d and hfodd_mpiio.d)

scratch_dir = '/p/lscratchh/matheson/rprocess/294Og/inertia_tensor/sample_scratch_dir'
xml_file = '294Og_PES.xml'
hfodd_exe = './hf268f'
inertia_exe = './qpmas4.1'

#-------------------------------------------------#
#    In the preliminary matter, set the parameter #
#    defining the precision of your numerical     #
#    derivative; for instance:                    #
#        dx = d_q20, dy = d_q30, dz = d_q22       #
#-------------------------------------------------#

num_constraints = 2 # Number of constraints in the PES
nNeighbors = 2*num_constraints # Number of neighboring points used in the derivative

dx = 0.001 # This is the amount your multipole constraints will change as you calculate nearby points to numerically compute the derivative of the density with respect to your multipole moments


world_comm = MPI.COMM_WORLD
world_rank = world_comm.rank
world_size = world_comm.size

# Read the XML file. Extract Q20 values and round to the nearest integer

tree = ET.parse( xml_file )
root = tree.getroot()
points = root.findall("./PES/point")
total_points = = len(points)

global_prop = root.findall("./PES/Global")
for prop in global_prop:
    for line in prop.iter('nucleus'):
        protons = float(line.get('Z'))
        neutrons = float(line.get('N'))
        a_mass = neutrons + protons

q20values = []
file_count = []

for point in points:
    for line in point.iter('constraint'):
        qtype = line.get('type')
        if qtype == 'q20':
            value = line.get('val')
            value = re.search('\D\d*\.\d*',value).group(0)
            q20 = int(round(float(value),0))
            if q20 not in q20values:
                q20values.append(q20)

# Create a subdirectory in your scratch directory for each value of Q20
## This would be a good place to do an MPI_Comm_Spawn or whatever you decide to do. Pretty much everything after this point can be done independently in the different q20 folders. You'd spawn a number of tribes and then assign them to a q20 value by like "for i in range(0, len(q20values): if tribe_num == i: q20 = q20values[i]; subdirectory = ..."
## The tribes really don't need to talk to each other. One very real danger, though, is that some tribes would have very little work to do and some would have a lot, just depending how many points there are for each value of q20. It would be great to implement some kind of load balancing

for q20 in q20values:
    subdirectory = scratch_dir + "/q20-%s/" %str(q20)
    subdir_restart = subdirectory + "/restart/"

    try: 
        os.makedirs(subdir_restart)
    except OSError:
        if not os.path.isdir(subdir_restart):
            raise

## Copy the XML file, both executables, and both input files into each subdirectory

    os.system(" cp hfodd.d hfodd_mpiio.d %s %s %s %s " %(xml_file, hfodd_exe, inertia_exe, subdirectory) )

## Within each subdirectory, modify the input file hfodd.d with the appropriate basis (and make sure the proper restart settings are enabled)

    if abs(q20)>30:
        omega0 = 0.1 * float(abs(q20)) * math.exp( -0.02 * float(abs(q20)) ) + 6.5
    else:
        omega0 = 8.1464
    beta2 = 0.05 * math.sqrt( float( abs(q20) ) )
    FCHOM0 = omega0 / ( 41. / a_mass**(1./3.) )

    fichier = subdirectory + 'hfodd.d'

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
    allLines[position[0]+1] = '               2       0      '+ str(beta2) +'\n'

    chaine = 'HOMEGAZERO   FCHOM0\n'
    position = [k for k, x in enumerate(allLines) if x == chaine]
    allLines[position[0]+1] = '              '+ str(FCHOM0) +'\n'

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

    chaine = "CONTAUGMEN   IACONT\n"
    position = [k for k, x in enumerate(allLines) if x == chaine]
    allLines[position[0]+1] = '               1\n'

    # Write the lines to file
    fwrite = open( fichier, 'w' )
    for lines in allLines:
        fwrite.write(lines)
    fwrite.close()

##! Copy the needed record/restart files into their respective subdirectories

    # This is actually going to be tricky, because you'll have to find the names in the XML file, and you'll have to change the names once you've moved them into this folder. You can combine this step with the following step for some things; that is, you'll be filtering the XML file down to a limited number of points and extracting and manipulating properties that way

    file_counter = 0

    for point in points:
        for line in point.iter('constraint'):
            qtype = line.get('type')
            value = line.get('val')
            value = re.search('\D\d*\.\d*',value).group(0)
            if qtype == 'q20':
                q20test = int(round(float(value),0))
                if q20test == q20:
                    file_counter += 1
    file_count.append(file_counter)

    data_file = open(subdirectory + 'hfodd_path.d','w')
    data_file2 = open(subdirectory + 'hfodd_path_new.d','w')
    data_file.write("%d %d \n" %(num_constraints+1, file_counter) )
    data_file2.write("%d %d \n" %(num_constraints+1, file_counter*nNeighbors) )

    file_counter = 0

    for point in points:
        qtypes = ['q10']
        values = [0.0]
        for line in point.iter('constraint'):
            qtype = line.get('type')
            qtypes.append(qtype)
            value = line.get('val')
            value = re.search('\D\d*\.\d*',value).group(0)
            values.append(value)
            if qtype == 'q20':
                q20test = int(round(float(value),0))
                if q20test == q20:
                    file_counter += 1
                    for line2 in point.iter('file'):
                        oldindex = line2.get('name')     # "name" typically has the form "hfodd_000002.out"
                    oldindex = oldindex.split('_')[1]
                    oldindex = oldindex.split('.')[0]
                    old_rec = 'HFODD_' + oldindex.zfill(8) + '.REC'
                    new_rec = 'HFODD_' + str(file_counter).zfill(8) + '.REC'
#                    shutil.copy2(rec_archive + old_rec, subdir_restart + new_rec)
                    print(rec_archive + old_rec, 'moved to', subdir_restart + new_rec)

## Within each subdirectory, parse the XML file and build a list hfodd_path.d of which files belong to that subdirectory
## At the same time, build a list hfodd_path_new.d of the satellite points you'll need to calculate to compute the inertia

                    newLine = ['1 0    0.0  ']
                    newLine2 = ['1 0    0.0  ']

                    for i in range( 1, len(qtypes) ):
                        lam = qtypes[i][1]
                        mu = qtypes[i][2]
                        addition='%1s %1s %8s  ' %(lam, mu, values[i] )
                        newLine.append(addition)

                        for line in range( 1, nNeighbors+1 ):
                            if( (line-1)/2 == (i-1) ):

                                if( line % 2 == 0):
                                    addition='%1s %1s %8s  ' %(lam, mu, str(float(values[i])+dx) )
                                else:
                                    addition='%1s %1s %8s  ' %(lam, mu, str(float(values[i])-dx) )
                            else:
                                addition='%1s %1s %8s  ' %(lam, mu, values[i] )

                            newLine2.append(addition)

                        data_file2.write( "".join(word.center(1) for word in newLine) )
                        data_file2.write('\n')


                    data_file.write( "".join(word.center(1) for word in newLine) )
                    data_file.write('\n')

    data_file.close()
    data_file2.close()


#! You can now submit these subdirectory jobs to the queue. Depending how you have things set up, you might just need to run them using separate SRUN commands

for i in range( 0, len(q20values) ):
    # Submit a job to the queue which has nNeighbors*file_count[i] tasks, i.e.
    # os.system( 'srun -N1 -n%d -o %s/%s.txt %s &' %(nNeighbors*file_count[i], subdirectory, executable, executable) )
    pass


##! After each subdirectory HFODD run completes (and hopefully as part of that SRUN command? - maybe the key is to move the SRUN command to the very beginning once the directories are defined, and explain what it is to do via another "inner" Python script?), you'll want to collect your qp outputs and name them according to the same naming scheme as the original files (this could be tricky, but you have the XML file and the hfodd_path_new.d file in there still so there is at least some kind of reference)

## In each subdirectory, create the inertia input list in the same directory as the collected qp outputs

##! In each subdirectory, run the inertia code for the points in that subdirectory (you should have several MPI ranks allocated already)

    # It's probably best to do it this way, actually, because it seems that if you use too many at once, I'm guessing you run into memory issues. 10 points at once per node seems to be achievable; 30 is way too many. I'm not sure where that transition takes place.

## Give the inertia output file a unique, subdirectory-dependent name and copy it to a common folder in the parent directory. Maybe even have it append to a common file in that parent directory, as well (although I'm not sure about that just yet, depending on how we end up identifying specific lines in the inertia output file whether by rank or ideally by characteristics)




## *## Comments with two ## signs are steps that can be done in parallel
#! *#! Comments marked by #! will take some thinking to be able to do. Everything else more or less exists up to this point.
