index=1; for file in HFODD_00*; do echo $file; filename=$(printf "HFODD_%08d.REC" $index); echo $file >> path.d; mv $file $filename; let index=$index+1; done
