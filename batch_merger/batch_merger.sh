parent_directory=$(pwd)

tasks_per_batch=81 # Multiples of three help, assuming 3 tasks/node (=> 27 nodes)
### NOTE: THIS IS ALREADY ASSUMED IN THE TEMPLATE FILE!!! I HAVEN'T GENERALIZED IT YET
### (probably the best way to generalize would be to use a regex instead of a specific number)


### STITCHING IT BACK TOGETHER - move this to the batch script template!!!
### Then just have each of them move stitch themselves back into the main folder
### This recipe is completely deterministic, so you don't have to worry about them doing it out of order

### This script will work for the jobs you already have running, but in the future, just move this functionality into the batch submission script and let them take care of it themselves.

for folder in RUN_*; do

        folder_index=$(echo $folder | cut -d'_' -f2)
        file_index=1
        last_file=$(ls $folder/restart | wc -l)

        while [ $file_index -le $last_file ]; do

               new_index=$(bc <<< "($folder_index * $tasks_per_batch) + $file_index")

               printf -v new_index "%06d" $new_index

#                mv $folder/out/hfodd_0*000$file_index.out out/hfodd_$new_index.out
               cp $folder/out/hfodd_0*000$file_index.out out/hfodd_$new_index.out

               printf -v new_index "%08d" $new_index

#                mv $folder/rec/HFODD_0*000$file_index.REC rec/HFODD_$new_index.REC
               cp $folder/rec/HFODD_0*000$file_index.REC rec/HFODD_$new_index.REC
#                mv $folder/lic/HFODD_0*000$file_index.LIC lic/HFODD_$new_index.LIC
               cp $folder/lic/HFODD_0*000$file_index.LIC lic/HFODD_$new_index.LIC
#                mv $folder/qp/HFODD_0*000$file_index.QP qp/HFODD_$new_index.QP
               cp $folder/qp/HFODD_0*000$file_index.QP qp/HFODD_$new_index.QP

               let file_index+=1
        done
done

