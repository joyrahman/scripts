#!/bin/bash
add_to_ring(){
    # $1 = > destworker
    # $2 = > Zone
    # insert into proxy
    echo "adding to ring $1 in zone$2"
    cd /etc/swift/
    swift-ring-builder account.builder add z$2-$1:6002/sdb1 100
    swift-ring-builder container.builder add z$2-$1:6001/sdb1 100
    swift-ring-builder object.builder add z$2-$1:6000/sdb1 100
}

rebalance_ring(){
    # rebalance the ring
    echo "balancing ring"
    swift-ring-builder /etc/swift/account.builder rebalance
    swift-ring-builder /etc/swift/container.builder rebalance
    swift-ring-builder /etc/swift/object.builder rebalance
    sudo swift-init proxy restart

}
copy_to_node(){
    # $1=> node_ip
    # $2=> username 
    password="joy123"
    echo "copying to $2@$1"
    fulldestworker=$2@$1
    scp /etc/swift/*.gz ${fulldestworker}:/etc/swift
    sshpass -p ${password} ssh ${fulldestworker} 'sudo swift-init all restart'


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
     echo $destworker $destmaster $username
     
     #add_to_ring  $destworker $zonename $username $destmaster
     rebalance_ring
     copy_to_node $destworker $username
  fi
done


wait

