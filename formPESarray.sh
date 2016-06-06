cd /lustre/medusa/zatore

for q22 in 00 02 04 06 08 10 12 14 16 18 20 22 24 26 28 30 minus2; do
   mkdir 22-$q22
   cp -r 22-00/* 22-$q22
   cd 22-$q22
   for folder in */; do
      cd $folder
      sed -i.bak "s_\(-2 *2 *\)[0-9][0-9]*\.[0-9]_\1$q22\.0_" hfodd_mpiio.d # Replace the q22 value with $q22

      sed -i "s_\(-2 *0 *\)[0-9][0-9]*\.[0-9]\( *\)[0-9][0-9]*\.[0-9]\( *\)[0-9][0-9]*_\101.0\2349.0\3100_" hfodd_mpiio.d # Replace the q20 values so they cover the entire range, 01.0 to 349.0 with 88 points

      sed -i.bak "s:zatore/\(30-.._22-\)00:zatore/22-$q22/\1$q22:" pbs_hfodd # Change the directory from "cd /lustre/medusa/zatore/30-.._22-00" to "cd /lustre/medusa/zatore/22-$q22/30-.._22-$q22"

      sed -i "s/-N 178-Pt-/-N 22-$q22\_/" pbs_hfodd # replace #PBS -N 178-Pt-30-?? with #PBS -N 22-$q22_30-??

      sed -i "s/walltime=..:00:00,size=[0-9][0-9]*/walltime=03:00:00,size=352/" pbs_hfodd # replace walltime and size in #PBS -l walltime=03:00:00,size=16 

      sed -i "s/aprun -n[0-9][0-9]*/aprun -n88/" pbs_hfodd # replace -n88 in aprun -n? -d4 ./hf268f &

#      sed -i "
#/wait/ a\
#cp rec/* restart/
#" pbs_hfodd # This works, but it doesn't really save any time

      sed -i.bak "s_[0-9]\.e-[0-9]_3\.e-1_" hfodd.d #replace "             ?.e-?" with the appropriate epsilon


##      sed "___" pbs_hfodd # Add "cp rec/* ../../22-`expr $q22 + 2`/30-.._22-`expr $q22 + 2`/restart/" <- This line (which would copy REC files from one sheet to the next one up) is probably not worth it. That '..' after the 30 will make things a mess, and you're going to have to disable it from everything after the first run, anyway. Yep. Delete it. I'm only leaving this here so you don't try to add it again later.

      cd ..
   done
   cd ..
done

####################################################
# This could be a separate thing, where you get the first layer going:
#cd /lustre/medusa/zatore/22-02 # Also 22--2

#for q30 in -2_22 00_22 02_22 04_22 06_22 08_22 10_22 12_22 14_22 16_22 18_22 20_22 22_22 24_22 26_22 28_22 30_22; do
#   tar -xzf /lustre/medusa/proj/Pt-178/30-$q30-00.tar.gz -C 30-$q30-02/restart
#done
