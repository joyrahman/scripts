#! /bin/bash

output_file_name="var_scalability"
popularity=-1
interval=20
end_limit=5
executable="experiment_exp2_scalability.py"
no_of_sessions=1
manifest_dir="manifest"

for i in 1 5 10 35 70 140 280 560
do
            manifest_file_name="wordcount_dir${i}mb.json"
    		echo "running iteration:$manifest_file_name"
    		python $executable $interval $no_of_sessions $popularity $manifest_dir $manifest_file_name "$output_file_name-$i"

done

#python experiment_exp1_loadlevel.py 1 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 2 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 3 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 4 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 5 500 -1 test1.csv

