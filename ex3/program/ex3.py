
from Crypto.PublicKey import RSA
import socket
import sys
import random
from random import randint
import errno
from garbledGate import garbled_gate 
import pickle
import operator
import time

	
def get_bob_ip():
	return '127.0.0.1'
	
def alice_get_bob_port():
	file = open('bob/port', "r")
	f0 = file.read() 
	file.close()
	return int(f0)
	
#returns how much to read from the socker buffer	
def getReadSizeFromBuffer():
	return 1000	
	
def get_num_of_running_times():
	return 2	
#gets a string as input and returns is first bit	
def get_first_bit_of_string(s):
	return (ord(s[0]))%2

#gets 2 string s1 and s2 and returns the xored string	
#the return value will be in the length of min(leng(s1),len(s2))!!!!
def xor_2_strings(s1,s2):
	return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))
	



def get_key_length():
	return 60

	
#send to bob a message on a socket and waits for bob to respunse
#the fllow then appans accourding to bobs respunse!!	
def alice_send2BobAndRecieve(toSend):
	
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		s.connect((get_bob_ip(), alice_get_bob_port()))
	except socket.error, v:
		errorcode=v[0]
		if errorcode==errno.ECONNREFUSED:
			print "Connection Refused - problem with the socket"
			sys.exit(1)
		else:
			print v[1]
			sys.exit(1)
		
	s.send(toSend.encode())										#send
	recv=str(s.recv(getReadSizeFromBuffer()).decode('utf-8', 'ignore'))	#wait for response
	#print recv
	if(recv =='Rb are ready'):
		rb=alice_load_Rb_from_bob("bob/rb")
		return rb
	elif(recv =='z0 and z1 were received'):
		return	True

		

#gets a files address to load rb from and returns rb	
def alice_load_Rb_from_bob(loadFrom0):
	
	file = open(loadFrom0, "r")
	rb = file.read() 
	file.close()
	
	return rb
			

#get to addresses	(saveTo0,saveTo1) and 2 keys and save the keys to the addresses
def alice_save_PKs(key0,saveTo0,key1,saveTo1):
	
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
def alice_save_Zs	(z0,saveTo0,z1,saveTo1):
	file = open(saveTo0, "w")
	file.write(str(z0)) #save z0 key
	file.close()
	
	file = open(saveTo1, "w")
	file.write(str(z1)) #save z1 key
	file.close()

#here we can choose x0 and x1 randomly
#this function is good for debuging
def randomly_choose_x0_x1(b=-1):
	if(b==1):#insert b=1 for 1 bit transform
		x0=randint(0,1)
		x1=randint(0,1)
		
	elif(b==-1):#otherwise random strings with random sizes a generated 	
		x0=choose_random_s()
		x1=choose_random_s()
	else:
		x0=choose_random_s(b)
		x1=choose_random_s(b)
			
	
	return (str("value-")+str(x0),str("value-")+str(x1))
	



#creates to RSA keys
def alice_create_keys():
	RSAkey0 = RSA.generate(256*6)
	RSAkey1 = RSA.generate(256*6)
	return (RSAkey0,RSAkey1)
	
	
def alice_initial(debug):
	
	if(debug):
		print("Alice is running")
		print("--------------------------------------------------------------------------------\n")	
		print("2 RSA keys are ready")
		print '*************************************************'
		print '****		initial is done!!!           ****'
		print '*************************************************\n'
	
def alice_OT(x0,x1,debug):
	
########## Alice a1#####################################################################
	
#a_1.1 alice chooses x0 and x1
#a_1.2 Alice chooses two RSA key pairs, with public keys <n0, e0>, <n1,e1>
	(key0,key1)=alice_create_keys()
	
#a_1.3 Alice saves in file the public keys to Bob.
	#print("saving for bob: 2 PKs - (pub_key0,pub_key1) ...\n")
	alice_save_PKs(key0,"alice/public_key0",key1,"alice/public_key1")


