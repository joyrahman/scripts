## Instructions:
1. Run the fix_swift.sh 
which will eventually unstack and restack the cloud. Then it will run the fix_swift.py which will copy the zerocloud specific swift configuration and kill all the running proxy and object services.
2. on a new console, execute run-proxy-server.sh
3. on a another console, execute run-object-server.sh


## To kill any service any time, run

python stop_service { proxy | object }

and then initiate any service manually through execute-run-{service_name}-server.sh

