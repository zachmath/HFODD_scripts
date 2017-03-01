for folder in RUN_*; do
# Customization of names and places
EXECUTABLE='./hf268f'
SCRATCH_DIR=$folder

OUTPUT=$EXECUTABLE'.txt'
RESTART_DIR=$SCRATCH_DIR'/restart/'
RECORD_DIR=$SCRATCH_DIR'/rec/'
REVIEW_DIR=$SCRATCH_DIR'/rev/'
OUTPUT_DIR=$SCRATCH_DIR'/out/'
SUMMARY_DIR=$SCRATCH_DIR'/summary/'
DENSITY_DIR=$SCRATCH_DIR'/densities/'
QP_DIR=$SCRATCH_DIR'/qp/'
LIC_DIR=$SCRATCH_DIR'/lic/'

# Stitch the individual batches back together in the parent folder

tasks_per_batch=81

folder_index=$(echo $SCRATCH_DIR | cut -d'_' -f2)
file_index=1
last_file=$(ls $RESTART_DIR | wc -l)

while [ $file_index -le $last_file ]; do

       new_index=$(bc <<< "($folder_index * $tasks_per_batch) + $file_index")

       printf -v new_index6 "%06d" $new_index

#       mv $OUTPUT_DIR/hfodd_0*000$file_index.out $SCRATCH_DIR/../out/hfodd_$new_index6.out
       cp $OUTPUT_DIR/hfodd_0*000$file_index.out $SCRATCH_DIR/../out/hfodd_$new_index6.out

       printf -v new_index8 "%08d" $new_index

#       mv $RECORD_DIR/HFODD_0*000$file_index.REC $SCRATCH_DIR/../rec/HFODD_$new_index8.REC
       cp $RECORD_DIR/HFODD_0*000$file_index.REC $SCRATCH_DIR/../rec/HFODD_$new_index8.REC
#       mv $LIC_DIR/HFODD_0*000$file_index.LIC $SCRATCH_DIR/../lic/HFODD_$new_index8.LIC
       cp $LIC_DIR/HFODD_0*000$file_index.LIC $SCRATCH_DIR/../lic/HFODD_$new_index8.LIC
#       mv $QP_DIR/HFODD_0*000$file_index.QP $SCRATCH_DIR/../qp/HFODD_$new_index8.QP
       cp $QP_DIR/HFODD_0*000$file_index.QP $SCRATCH_DIR/../qp/HFODD_$new_index8.QP

       let file_index+=1
done

# Clean up

#rm *.py *.out toto
rm -rf rev
rm -rf $DENSITY_DIR
done