####################################### Bob b1 #################################################
#b_1.1 bob gets from alice 	(pub_key0,pub_key1)	
#b_1.2 bob chooses his bit b	
#b_1.3 Bob chooses random plaintext s 
#b_1.4 bob sends rb=s^eb mod nb to Alice.	
###########################################################################################3	

	
########## Alice a2 #####################################################################
	#a_2.1 alice gets rb from bob
	rb= alice_send2BobAndRecieve('PKs_are_ready')
	
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
		alice_send2BobAndRecieve('MSG TOO LONG ERROR')
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
	#Bs_0=get_first_bit_of_string(Bs_0)
	#Bs_1=get_first_bit_of_string(Bs_1)
	
	if(debug):
		print("(Bs_0,x0) = "+str((Bs_0,x0)))
		print("(Bs_1,x1) = "+str((Bs_1,x1)))
	
	#a_2.4 Alice calcs z0, z1, where zb=xb+B(sb)
		print("\nresults to be send to bob are:")
	
	''' use this part if you want ot send only 1st bit of x1 and x0!!!!
	z0= (x0+Bs_0)%2
	z1= (x1+Bs_1)%2
	'''
	
	#use this part if you want to send all x1 and x0 data 
	z0=xor_2_strings(x0,Bs_0)
	z1=xor_2_strings(x1,Bs_1)
	
	if(debug):
		print("z0= x0+Bs_0 ="+z0)
		print("z1= x1+Bs_1 ="+z1)
		print("")
	

	#a_2.5 alice sends to bob (z0,z1)
	#print("bob is being informed that z0 and z1 are ready")
	alice_save_Zs(z0,"alice/z0",z1,"alice/z1")
	alice_send2BobAndRecieve('Zs are ready')
	return True
	
#this function gets x0,x1 and preforms the OT transform
#set debug to false if you don't want any printings
	
def alice_preform_OT(x0,x1,debug=False):
	res =False
	while(res==False):
		res=alice_OT(x0,x1,debug)
		
def alice_use_gate(gateKind,aliceBit,z0,z1,gate=None,pathToSave=None):
	#this gate was not entered - build one
	if (gate==None):
		a=aliceBit
		gate=garbled_gate(gateKind,Z0=z0,Z1=z1)
		gate.set_x(a)
		
		
	#use the gate	
	
	#alice sends her gate content and Kx to bob
	xKey=gate.get_THE_x_key()
	(k0y,k1y)=gate.get_keys('y')
	vec=gate.get_garbled_output_vec()
	vec.append(xKey)
	
	
	#print "saved vector:\n"+str(vec)
	if(pathToSave==None):
		save_enc_gate_vactor(vec,'./vec.txt')
	else:
		save_enc_gate_vactor(vec,pathToSave)
			
	
	#send the relevant y-key
	alice_preform_OT(k0y,k1y)
	
#def alice_are_2_bits_the_same(a_s,z0_s,z1_s):
def alice_are_2_bits_the_same(a_s,z0_s,z1_s):
	z=(z0_s,z1_s)
	'''
	andGateKx_s=[]
	andGateKy_s=[]
	gateXor=[]
	for i in xrange(2):
		tmp=garbled_gate('xor',Z0=z0_s[i],Z1=z1_s[i])
		tmp.set_x(a_s[i])
		gateXor.append(tmp)
		
		
		#AND-gate inputs
		andGateKx_s.append( z0_s[i][len('true -'):-1]  )
		andGateKy_s.append( z1_s[i][len('true -'):-1]  )
		
	andGate=garbled_gate('and',Z0='false-',Z1='true -',Kx=andGateKx_s,Ky=andGateKy_s)
	toSaveVec=andGate.get_garbled_output_vec()
	save_enc_gate_vactor(toSaveVec,'./alice/gate12.txt')
	
	for i in xrange(2):
		alice_use_gate('xor',a_s[i],z0_s[i],z1_s[i],gateXor[i],'./alice/vec'+str(i)+'.txt')
	'''

	
	
	#gateXor1=garbled_gate('xor',Z0=z0_s[0],Z1=z0_s[1])
	gateXor1=garbled_gate('xor',Z0=z[0][0],Z1=z[0][1])
	gateXor1.set_x(a_s[0])
	
	#gateXor2=garbled_gate('xor',Z0=z1_s[0],Z1=z1_s[1])
	gateXor2=garbled_gate('xor',Z0=z[1][0],Z1=z[1][1])
	gateXor2.set_x(a_s[1])
	
	#AND-gate inputs
	and_Kx=(z[0][0][len('true -'):-1] ,z[0][1][len('true -'):-1]  )
	and_Ky=(z[1][0][len('true -'):-1] ,z[1][1][len('true -'):-1]  )
	
	#create the AND-gate
	andGate=garbled_gate('and',Z0='false-',Z1='true -',Kx=and_Kx,Ky=and_Ky)
	toSaveVec=andGate.get_garbled_output_vec()
	save_enc_gate_vactor(toSaveVec,'./alice/gate12.txt')
	
	alice_use_gate('xor',a_s[0],z[0][0],z[0][1],gateXor1,'./alice/vec0.txt')
	alice_use_gate('xor',a_s[1],z[1][0],z[1][1],gateXor2,'./alice/vec1.txt')
	
	



	
	



