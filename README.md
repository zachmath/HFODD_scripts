These files constitute a suite of shell and Python scripts designed to facilitate large HFODD potential energy surface projects.

# Main Folder

 - **formPESarray.sh** creates a multidimensional array of gridpoints, representing multipolarity constraints on a nucleus. HFODD can then be used to calculate properties of the nucleus subject to each grid point in this array. *OBSOLETE - replaced by the combined functionality of mpidef=4 and batch_splitter.py*

 - **parseHFODDoutput.py** is a modified version of Nicolas's Python script of the same name. No substantial differences; just some tweaks to get it to run for me.

 - **parseXMLarray.py** uses the XML database created by Nicolas Schunck's script `parseHFODDoutput.py` to create a `.dat` file readable by `PES_plotting_script.py` (that is, it contains the multipole moment constraints and the HFB energies).

 - **PES_plotting_script.py** creates nice-looking potential energy surfaces using the output from either `restart_v2.sh` or `parseXMLarray.py`. It has several features implemented depending what data you'd like to include on your plot, which it will ask you for at runtime.

 - **restart_v2.sh** is used after HFODD has completed its run, to collect results in a readable form ready for plotting potential energy surfaces, as well as to prepare the array for future runs. [You might give the option of consolidating outputs without moving around rec files, since that can be time consuming and you might not even care about running it again. Also, you should find out if people even want these features. You might use them occasionally, but given how time-consuming it is to even create a 2D PES, it might not be worth it to create this massive labyrinth of constraints (although again, a map would certainly help)]. *OBSOLETE - replaced by the combined functionality of `mpidef=4` and `batch_splitter.py`*

 - **restart_v3.py** Similar to `restart_v3.sh`, this version prepares the project for another run with a tighter convergence parameter. It will analyze the XML file created in `parseHFODDoutput.py` and copy the "good" .REC files to the restart folder. As it does so, it will reindex those good .REC files and generate the corresponding file `hfodd_path.d`.

A sample workflow for creating a PES plot from start to finish might be the following: 

1. Begin with a set of `.REC` files which are indexed in a file `hfodd_path.d` and located in some folder `restart/`. You will also need a file `hfodd_path_new.d` (as explained the the HFODD papers), plus the executable and the files `hfodd.d` and `hfodd_mpiio.d` (with `mpidef=4`). Finally, you should also create (in addition to `restart/`) the folders `out/`, `rec/`, `lic/`, and `qp/`.

2. Copy batch_splitter.py and batch_script_template.txt to the project folder, and then run batch_splitter.py in the project folder. It will break the PES into small pieces and submit each piece automatically to the queue.

3. The small chunks of PES will finish computing and automatically add their results to the project directory subfolders.

4. Once all the sub-jobs have finished running, run parseHFODDoutput.py to generate an XML array with collected data from all the output files. Then run restart_v3.py to prepare for the next run.

5. Run parseXMLoutput.py to generate an output file similar to the one created in older versions of HFODD, containing multipole moments and HFB energies as plaintext columns. *NOTE - I do this step on my personal computer by SFTP-ing the XML file onto my machine*

6. Run `PES_plotting_script.py` using the .dat file generated in the previous step. *NOTE - I do this step on my personal computer*


## batch_splitter

The HFODD option `mpidef=4` is useful for filling in "holes" in your PES, but if you are generating a complete PES then this is not a good option, because the number of processors required means your job is stuck in the queue for days. This Python script essentiall pulls that functionality out of HFODD by filling in the holes *before* HFODD even begins, which then allows you to break the PES into several smaller batches which run through the queue faster. You should specify the name of your executable and the number of tasks per batch you'd like to use in the first few lines of batch_splitter.py; everything else *should* run automatically. The script (which, I should mention, takes several minutes to run) fills in holes, breaks the project into small batches, submits the batches automatically, and moves the individual batch outputs back into one single parent directory after completion.


## min_energy

The folder `min_energy` contains some unfinished python scripts for estimating the minimum energy pathway along a PES


## density_scripts

**density.py** and **particle_counter.py** are a couple of more experimental scripts, that depend on the localization version of HFODD developed by Chunli Zhang. density.py creates cross-sectional views of the total particle density distribution of particles, and particle_counter.py is a very rough attempt to count the number of particles inside a certain region (useful for estimating the most-probable fission fragment yield).

