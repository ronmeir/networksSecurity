import time,commands

def linux_cmd(cmd):
	ret=commands.getoutput(cmd)
	return ret
	
def main():
	times=300
	for i in xrange(times):
		print "--------------------------------["+str(i)+"/"+str(times)+"]---------------------------------------"
		print linux_cmd("cat /proc/net/arp")
		print "-------------------------------------------------------------------------------"
		print ""
		time.sleep(0.2)
		
	
	
	return 0

if __name__ == '__main__':
	main()

