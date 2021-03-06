
from Crypto.PublicKey import RSA
import socket
import sys
import random
from random import randint


def get_bob_ip():
	return '127.0.0.1'
	
def bob_get_bob_port():
	s= str(bob_load_from_file("bob/port","bob/port",'port'))
	
	if(s==''):
		save('12345','bob/port')
		return 12345
		
	else:
		u = unicode(s)
		if(u.isnumeric()):
			return int(s)
	
	save('12345','bob/port')
	return 12345
		

	
def save(data,saveTo):
	
	file = open(saveTo, "w")
	file.write(str(data)) #save exported PK_0 key
	file.close()
		
	
	
def bob_create_welcome_socket(debug):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if(debug):
		print '-------------------------------------------------'
		print ' start with socket				-'
		print ' 	Socket created				-'
	 
	#1st connection trail 
	try:
		port=int(bob_get_bob_port())
		if(debug):
			print('	PORT:'+str(port)+'				-')
		s.bind((get_bob_ip(),port ))
		save(port,'bob/port')
	except socket.error , msg:
		if(debug):
			print('Bind failed, rebinding')
		
		#2nd connection trail 
		try:
			port= randint(1030,60000)
			s.bind((get_bob_ip(), port))
			if(debug):
				print('	PORT:'+str(port)+'				-')
			save(port,'bob/port')
			
		except socket.error , msg:
			print('Bind failed, rebinding')
			#3rd connection trail 
			try:
				port= randint(1030,60000)
				s.bind((get_bob_ip(), port))
				if(debug):
					print('	PORT:'+str(port)+'				-')
				save(port,'bob/port')
					
			except socket.error , msg:
				#connection fail!!! - bye bye	
				print ('	Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
				sys.exit()
		
		 
	if(debug):
		print ' 	Socket bind complete			-'
	 
	s.listen(10)
	if(debug):
		print ' 	Socket now listening			-'
		print ' done with socket				-'
		print '-------------------------------------------------\n'
	 
	return s
		
	
#choose a random int from (0,1)	
def choose_random_b():
	return randint(0,1)
	
#gets a string as input and returns is first bit	
def get_first_bit_of_string(s):
	return (ord(s[0]))%2



#gets a socket to listen to
#returns the MSG alice sent on this socket	
def bob_get_from_alice(socket,debug):
	
	#wait to accept a connection - blocking call
	alice_socket, addr = socket.accept()
	data = alice_socket.recv(getReadSizeFromBuffer())
	
	if(debug):
		print '	this received from Alice:	'+data		
	return (alice_socket,data)



#gets a MSG and a socket to send the MSG on - and sends the MSG
def bob_send2Alice(toSend,alice_socket):
	alice_socket.send(toSend)


#returns how much to read from the socker buffer
def getReadSizeFromBuffer():
	return 1000	
		
	
	
	
#returns a random string to be used for the transform	
def choose_random_s(length=random.randint(1,120)):
	'''s= [chr(random.choice([i for i in range(ord('A'),ord('z'))])) for r in xrange(50)] '''
	#the string's LENGTH is a ramdom number from [1,120]!!!
	#otherwise alice, by the PT can easyly tell what key bob use => what is the number he wants to know (x0/x1)!!!
	
	s= [chr(random.choice([i for i in range(0,255)])) for r in xrange(length)] 
	s=''.join(s)
	return str(s)

#create r_b by the parms (s,b) of bob and the PKs from alice
#S is enc. with the relevate key choosen by b
def bob_create_r_b(pk0,pk1,b,s):

	if(b==0):
		return pk0.encrypt(s, 32)[0]
	else:
		return pk1.encrypt(s, 32)[0]
	
def bob_initial(debug):
	if(debug):
		print("Bob is running")
		print("--------------------------------------------------------------------------------\n")
		print '*************************************************'
		print '****		initial is done!!!           ****'
		print '*************************************************\n'
	return bob_create_welcome_socket(debug)
	
#gets to files loctions to read from 	 :loadFrom0,loadFrom1
#and what is to be read 
#returns the conntent to the files as a tuple
def bob_load_from_file(loadFrom0,loadFrom1,what):
	
	file = open(loadFrom0, "r")
	f0 = file.read() 
	file.close()
	
	if(what=='port'):
		return f0
	
	file = open(loadFrom1, "r")
	f1 = file.read() 
	file.close()
	
	if(what == 'PKs'):	
		f0= RSA.importKey(f0)
		f1= RSA.importKey(f1)
		
	elif(what=='Zs'):	
		f0= int(f0)
		f1= int(f1)

	return(f0,f1)


#this function gets a what bit b =(0,1) , a wellcome socket and 'debug flag'
#when xb is what we want to learn from bob (x0/x1)
#and preforms the transform
#set debug = false if you don't want any printings!!
def bob_preform_OT(b,socket,debug):
	res =False
	Xb=-1
	while (res==False):
		Xb,res=bob_OT(b,socket,debug)
	return Xb	

	
def bob_OT(b,socket,debug):
	
########## Alice a1#####################################################################
#a_1.1 alice chooses x0 and x1
#a_1.2 Alice chooses two RSA key pairs, with public keys <n0, e0>, <n1,e1>
#a_1.3 Alice sends the public keys to Bob.
#a_1.4 saves for bob the publuce keys:(  (pub_key0 ,  pub_key1 )

####################################### Bob b1  #################################################

	if(debug):
		print '************************************************************'
		print 'b1:'
	#b_1.1 bob gets from alices file 	(pub_key0,pub_key1)	
	if(debug):
		print("b_1.1:	getting public keys from alice:")
	(alice_soc,data)=bob_get_from_alice(socket,debug)
	if(data== 'PKs_are_ready'):
		(pub_key0,pub_key1)=bob_load_from_file("alice/public_key0","alice/public_key1",'PKs')
	else:
		print 'ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!! PK are not ready\n'
		sys.exit()
	if(debug):	
		print 'b_1.2:	b='+str(b) + '  => x'+str(b)+'=?'	
	

	#b_1.3 bob chooses random plaintext s 	
	s=choose_random_s()
	if(debug):
		print 'b_1.3:	the random text bob choose is:'
		print s
		print '************************************************************'

	
	#b_1.4 bob  sends rb=Enc_b[s] to Alice	- 	rb=s^eb mod nb	
	rb=bob_create_r_b(pub_key0,pub_key1,b,s)
	


	save(rb,"bob/rb")
	bob_send2Alice('Rb are ready',alice_soc)
	

########## Alice a2#####################################################################
	#a_2.1 alice gets rb from bob
	#a_2.2 dec rb with both keys
	#a_2.3 get the hardcore bit of the encryption
	#a_2.4 Alice calcs z0, z1, where zb=xb+B(sb)
	#a_2.5 alice sends to bob (z0,z1)	
####################################### Bob b2 #################################################
	
	#now bob can calc Xb
		
	(alice_soc,data)=bob_get_from_alice(socket,debug)

	#error in the decription procces
	if(data== 'MSG TOO LONG ERROR'):
		#print 'ERROR !!!!!!!!!!!!!!!! -MSG TOO LONG '
		bob_send2Alice('closing sessing',alice_soc)
		return (0,False)
		
	
	
	if(data!= 'Zs are ready'):
		print 'ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!! Zs are not ready'
		sys.exit()
		
	bob_send2Alice('z0 and z1 were received',alice_soc)
	Zs=bob_load_from_file("alice/z0","alice/z1",'Zs')
	
	if(debug):
		print str('(z0,z1) = '+str(Zs))
		
	xb=Zs[b]-int(get_first_bit_of_string(s))
	xb%=2
	return (xb,True)


		

def bob_main():
	debug =False
	socket=bob_initial(debug)
	times=7


	for i in xrange(times):	
		print 'itearation #'+str(i)
		#b_1.2 bob chooses his bit b	
		b=choose_random_b()
		Xb=bob_preform_OT(b,socket,debug)
		print 'x'+str(b)+'='+str(Xb)
		print '-------------------------------------'
		print ''
		
			
		

		


	


if __name__ == '__main__':
	bob_main()

