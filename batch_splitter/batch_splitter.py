import numpy as np
import os, subprocess, re

parent_directory = os.getcwd()

executable = 'hf268f'

tasks_per_batch = 81 # Multiples of three help, assuming 3 tasks/node (=> 27 nodes)
### NOTE: THIS IS ALREADY ASSUMED IN THE TEMPLATE FILE!!! I HAVEN'T GENERALIZED IT YET
### (probably the best way to generalize would be to use a regex instead of a specific number)
nodes_per_batch = tasks_per_batch/3

# It is assumed that you've already run restart_v3.py, which moved all your good .REC files into restart/ and indexed them into a file hfodd_path.d. This script starts by moving restart/ to a new folder restart_old/, then creating a new restart/ folder which it populates using the good .REC files from the restart_old/ folder to fill in the holes in the PES (which is represented by hfodd_path_new.d).

os.system(" mv restart/ restart_old/ ")
os.system(" mkdir restart/ ")

#-------------------------------------------------#
#           Read in HFODD path files              #
#-------------------------------------------------#

# Read the file and store all lines in a list
fread = open('hfodd_path_new.d','r')
newPathLines = fread.readlines()
fread.close()

fread = open('hfodd_path.d','r')
oldPathLines = fread.readlines()
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

def breakLine2(element):
    currentLine  = re.split("\n",element)
    brokenLine   = re.split("/",currentLine[0])
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


#-------------------------------------------------#
#         Make your path data usable by           #
#            storing it in arrays                 #
#-------------------------------------------------#

numNewPts = int( breakLine( newPathLines[0] )[1] ) 
numOldPts = int( breakLine( oldPathLines[0] )[1] ) 

newConstNames = listConstraints
oldConstNames = listConstraints

newConstVals = np.zeros((numNewPts, numConstraints))
oldConstVals = np.zeros((numOldPts, numConstraints))

for i in range(0,numNewPts):

    if i > 0: # Since we already established the first row by assigning newConstNames = listConstraints
        newConstNames = np.vstack([newConstNames, listConstraints])

    for j in range(0,numConstraints):
        newConstVals[i,j] = float( breakLine( newPathLines[i+1] )[3*j+2] )

for i in range(0,numOldPts):

    if i > 0:
        oldConstNames = np.vstack([oldConstNames, listConstraints])

    for j in range(0,numConstraints):
        oldConstVals[i,j] = float( breakLine( oldPathLines[i+1] )[3*j+2] )


#-------------------------------------------------#
#    This snippet of code plugs in the holes in   #
#        your PES, in the same way as             #
#           hfodd_mpimanager_4.f90                #
#        using option mpidef=4                    #
#-------------------------------------------------#

optimal_indices = np.ones(numNewPts)

for i in range(0, numNewPts):
    index_optimal = 1; min_dist=10**9 # if nothing else does any better, you just plug the first point in everywhere by default

    for j in range(0, numOldPts):
        distance = 0

        for k in range(0, numConstraints):

            const_restart = newConstNames[i,k]
            const_old = oldConstNames[j,k]

            q_restart = newConstVals[i,k]
            q_old = oldConstVals[j,k]

            if const_old==const_restart:
                distance = distance + (q_old - q_restart)**2

        if distance <= min_dist:
            min_dist = distance
            index_optimal = j

    optimal_indices[i] = index_optimal

# Don't forget to add 1 to your indices, since Python indices start from 0 but HFODD indices start at 1!
    oldRec = 'HFODD_' + str(index_optimal+1).zfill(8) + '.REC'
    newRec = 'HFODD_' + str(i+1).zfill(8) + '.REC'

#    print oldRec, 'is being moved to', newRec
    os.system('cp restart_old/%s restart/%s' %(oldRec, newRec))


#-------------------------------------------------#
#    Next we need to break the big job into       #
#          several smaller job batches            #
#-------------------------------------------------#

numTasks = numNewPts
numExtras = 0

numBatches = int(float(numTasks)/float(tasks_per_batch))

if numBatches != float(numTasks)/float(tasks_per_batch):
    numExtras = numTasks - (tasks_per_batch * numBatches)   # Leftover tasks that don't fit in evenly.
    numBatches = numBatches+1                               # Let's give them their own batch here

#-------------------------------------------------#
#    Create batch subfolders and fill them        #
#       with everything they need to run          #
#-------------------------------------------------#

for i in range(0,numBatches):

    batch_subfolder = parent_directory + "/RUN_%s" %i

    try: 
        os.makedirs(batch_subfolder)
    except OSError:
        if not os.path.isdir(batch_subfolder):
            raise

    os.system(" cp hfodd.d hfodd_mpiio.d %s %s " %(executable, batch_subfolder) ) ### DO I NEED ANY OTHER FILES?

    try: 
        os.makedirs(batch_subfolder + "/restart")
        os.makedirs(batch_subfolder + "/rec")
        os.makedirs(batch_subfolder + "/summary")
        os.makedirs(batch_subfolder + "/lic")
        os.makedirs(batch_subfolder + "/qp")
        os.makedirs(batch_subfolder + "/out")
    except OSError:
        if not ( os.path.isdir(batch_subfolder + "/restart") and os.path.isdir(batch_subfolder + "/rec") and os.path.isdir(batch_subfolder + "/summary") and os.path.isdir(batch_subfolder + "/lic") and os.path.isdir(batch_subfolder + "/qp") and os.path.isdir(batch_subfolder + "/out") ):
            raise


