#! /bin/bash

output_file_name="var_scalability"
popularity=-1
interval=20
end_limit=5
executable="experiment_exp2_scalability.py"
no_of_sessions=1

for i in 1 5 10 35 70 140 280 560
do

    		echo "running iteration:$i"
    		python $executable $j $no_of_sessions $popularity $manifest_file_name "$output_file_name-$i"

done

#python experiment_exp1_loadlevel.py 1 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 2 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 3 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 4 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 5 500 -1 test1.csv

