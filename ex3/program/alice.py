
from Crypto.PublicKey import RSA
import socket
import sys
from random import randint

	
def get_bob_ip():
	return '127.0.0.1'
	
def get_bob_port():
	file = open('bob/port', "r")
	f0 = file.read() 
	file.close()
	return int(f0)
	
#returns how much to read from the socker buffer	
def getReadSizeFromBuffer():
	return 1000	
	
	
#gets a string as input and returns is first bit	
def get_first_bit_of_string(s):
	return (ord(s[0]))%2
	

#send to bob a message on a socket and waits for bob to respunse
#the fllow then appans accourding to bobs respunse!!	
def send2BobAndRecieve(toSend):
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((get_bob_ip(), get_bob_port()))
	except ConnectionRefusedError:
		print("Connection refused")
		return False
		
	s.send(toSend.encode())										#send
	recv=str(s.recv(getReadSizeFromBuffer()).decode('utf-8', 'ignore'))	#wait for response
	#print recv
	if(recv =='Rb are ready'):
		rb=load_Rb_from_bob("bob/rb")
		return rb
	elif(recv =='z0 and z1 were received'):
		return	True

		

#gets a files address to load rb from and returns rb	
def load_Rb_from_bob(loadFrom0):
	
	file = open(loadFrom0, "r")
	rb = file.read() 
	file.close()
	
	return rb
			

#get to addresses	(saveTo0,saveTo1) and 2 keys and save the keys to the addresses
def save_PKs(key0,saveTo0,key1,saveTo1):
	
	pubkey0=key0.publickey()
	pubkey1=key1.publickey()
	
	file = open(saveTo0, "w")
	file.write(pubkey0.exportKey()) #save exported PK_0 key
	file.close()
	
	file = open(saveTo1, "w")
	file.write(pubkey1.exportKey()) #save exported PK0 key
	file.close()

	'''
	print 'the keys are:'
	print pubkey0.exportKey()
	print ''
	print ''
	print pubkey1.exportKey()	
	'''

#get to addresses	(saveTo0,saveTo1) and 2 Zs and save the Zs to the addresses
def save_Zs	(z0,saveTo0,z1,saveTo1):
	file = open(saveTo0, "w")
	file.write(str(z0)) #save z0 key
	file.close()
	
	file = open(saveTo1, "w")
	file.write(str(z1)) #save z1 key
	file.close()

	


#here we can choose x0 and x1 randomly
#this function is good for debuging
def randomly_choose_x0_x1():
	x0=randint(0,1)
	x1=randint(0,1)
	return (x0,x1)

#creates to RSA keys
def createKeys():
	RSAkey0 = RSA.generate(1024)
	RSAkey1 = RSA.generate(1024)
	return (RSAkey0,RSAkey1)
	
#creates a wellcome socket	
def create_welcome_socket():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if(debug):
		print '-------------------------------------------------'
		print ' start with socket				-'
		print ' 	Socket created				-'
	 
	try:
		s.bind((get_bob_ip(), get_bob_port()))
	except socket.error , msg:
		print '	Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()
	if(debug):	 
		print ' 	Socket bind complete			-'
	 
	s.listen(10)
	if(debug):
		print ' 	Socket now listening			-'
		print ' done with socket				-'
		print '-------------------------------------------------\n'
	 
	return s
	
def initial(debug):
	
	if(debug):
		print("Alice is running")
		print("--------------------------------------------------------------------------------\n")	
		print("2 RSA keys are ready")
		print '*************************************************'
		print '****		initial is done!!!           ****'
		print '*************************************************\n'
	
def OT(x0,x1,debug):
	
########## Alice a1#####################################################################
	
#a_1.1 alice chooses x0 and x1
#a_1.2 Alice chooses two RSA key pairs, with public keys <n0, e0>, <n1,e1>
	(key0,key1)=createKeys()
	
#a_1.3 Alice saves in file the public keys to Bob.
	#print("saving for bob: 2 PKs - (pub_key0,pub_key1) ...\n")
	save_PKs(key0,"alice/public_key0",key1,"alice/public_key1")


####################################### Bob b1 #################################################
#b_1.1 bob gets from alice 	(pub_key0,pub_key1)	
#b_1.2 bob chooses his bit b	
#b_1.3 Bob chooses random plaintext s 
#b_1.4 bob sends rb=s^eb mod nb to Alice.	
###########################################################################################3	

	
########## Alice a2 #####################################################################
	#a_2.1 alice gets rb from bob
	rb= send2BobAndRecieve('PKs_are_ready')
	
	#Let B be a hardcore bit of the encryption
	
	#a_2.2 dec rb with both keys
	try:
		#sometimes we get an error saying that the msg is too large
		Bs_0= key0.decrypt(rb)
		Bs_1= key1.decrypt(rb)
	except ValueError, e:
		if(debug):
			print 'printing error'
			print e
		send2BobAndRecieve('MSG TOO LONG ERROR')
		return False
	
		
		
		Bs_0= key0.decrypt(rb)
		Bs_1= key1.decrypt(rb)
		
		
	
	if(debug):
		print("______________________________________________")
		print("printing r_0 and r_1:")
		print("---------------------")
		print("r_0:\n"+str(Bs_0))
		print("\nr_1:\n"+str(Bs_1))
		print("\nend of r_0 and r_1 printing")
		print("______________________________________________\n")
	
	#a_2.3 get the hardcore bit of the encryption
	Bs_0=get_first_bit_of_string(Bs_0)
	Bs_1=get_first_bit_of_string(Bs_1)
	
	if(debug):
		print("(Bs_0,x0) = "+str((Bs_0,x0)))
		print("(Bs_1,x1) = "+str((Bs_1,x1)))
	
	#a_2.4 Alice calcs z0, z1, where zb=xb+B(sb)
		print("\nresults to be send to bob are:")
	
	z0= (x0+Bs_0)%2
	z1= (x1+Bs_1)%2
	
	if(debug):
		print("z0= x0+Bs_0 ="+str(z0))
		print("z1= x1+Bs_1 ="+str(z1))
		print("")
	

	#a_2.5 alice sends to bob (z0,z1)
	#print("bob is being informed that z0 and z1 are ready")
	save_Zs(z0,"alice/z0",z1,"alice/z1")
	send2BobAndRecieve('Zs are ready')
	return True
	
#this function gets x0,x1 and preforms the OT transform
#set debug to false if you don't want any printings
	
def preform_OT(x0,x1,debug):
	res =False
	while(res==False):
		res=OT(x0,x1,debug)

		
	
		
	
	


def main():
	debug=False
	initial(debug) #just a print
	times=20

	for i in xrange(times):
		print 'itearation #'+str(i)
		#a_1.1 alice chooses x0 and x1
		x0,x1=randomly_choose_x0_x1()	#randomly - but this line can be remove
		preform_OT(x0,x1,debug)
		print 'x0= '+str(x0)
		print 'x1= '+str(x1)
			
		print '-------------------------------------'
	




	
	
	
	
	
####################################### Bob b2 #################################################
	


	


if __name__ == '__main__':
	global debug

	main()

