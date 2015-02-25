#! /bin/bash

output_file_name="var_popularity"
popularity=-1
interval=1
end_limit=5
executable="experiment_exp1_loadlevel.py"
no_of_sessions=200

for i in 0 10 20 30 40 50 60 70 80 90 100
do
    echo "running iteration:$i"
    i=$i+10
    python $executable $interval $no_of_sessions $i "$output_file_name-$i.csv"
done

#python experiment_exp1_loadlevel.py 1 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 2 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 3 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 4 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 5 500 -1 test1.csv

