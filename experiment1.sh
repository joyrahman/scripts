#! /bin/bash

output_file_name="var_interval"
popularity=-1
interval=0
end_limit=5
executable="experiment_exp1_loadlevel.py"
no_of_sessions=5

for i in {1..$end_limit}
do
    echo "running iteration:$i"
    python $executable $i $no_of_sessions $popularity "$output_file_name-$i.csv"
done

#python experiment_exp1_loadlevel.py 1 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 2 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 3 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 4 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 5 500 -1 test1.csv

