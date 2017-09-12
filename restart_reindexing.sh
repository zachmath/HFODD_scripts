index=1; for file in HFODD_00*; do echo $file; filename=$(printf "HFODD_%08d.REC.bak" $index); echo $file >> path.d; mv $file $filename; let index=$index+1; done



To remove four characters from the end of the string use ${var%????}.
To remove everything after the final . use ${var%.*}.


sed -i "s/*  SPHERICAL SHAPE REQUESTED FOR THE SURFACE                                  */*  AL10 =   ZERO  AL11 =   ZERO  .............  .............  .............  *\n*                                                                             *\n*  AL20 =  0.000  AL21 =   ZERO  AL22 =   ZERO  .............  .............  */" out/hfodd_00*.out



while read -r line; do let prev=$line+1; oldfile=$(printf "HFODD_%08d.REC" $prev); newfile=$(printf "HFODD_%08d.REC" $line); cp restart/$oldfile restart/$newfile; echo "cp restart/$oldfile restart/$newfile"; done < test.out