#-------------------------------------------------#
#  Give each subfolder its own set of .REC files  #
#-------------------------------------------------#

    if (numExtras != 0) and (i == numBatches-1):

        for j in range(0,numExtras):

            old_index = (tasks_per_batch * i) + j + 1
            new_index = j+1

            oldRec = 'HFODD_' + str(old_index).zfill(8) + '.REC'
            newRec = 'HFODD_' + str(new_index).zfill(8) + '.REC'

            os.system(" cp %s/restart/%s %s/restart/%s " %(parent_directory, oldRec, batch_subfolder, newRec))

    else:

        for j in range(0,tasks_per_batch):

            old_index = (tasks_per_batch * i) + j + 1
            new_index = j+1

            oldRec = 'HFODD_' + str(old_index).zfill(8) + '.REC'
            newRec = 'HFODD_' + str(new_index).zfill(8) + '.REC'

            os.system(" cp %s/restart/%s %s/restart/%s " %(parent_directory, oldRec, batch_subfolder, newRec))


#-------------------------------------------------#
#       Those .REC files will need custom         #
#         hfodd_path.d & hfodd_path_new.d         #
#       files to keep track of what's what        #
#-------------------------------------------------#

# Instead of rewriting/regenerating hfodd_mpiio.d for each subfolder (which might
# not correspond to a rectangular grid), we just copy hfodd_path_new.d to
# hfodd_path.d within the batch_subfolder and keep mpidef=4, PRETENDING like we
# happen to have exactly the same .REC files we'll be calculating.

    pathfile = "RUN_%d-path.d" %i
    data_file = open(pathfile,'w')

    if (numExtras != 0) and (i == numBatches-1):
        data_file.write("%d %d \n" %(numConstraints, numExtras) )
        for j in range(0,numExtras):
            line = newPathLines[(tasks_per_batch * i) + j + 1]
            data_file.write( "%s" %line )

    else:
        data_file.write("%d %d \n" %(numConstraints, tasks_per_batch) )
        for j in range(0,tasks_per_batch):
            line = newPathLines[(tasks_per_batch * i) + j + 1]
            data_file.write( "%s" %line )

    data_file.close()

    os.system(" mv %s %s/hfodd_path_new.d " %(pathfile, batch_subfolder))
    os.system(" cp %s/hfodd_path_new.d %s/hfodd_path.d " %(batch_subfolder, batch_subfolder))


#-------------------------------------------------#
#         Create batch submission scripts         #
#            for each batch_subfolder             #
#-------------------------------------------------#

    short_folder_name = breakLine2(parent_directory)[-1]

    batch_file = 'batch_script_template.txt'
    fread = open( batch_file )
    lines_template = fread.readlines()
    fread.close()

    chaine = '#MSUB -N \n'
    position = [k for k, x in enumerate(lines_template) if x == chaine]
    lines_template[position[0]] = '#MSUB -N ' + short_folder_name + '-RUN_' + str(i) + '\n'

    chaine = 'SCRATCH_DIR=\n'
    position = [k for k, x in enumerate(lines_template) if x == chaine]
    lines_template[position[0]] = 'SCRATCH_DIR=\'' + parent_directory + '/RUN_' + str(i) + '\'\n'

    if (numExtras != 0) and (i == numBatches-1):

        if numExtras/3 == float(numExtras)/3.0:
            numNodes = numExtras/3              # 4 cores/task; 12 cores/node => 3 tasks/node
        else:
            numNodes = numExtras/3 + 1          # Reserve an extra node, even if you just need part of it

        chaine = '#MSUB -l nodes=9\n'
        position = [k for k, x in enumerate(lines_template) if x == chaine]
        lines_template[position[0]] = '#MSUB -l nodes=' + str(numNodes) + '\n'

        chaine = '#MSUB -l ttc=108\n'
        position = [k for k, x in enumerate(lines_template) if x == chaine]
        lines_template[position[0]] = '#MSUB -l ttc=' + str(4*numExtras) + '\n'

        chaine = 'srun -n %s --ntasks-per-node=3 -c $OMP_NUM_THREADS $EXECUTABLE < /dev/null >& $OUTPUT\n' % nodes_per_batch
        position = [k for k, x in enumerate(lines_template) if x == chaine]
        lines_template[position[0]] = 'srun -n' + str(numExtras) + ' --ntasks-per-node=3 -c $OMP_NUM_THREADS $EXECUTABLE < /dev/null >& $OUTPUT\n'

    # writing batch job script to file
    batch_file = 'RUN_%d.pbs' %i
    fwrite = open( batch_file, 'w' )
    for lines in lines_template:
        fwrite.write(lines)
    fwrite.close()

    os.system(" mv %s %s " %(batch_file,batch_subfolder) )
#    os.system(" msub %s/%s " %(batch_subfolder, batch_file) )


#-------------------------------------------------#
#    You might look into stitching it back        #
#             together here as well               #
#-------------------------------------------------#

### STITCHING IT BACK TOGETHER - move this to the batch script template!!!

# Check to see if any more jobs are still running
#more_jobs = subprocess.check_output( 'showq -u $USER | grep $USER | wc -l', shell=True)
#more_jobs = int(more_jobs)
#
#if more_jobs == 0:
#    print 'more_jobs = ', more_jobs
###    Notify me?
###    Stitch them back together automatically?
###        Has time ever been an issue down to those last few minutes?
###        How long will this script take to run?
###    Launch another job to stitch them together automatically?
###      Don't forget, you'll need the .REC files, the .out files, AND the .QP, .LIC, etc. files
