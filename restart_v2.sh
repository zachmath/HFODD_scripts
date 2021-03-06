# This script is designed to collect the stdouts from an array of HFODD outputs. It consolidates the converged results into a single file which can be used by PES_plotting_script.py to plot a 2D potential energy surface. It also deletes .REC files in the folder rec/ which did not converge, and moves the .REC files which did successfully converge into the restart folder. If you like, it can also change various parameters of the parallel run (such as walltime, convergence parameter epsilon, etc.) in preparation for future runs.

mkdir $HOME/outputs

timestamp="$(date +%F)"
OUTDIR="$HOME/outputs/176Pt-fission/$timestamp"
mkdir $OUTDIR

rm badindices.out

for folder in 30-*; do

        grep 'divergence' $folder/summary/hf268f-loc.txt | cut -d '.' -f 1 | cut -d ' ' -f 5 > todelete.out
        while read -r line; do echo "($line + 3)/4" | bc; done < todelete.out > indices.out
	cat indices.out >> badindices.tmp
        while read -r line; do rm $folder/rec/HFODD_0*$line.REC; done < indices.out
        rm todelete.out
        rm indices.out

        grep 'failed' $folder/summary/hf268f-loc.txt | cut -d ' ' -f 6 > todelete.out
        while read -r line; do echo "$line + 1" | bc; done < todelete.out > indices.out
	cat indices.out >> badindices.tmp
        while read -r line; do rm $folder/rec/HFODD_0*$line.REC; done < indices.out
        rm todelete.out
        rm indices.out


#        rm $folder/restart/*.REC
        cp $folder/rec/*.REC $folder/restart/

	echo $folder >> badindices.out
	sort -h badindices.tmp >> badindices.out
	rm badindices.tmp

        mv $folder/summary/hf268f-loc $folder
        mv $folder/summary/*.d $folder
        mv $folder/*.qp $folder/qp/
        mv $folder/*.LIC $folder/loc/

        cat $folder/summary/hf268f-loc.txt >> outputs.dat

        cp $folder/summary/hf268f-loc.txt ~/outputs/$timestamp/$folder.out

#        sed -i.bak "s_\(-2 *0 *\)[0-9][0-9]*\.[0-9]\( *\)[0-9][0-9]*\.[0-9]\( *\)[0-9][0-9]*_\101.0\2345.0\387_" $folder/hfodd_mpiio.d # Replace the q20 values so they cover the entire range, 01.0 to 345.0 with 87 points

#        sed -i.bak "s/mv m* p* h* $SUMMARY_DIR/mv *.txt $SUMMARY_DIR/" $folder/HFODD-varyQ22.pbs-modified
#        sed -i.bak -e "s/walltime=06/walltime=05/" -e "s/nodes=[0-9][0-9]*/nodes=29/" -e "s/ttc=[0-9][0-9]*/ttc=348/" -e "s/srun -n [0-9][0-9]*/srun -n 87/" $folder/HFODD-varyQ22.pbs-modified
done

sed -i -n '/Skyrme/!p' outputs.dat
sed -i -n '/failed/!p' outputs.dat
sed -i -n '/.00000000/!p' outputs.dat
sed -i -n '/srun/!p' outputs.dat
sed -i -n '/sierra/!p' outputs.dat

sort -h outputs.dat -o outputs.dat

cp badindices.out $HOME/outputs/$timestamp/

cp outputs.dat $HOME/outputs/$timestamp/

