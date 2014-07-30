import os, sys
victimIP = sys.argv[1]
getMacFromIP(victimIP)	


def getMacFromIP(ip):
	# ping is optional (sends a WHO_HAS request)
	os.popen('ping -c 1 %s' % ip)

	# grep with a space at the end of IP address to make sure you get a single line
	fields = os.popen('grep "%s " /proc/net/arp' % ip).read().split()
	if len(fields) == 6 and fields[3] != "00:00:00:00:00:00":
		print fields[3]
	else:
		print 'no response from', ip
