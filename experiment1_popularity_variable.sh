#! /bin/bash

output_file_name="var_popularity"
popularity=-1
interval=10
end_limit=5
#executable="experiment_exp1_loadlevel.py"
executable="experiment_exp1_popularity.py"
no_of_sessions=1

for i in 0 50 80
do
   echo "running iteration:$i, $j"
   python $executable 1 $no_of_sessions $i "$output_file_name-1_pop$i"
done

#for i in 0 10 20 30 40 50 60 70 80 90 100
#do      
#   echo "running iteration:$i, $j"
#   python $executable 2 $no_of_sessions $i "$output_file_name-2_pop$i"
#done

#for i in 0 10 20 30 40 50 60 70 80 90 100
#do      
#   echo "running iteration:$i, $j"
#   python $executable 3 $no_of_sessions $i "$output_file_name-3_pop$i"
#done

#for i in 0 10 20 30 40 50 60 70 80 90 100
#do      
#   echo "running iteration:$i, $j"
#   python $executable 4 $no_of_sessions $i "$output_file_namer-4_pop$i"
#done

#for i in 0 10 20 30 40 50 60 70 80 90 100
#do      
#   echo "running iteration:$i, $j"
#   python $executable 5 $no_of_sessions $i "$output_file_name-5_pop$i"
#done





#python experiment_exp1_loadlevel.py 1 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 2 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 3 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 4 500 -1 test1.csv
#python experiment_exp1_loadlevel.py 5 500 -1 test1.csv

