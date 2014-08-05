#!/usr/bin/env bash




cd /opt/stack/devstack/
./unstack.sh
./stack.sh
python fix_swift.py

echo "please run the object server and proxy server in two different shells" 