def alice_main(debug):
	a0=1
	a1=1
	a=(a0,a1)
	z0=randomly_choose_x0_x1(get_key_length()-len('true -'))
	z1=randomly_choose_x0_x1(get_key_length()-len('true -'))
	print ('a=('+str(a0)+','+str(a1))+')'
	alice_are_2_bits_the_same(a,z0,z1)
	print ''
		

	'''
	gateKind='xor'
	alice_initial(debug) #just a print
	times=int(get_num_of_running_times())
	print 'gate kind: '+gateKind
	print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
	vec=[]
	printingVec=[]
	for i in xrange(times):
		#print 'itearation #'+str(i)
		#a_1.1 alice chooses x0 and x1
	
		#alice chooses her gate input
		a=choose_random_b()
		
		#gate output  choosen randomly - but this line can be remov
		(z0,z1)=randomly_choose_x0_x1(get_key_length()-len('true -'))
		vec.append((a,z0,z1))
		printingVec.append('i='+str(i)+':	'+'a='+str(a)+'	 z0='+str(z0)+' 	 z1='+str(z1))
		
		
		
		#z0,z1='false-'+str('0000'),'true -'+str('1111')
		#print 'z0= '+str(z0)
		#print 'z1= '+str(z1)
		
		alice_use_gate(gateKind,a,z0,z1)

		#print "a="+str(a)

		#print '-------------------------------------'
		
	for i in printingVec:
		print i
	#the 6 first chars are remove because they CONST :{'true -','false-','value-'}	
	kx=(vec[0][1][6:-1],vec[0][2][6:-1])	
	ky=(vec[1][1][6:-1],vec[1][2][6:-1])
	gate1=garbled_gate('and',Z0='false-',Z1='true -',Kx=kx,Ky=ky)
	
	toSaveVec=gate1.get_garbled_output_vec()
	
	#now check if it works
	#print gate1.dec_vector(kx[0],ky[0],toSaveVec)#00
	#print gate1.dec_vector(kx[0],ky[1],toSaveVec)#01
	#print gate1.dec_vector(kx[1],ky[0],toSaveVec)#10
	#print gate1.dec_vector(kx[1],ky[1],toSaveVec)#11
	
	save_enc_gate_vactor(toSaveVec,'./gate12.txt')
	print toSaveVec
	'''
	
	
	
	

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
	
	file = open(saveTo, "wb")
	file.write(str(data)) #save exported PK_0 key
	file.close()
	
def save_enc_gate_vactor(vec,fullPath):
	f = open(fullPath, "wb")
	pickle.dump(vec,f)          
	f.close()	

def load_enc_gate_vactor(fullPath):
	f = open(fullPath, "rb")
	vec=pickle.load(f)          
	f.close()	
	return vec	
	
	
		
	
	
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
	
	
#returns a random string to be used for the transform
def choose_random_s(length=random.randint(12,150)):
	
	#otherwise alice, by the PT can easyly tell what key bob use => what is the number he wants to know (x0/x1)!!!
	#s=''.join(chr(random.randint(ord('0'),ord('z'))) for _ in range(length))
	s=''.join(chr(random.randint(0,255)) for _ in range(length))
	s=bytes(s)

	return s

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
	
	file = open(loadFrom0, "rb")
	f0 = file.read() 
	file.close()
	
	if(what=='port'):
		return f0
	
	file = open(loadFrom1, "rb")
	f1 = file.read() 
	file.close()
	
	if(what == 'PKs'):	
		f0= RSA.importKey(f0)
		f1= RSA.importKey(f1)
		
	elif(what=='Zs'):	
		f0= f0
		f1= f1

	return(f0,f1)


#this function gets a what bit b =(0,1) , a wellcome socket and 'debug flag'
#when xb is what we want to learn from alice (x0/x1)
#and preforms the transform
#set debug = false if you don't want any printings!!
def bob_preform_OT(b,socket,debug=False):
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
	s=str(choose_random_s())
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
		
	#xb=Zs[b]-int(get_first_bit_of_string(s))
	#xb%=2
	#xb=Zs[b]+s
	xb=xor_2_strings(Zs[b],s)
	return (xb,True)

