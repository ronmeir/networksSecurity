
from Crypto.PublicKey import RSA

def get_bob_ip():
	return '127.0.0.1'
	
def get_bob_port():
	return 12345	


def get_first_bit_of_string(s):
	return (ord(s[0]))%2
	
def send2Bob(toSend):
	print("	this function is not ready yet!!!\n")	
	
def get_rb():
	print("waiting for bob to send his rb")
	print("	this function is not ready yet!!!\n")	
	return 'some random string'

	



def choose_x0_x1():
	x0=0
	x1=1
	return (x0,x1)

def createKeys():
	RSAkey0 = RSA.generate(1024)
	RSAkey1 = RSA.generate(1024)
	return (RSAkey0,RSAkey1)
	
	
	


def main():
	global debug
	debug=True

########## Alice a1#####################################################################
	print("Alice is running")
	print("--------------------------------------------------------------------------------\n")
	
	
	#a_1.1 alice chooses x0 and x1
	x0,x1=choose_x0_x1()
	print("alice: x0 and x1 were choosen\n")


	#a_1.2 Alice chooses two RSA key pairs, with public keys <n0, e0>, <n1,e1>
	(key0,key1)=createKeys()
	pub_key0 = key0.publickey()
	pub_key1 = key1.publickey()
	print("2 RSA keys are ready")
	
	print("	sending to bob: 2 PKs - (pub_key0,pub_key1) ")
	#a_1.3 Alice sends the public keys to Bob.
	toSend=(pub_key0 ,  pub_key1 )
	send2Bob(toSend)


####################################### Bob b1 #################################################
#b_1.1 bob gets from alice 	(pub_key0,pub_key1)	
#b_1.2 bob chooses his bit b	
#b_1.3 Bob chooses random plaintext s 
#b_1.4 bob sends rb=s^eb mod nb to Alice.	
###########################################################################################3	





		

	
	
	
########## Alice a2 #####################################################################
	#a_2.1 alice gets rb from bob
	rb= get_rb()
	
	#Let B be a hardcore bit of the encryption
	
		
	#a_2.2 dec rb with both keys
	Bs_0= key0.decrypt(rb)
	Bs_1= key1.decrypt(rb)
	
	if(debug):
		print("______________________________________________")
		print("printing r_0 and r_1:")
		print("---------------------")
		print("r_0:\n "+str(Bs_0))
		print("\nr_1:\n"+str(Bs_1))
		print("\nend of r_0 and r_1 printing")
		print("______________________________________________\n")
	
	#a_2.3 get the hardcore bit of the encryption
	Bs_0=get_first_bit_of_string(Bs_0)
	Bs_1=get_first_bit_of_string(Bs_1)
	
	if(debug):
		print("debug mode")
		print("(Bs_0,x0) = "+str((Bs_0,x0)))
		print("(Bs_1,x1) = "+str((Bs_1,x1)))
	
	#a_2.4 Alice calcs z0, z1, where zb=xb+B(sb)
	print("\nresults to be send to bob are:")
	z0= (x0+Bs_0)%2
	z1= (x1+Bs_1)%2
	
	print("z0= x0+Bs_0 ="+str(z0))
	print("z1= x1+Bs_1 ="+str(z1))
	print("")
	

	#a_2.5 alice sends to bob (z0,z1)
	print("zo and z1 are now being sent to bob")
	toSend=(z0,z1)
	send2Bob(toSend)



	
	
	
	
	
####################################### Bob b2 #################################################
	


	


if __name__ == '__main__':
	main()

