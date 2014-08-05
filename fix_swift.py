import shutil
import os
import subprocess, signal 

#output = subprocess.check_output(['cd','~/devstack'])
#print output
#output = subprocess.check_output(['sh /opt/stack/devstack/unstack.sh'])
#print output
#output = subprocess.call(['sh /opt/stack/devstack/stack.sh'])
#print output


shutil.copy2('/opt/stack/proxy-server.conf','/etc/swift/proxy-server.conf')
shutil.copy2('/opt/stack/1.conf','/etc/swift/object-server/1.conf')



#proc_list = os.system('ps -ef | grep swift-object-server | grep python | cut -c 11-15').read()
#proc_list = os.popen("ps -ef | grep swift-object-server | grep python").read()

#print type(proc_list), proc_list

#i1, i2, _ =  [proc_list.split()]
#count = 0
#for i in item:
#    print i, count
#    count += 1

'''
    List the process and find object-server pid to kill 
    List the process and find proxy-server pid to kill	
    Run the process
    proc_object_server = "/opt/stack/swift/bin/swift-object-server /etc/swift/object-server/1.conf -v"	
'''

proc_list = subprocess.Popen(['ps','-ef'],stdout = subprocess.PIPE)
out,err = proc_list.communicate()
for line in out.splitlines():
    #print line
    #if 'swift-object-server' in line:
    if ('swift-proxy-server' in line) or ('swift-object-server' in line) :
        pid = int (line.split(None,2)[1])
	#print pid
	os.kill(pid,signal.SIGKILL)

print "please run the servers manually"
#proc_object_server = "/opt/stack/swift/bin/swift-object-server /etc/swift/object-server/1.conf -v"  
    	
	
