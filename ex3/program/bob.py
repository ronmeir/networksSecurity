
from Crypto.PublicKey import RSA
import socket
import sys
import random
from random import randint


def get_bob_ip():
	return '127.0.0.1'
	
def get_bob_port():
	s= str(load_from_file("bob/port","bob/port",'port'))
	
	if(s==''):
		save('12345','bob/port')
		return 12345
		
	else:
		u = unicode(s)
		if(u.isnumeric()):
			return int(s)
	
	save('12345','bob/port')
	return 12345
		
	
def getReadSize():
	return 8192	
	
	
def save(data,saveTo):
	
	
	file = open(saveTo, "w")
	file.write(str(data)) #save exported PK_0 key
	file.close()
		
	
	
def create_welcome_socket(debug):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	if(debug):
		print '-------------------------------------------------'
		print ' start with socket				-'
		print ' 	Socket created				-'
	 
	#1st connection trail 
	try:
		port=int(get_bob_port())
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
		
	
	
def choose_random_b():
	return randint(0,1)
	
def get_first_bit_of_string(s):
	return (ord(s[0]))%2
	
def get_from_alice(socket,debug):
	
	#wait to accept a connection - blocking call
	alice_socket, addr = socket.accept()
	data = alice_socket.recv(1000)
	
	if(debug):
		print '	this received from Alice:	'+data		
	return (alice_socket,data)


def send2Alice(toSend,alice_socket):
	alice_socket.send(toSend)

def getReadSize():
	return 8192	
		
	
	
	
#a random string uses for the transform	
def choose_random_s():
	
	#s= [chr(random.choice([i for i in range(ord('A'),ord('z')           )])) for r in xrange(50)] 
	s= [chr(random.choice([i for i in range(0,255)])) for r in xrange(10)] 
	
	s=''.join(s)
	return str(s)
	#return "aaa helow to you"	

#create r_b by the parms (s,b) of bob and the PKs from alice
#S is enc. with the relevate key choosen by b
def create_r_b(pk0,pk1,b,s):

	if(b==0):
		return pk0.encrypt(s, 32)[0]
	else:
		return pk1.encrypt(s, 32)[0]
	
def initial(debug):
	if(debug):
		print("Bob is running")
		print("--------------------------------------------------------------------------------\n")
		print '*************************************************'
		print '****		initial is done!!!           ****'
		print '*************************************************\n'
	return create_welcome_socket(debug)
	
def load_from_file(loadFrom0,loadFrom1,what):
	
	
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

	
def OT(b,socket,debug):
	
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
	(alice_soc,data)=get_from_alice(socket,debug)
	if(data== 'PKs_are_ready'):
		(pub_key0,pub_key1)=load_from_file("alice/public_key0","alice/public_key1",'PKs')
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
	rb=create_r_b(pub_key0,pub_key1,b,s)
	


	save(rb,"bob/rb")
	send2Alice('Rb are ready',alice_soc)
	

########## Alice a2#####################################################################
	#a_2.1 alice gets rb from bob
	#a_2.2 dec rb with both keys
	#a_2.3 get the hardcore bit of the encryption
	#a_2.4 Alice calcs z0, z1, where zb=xb+B(sb)
	#a_2.5 alice sends to bob (z0,z1)	
####################################### Bob b2 #################################################
	
	#now bob can calc Xb
		
	(alice_soc,data)=get_from_alice(socket,debug)
	if(data!= 'Zs are ready'):
		print 'ERROR !!!!!!!!!!!!!!!!!!!!!!!!!!!! PK are not ready'
		sys.exit()
		
	send2Alice('z0 and z1 were received',alice_soc)
	Zs=load_from_file("alice/z0","alice/z1",'Zs')
	print str('(z0,z1) = '+str(Zs))
	xb=Zs[b]-int(get_first_bit_of_string(s))
	xb%=2
	return xb

		

def main():
	debug =False
	socket=initial(debug)
		
	#b_1.2 bob chooses his bit b	
	b=choose_random_b()

	
	Xb=OT(b,socket,False)
	print 'x'+str(b)+'='+str(Xb)
		

		


	


if __name__ == '__main__':
	main()

