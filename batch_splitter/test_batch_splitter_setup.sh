mkdir restart/

for index in [0-150]; do
    touch restart/HFODD_000000$index.REC
    sed add line to each file that says its name

Make a small set of initial .REC files, and a corresponding hfodd_path.d file

Then make a larger hfodd_path_new.d file using hfodd_generateGrid.py or whatever.

You'll need to put the hfodd.d, hfodd_mpiio.d, pbs_example.txt, executable files in the main folder.