def bob_use_gate(socket,emptyGate,bobsBit,debug=False,pathToLoad=None):
	b=bobsBit
	k_y=bob_preform_OT(b,socket,debug)
	if(pathToLoad==None):
		vec= load_enc_gate_vactor('./vec.txt')
	else:
		vec= load_enc_gate_vactor(pathToLoad)
	k_x=vec[-1]
	ans=vec[0:-1]
	ans=emptyGate.dec_vector(k_x,k_y,ans)
	ans=emptyGate.get_output_from_decrypted_vector(ans)
	ans=ans[0]
	return ans
			
			
def bob_are_2_bits_the_same(socket,b0,b1):
	gateKind='xor'
	b=(b0,b1)
	vec=[]
	gate=garbled_gate(gateKind,0) 

	for i in xrange(2):
		ans=bob_use_gate(socket,gate,b[i],pathToLoad='./alice/vec'+str(i)+'.txt')
		#vec.append((b[i],ans))
		vec.append(ans)
		
	gate12=load_enc_gate_vactor('./alice/gate12.txt')
	ans= gate.dec_vector(vec[0][6:-1],vec[1][6:-1],gate12)
	ans=gate.get_output_from_decrypted_vector(ans)
	ans=ans[0][0:-1]
	return ans	
			
			
		

def bob_main(debug=False):
	socket=bob_initial(debug)
	'''
	gateKind='xor'
	gate=garbled_gate(gateKind,0)
	times=int(get_num_of_running_times())
	vec=[]
	printingVec=[]
	print 'gate kind: '+gateKind
	print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'

	for i in xrange(times):	
		#print 'itearation #'+str(i)
		b=choose_random_b()
		ans=bob_use_gate(socket,gate,b,pathToLoad='./alice/vec'+str(i)+'.txt')
		#print("ans= "+str(ans))
		#print ''
		#print ('b='+str(b))
		#print '-------------------------------------'
		printingVec.append('i='+str(i)+':	'+'b='+str(b)+'	 ans='+str(ans))
		vec.append((b,ans))
	
	for i in printingVec:
		print i	
	gate12=load_enc_gate_vactor('./alice/gate12.txt')
	#print gate12	
	#print ((vec[0][1]),vec[1][1])
	
	#decrypt the whole vector
	ans= gate.dec_vector(vec[0][1][6:-1],vec[1][1][6:-1],gate12)
	ans=gate.get_output_from_decrypted_vector(ans)
	print ans[0][0:-1]
	'''
	(b0,b1)=(choose_random_b(),choose_random_b())
	print ('b= ('+str(b0)+','+str(b1))+')'
	ans=bob_are_2_bits_the_same(socket,b0,b1)
	print 'ans = '+str(ans)
	
		
	#	k_y=bob_preform_OT(b,socket,debug)
	#	#print 'Ky'+str(b)+'='+str(k_y)+str(b)
	#	print ''
		
	#	#bob gets from alice gate content and Kx to bob
	
	#	vec= load_enc_gate_vactor('./vec.txt')
	#	#print "loaded vector\n"+str(vec)
		
	#	k_x=vec[-1]
	#	ans=vec[0:-1]
	#	ans=gate.dec_vector(k_x,k_y,ans)
	#	ans=gate.get_output_from_decrypted_vector(ans)
	#	ans=ans[0]
	#	print("ans= "+str(ans))
	#	print ('b='+str(b))
	#	print '-------------------------------------'
		
		

	


if __name__ == '__main__':

	debug=False
	numOfArgs=len(sys.argv)
	
	if(numOfArgs<=1):
		print 'the program 1st arg MUST be: bob / alice'
		print 'exiting...'
		sys.exit(1) 
	
	if(numOfArgs>3):
		print 'the program cannot have 3 or more args'
		print 'exiting...'
		sys.exit(1) 
		
		

	listOfArgs=str(sys.argv)
	listOfArgs=listOfArgs.split(",")
	name=((listOfArgs[1].split(","))[0]).split("'")[1]
	
	if(name=='bob'):
		print 'BOB\n'
	elif(name=='alice'):
		print 'ALICE\n'
	else:
		print 'the program 1st arg MUST be: bob / alice not '+str(name)
		print 'exiting...'
		sys.exit(1) 	
		
	if(numOfArgs==2):
		debug=False
		
	elif(numOfArgs==3):
		debug= (((listOfArgs[2].split(","))[0]).split("'"))[1]
		debug= (debug=='debug')
		
	if(name=='bob'):
		bob_main(debug)
	elif(name=='alice'):
		alice_main(debug)
	else:
		print 'error happand'
		
	print '--------------------------------END MAIN-----------------------------------'	
		
		

