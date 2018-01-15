index=1; for file in HFODD_00*; do echo $file; filename=$(printf "HFODD_%08d.REC.bak" $index); echo $file >> path.d; mv $file $filename; let index=$index+1; done



To remove four characters from the end of the string use ${var%????}.
To remove everything after the final . use ${var%.*}.


sed -i "s/*  SPHERICAL SHAPE REQUESTED FOR THE SURFACE                                  */*  AL10 =   ZERO  AL11 =   ZERO  .............  .............  .............  *\n*                                                                             *\n*  AL20 =  0.000  AL21 =   ZERO  AL22 =   ZERO  .............  .............  */" out/hfodd_00*.out



for file in 3D-lambda05/qp/*QP*; do newname=lambda05_$(echo ${file%????} | cut -d'_' -f2); mv $file $newname; done

while read -r line; do let prev=$line+1; oldfile=$(printf "HFODD_%08d.REC" $prev); newfile=$(printf "HFODD_%08d.REC" $line); cp restart/$oldfile restart/$newfile; echo "cp restart/$oldfile restart/$newfile"; done < test.out



ls qpmas-lambda05*d >> l05-inertia.pbs
# Copy the list so each entry appears twice in the same line
sed -i "s/qpmas/srun -N 1 -n 9 -c \$OMP_NUM_THREADS \$EXECUTABLE 4 qpmas/" l05-inertia.pbs
sed -i "s/\.dqpmas/\.d >\& qpmas/" l05-inertia.pbs
sed -i '0~58 s/$/\nwait/g' l05-inertia.pbs
