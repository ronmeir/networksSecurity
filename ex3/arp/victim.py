import time,commands,sys

def linux_cmd(cmd):
	ret=commands.getoutput(cmd)
	return ret

import curses
BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE = range(8)

#following from Python cookbook, #475186
def has_colours(stream):
	if not hasattr(stream, "isatty"):
		return False
	if not stream.isatty():
		return False # auto color only on TTYs
	try:
		curses.setupterm()
		return curses.tigetnum("colors") > 2
	except:
		# guess false in case of error
		return False
has_colours = has_colours(sys.stdout)


def printout(text, colour=WHITE):
	if has_colours:
		seq = "\x1b[1;%dm" % (30+colour) + text + "\x1b[0m"
		sys.stdout.write(seq)
	else:
		sys.stdout.write(text)

	
def main():
	
	'''
	#example for text coloring
	printout("[debug]   ", GREEN)
	print("in green")
	printout("[warning] ", YELLOW)
	print("in yellow")
	printout("[error]   ", RED)
	print("in red")	
	'''
	
	times=300
	oldString=""
	newString=""
	for i in xrange(times):
		print "--------------------------------["+str(i)+"/"+str(times)+"]---------------------------------------"
		newString = linux_cmd("cat /proc/net/arp")
		
		if(i==0):
			oldString=newString
		
		if(oldString==newString):
			printout(newString, GREEN)
		else:
			printout(newString, RED)
				
			
		print "-------------------------------------------------------------------------------"
		print ""
		time.sleep(0.2)
		
	
	
	return 0

if __name__ == '__main__':
	main()

