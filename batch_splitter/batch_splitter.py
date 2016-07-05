import numpy as np
import os, subprocess

current_directory = os.getcwd()

tasks_per_batch = 81 # Multiples of three help, assuming 3 tasks/node (=> 27 nodes)
### NOTE: THIS IS ALREADY ASSUMED IN THE TEMPLATE FILE!!! I HAVEN'T GENERALIZED IT YET
### (probably the best way to generalize would be to use a regex instead of a specific number)
nodes_per_batch = tasks_per_batch/3

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
#     Import your data somehow, to make it        #
#                    usable                       #
#-------------------------------------------------#

numNewPts = int( breakLine( newPathLines[0] )[1] ) 
numOldPts = int( breakLine( oldPathLines[0] )[1] ) 

newConstNames = np.zeros((numNewPts, numConstraints))
oldConstNames = np.zeros((numOldPts, numConstraints))

newConstVals = np.zeros_like(newConstNames)
oldConstVals = np.zeros_like(oldConstNames)

for i in range(0,numNewPts):
    newConstNames(i,:) = listConstraints
    for j in range(0,numConstraints):
        newConstVals(i,j) = int( breakLine( newPathLines[i+1] )[3*j+2] )

for i in range(0,numOldPts):
    oldConstNames(i,:) = listConstraints
    for j in range(0,numConstraints):
        oldConstVals(i,j) = int( breakLine( oldPathLines[i+1] )[3*j+2] )


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

            const_restart = newConstNames(i,k)
            const_old = oldConstNames(j,k)

            q_restart = newConstVals(i,k)
            q_old = oldConstVals(j,k)

            if const_old==const_restart:
                distance = distance + (q_old - q_restart)**2

        if distance <= min_dist:
            min_dist = distance
            index_optimal = j

    optimal_indices(i) = index_optimal

#    cp restart_old/HFODD_000optimal_indices(i).REC restart/HFODD_0000000i.REC # ...however you choose to implement this...

# Don't forget to add 1 to your indices, since Python indices start from 0 but HFODD indexes starting at 1!
    oldRec = 'HFODD_' + str(index_optimal+1).zfill(8) + '.REC'
    newRec = 'HFODD_' + str(i+1).zfill(8) + '.REC'

    print oldRec, 'is being moved to', newRec
    os.system('cp restart_old/%s restart/%s' %(oldRec, newRec))


#-------------------------------------------------#
#    Next we need to break the big job into       #
#             several smaller jobs                #
#-------------------------------------------------#


numBatches = int(numNewPts/tasks_per_batch)
if numBatches != numNewPts/tasks_per_batch:
    numExtras = numNewPts - (tasks_per_batch * numBatches)
    numBatches = numBatches+1

for i in range(0,numBatches):
    os.mkdir("RUN_%s" %i) ### OR WHATEVER IT IS
    ### STOCK IT WITH A RESTART FOLDER, A REC FOLDER, etc.
    ### YOU'LL NEED A TEMPLATE .PBS FILE, AS WELL AS HFODD.D and HFODD_MPIIO.D FILES
    ### AND MAYBE EVEN MORE THAN THAT
    for j in range(0,tasks_per_batch):
        old_index = (tasks_per_batch * i) + j + 1
        new_index = j+1
        os.system(" cp restart/HFODD_000old_index.REC RUN_%s/HFODD_000new_index.REC " %i) ### THIS NEEDS TO BE CLEANED UP

    # Create batch submission scripts for each folder
    fichier = 'batch_script_template.txt'
    fread = open( fichier )
    lines_template = fread.readlines()
    fread.close()

    chaine = '#MSUB -N \n'
    position = [i for i, x in enumerate(lines_template) if x == chaine]
    lines_template[position[0]] = '#MSUB -N ' + current_directory + '-RUN_' + i + '\n'

    chaine = 'SCRATCH_DIR=\n'
    position = [i for i, x in enumerate(lines_template) if x == chaine]
    lines_template[position[0]] = 'SCRATCH_DIR=\'' + current_directory + '/RUN_' + i + '\'\n'

    if numExtras != 0:

        if numExtras/3 == int(numExtras/3):
            numNodes = numExtras/3              # 4 cores/task; 12 cores/node => 3 tasks/node
        else:
            numNodes = numExtras/3 + 1          # Reserve an extra node, even if you just need part of it

        chaine = '#MSUB -l nodes=9\n'
        position = [i for i, x in enumerate(lines_template) if x == chaine]
        lines_template[position[0]] = '#MSUB -l nodes=' + numNodes + '\n'

        chaine = '#MSUB -l ttc=108\n'
        position = [i for i, x in enumerate(lines_template) if x == chaine]
        lines_template[position[0]] = '#MSUB -l ttc=' + 4*numExtras + '\n'

        chaine = 'srun -n %s --ntasks-per-node=3 -c $OMP_NUM_THREADS $EXECUTABLE < /dev/null >& $OUTPUT\n' % nodes_per_batch
        position = [i for i, x in enumerate(lines_template) if x == chaine]
        lines_template[position[0]] = 'srun -n' + numExtras + ' --ntasks-per-node=3 -c $OMP_NUM_THREADS $EXECUTABLE < /dev/null >& $OUTPUT\n'

    # writing batch job script to file
    fichier = 'RUN_%s.pbs' %i
    fwrite = open( fichier, 'w' )
    for lines in header_full:
        fwrite.write(lines)
    for lines in lines_template:
        fwrite.write(lines)
    fwrite.close()

    os.system(" mv RUN_%s.pbs RUN_%s/ " %(i,i) )
#    os.system(" msub RUN_%s/RUN_%s.pbs " %(i,i) )


#-------------------------------------------------#
#    You might look into stitching it back        #
#             together here as well               #
#-------------------------------------------------#

### STITCHING IT BACK TOGETHER - move this to the batch script template!!!

# Check to see if any more jobs are still running
more_jobs = subprocess.check_output( 'showq -u $USER | grep $USER | wc -l', shell=True)
more_jobs = int(more_jobs)

if more_jobs == 0:
###    Notify me?
###    Stitch them back together automatically?
###        Has time ever been an issue down to those last few minutes?
###        How long will this script take to run?
###    Launch another job to stitch them together automatically?
