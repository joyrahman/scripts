#!/bin/bash
copy_to_node(){
    # $1=> node_ip
    # $2=> username
    password="joy123"
    echo "copying to $2@$1"
    fulldestworker=$2@$1
    scp /etc/swift/*.gz ${fulldestworker}:/etc/swift
    sshpass -p ${password} ssh ${fulldestworker } 'sudo swift-init all restart'


}

username="joy"
destmaster="10.20.109.9"
mkdir -p ./logs
zonename=1

for destworker in $(<~/workers); do
  echo "running"
  if [[ $destworker =~ ^[^\#] ]]
  then
     #fulldestworker=$username'@'$destworker
     #echo $destworker $destmaster $username

     #add_to_ring  $destworker $zonename $username $destmaster
     #rebalance_ring
     copy_to_node $destworker $username
  fi
done


wait