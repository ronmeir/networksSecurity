
from Crypto.PublicKey import RSA


#this is bobs secret
def bob_choose_random_b():
	return 1
	
def get_first_bit_of_string(s):
	return (ord(s[0]))%2

	
	
	
	
#a random string uses for the transform	
def bob_choose_random_s():
	return "aaa helow to you"	

#create r_b by the parms (s,b) of bob and the PKs from alice
#S is enc. with the relevate key choosen by b
def bob_creat_r_b(pk0,pk1,b,s):
	r_b=0
	if(b==0):
		r_b = pk0.encrypt(s, 32)
	else:
		r_b = pk1.encrypt(s, 32)
	return r_b
	



def alice_choose_x0_x1():
	x0=0
	x1=1
	return (x0,x1)

def alice_createKeys():
	RSAkey0 = RSA.generate(1024)
	RSAkey1 = RSA.generate(1024)
	return (RSAkey0,RSAkey1)
	
	
	
	
		

def main():

########## Alice 1#####################################################################


#alice chooses x0 and x1
	x0,x1=alice_choose_x0_x1()

#Alice chooses two RSA key pairs, with public keys <n0, e0>, <n1,e1>
	key0,key1=alice_createKeys()
	
	pub_key0 = key0.publickey()
	pub_key1 = key1.publickey()
	
	
#Alice sends the public keys to Bob.
# send2Bob(  (pub_key0 ,  pub_key1 )









####################################### Bob1 #################################################
#bob gets from alice 	(pub_key0,pub_key1)	
#bob chooses his bit b	
#Bob chooses random plaintext s and sends rb=s^eb mod nb to Alice.	

	b=bob_choose_random_b()
	s=bob_choose_random_s()
		
	#rb=s^eb mod nb	
	rb=bob_creat_r_b(pub_key0,pub_key1,b,s)
	#send2Alice(rb)
	
###########################################################################################3	





		

	
	






########## Alice 2#####################################################################
#alice gets rb from bob

#Let B be a hardcore bit of the encryption
#Alice returns z0, z1, where zb=xb+B(sb)

	Bs_0= key0.decrypt(rb)
	Bs_1= key1.decrypt(rb)
	
	#print("Bs_0="+str(Bs_0))
	#print("Bs_1="+str(Bs_1))
	
	Bs_0=get_first_bit_of_string(Bs_0)
	Bs_1=get_first_bit_of_string(Bs_1)
	print("B="+str(b))
	
	if(b==0):
		print("ALICE: (Bs_0,x0)=	"+str((Bs_0,x0)))
	if(b==1):
		print("ALICE: (Bs_1,x1)=	"+str((Bs_1,x1)))
	
	print("BOB: first bit of s is:  "+str(get_first_bit_of_string(s)))
	
	z0= x0+Bs_0
	z1= x1+Bs_1
	
	print("z0= x0+Bs_0 ="+str(z0))
	print("z1= x1+Bs_1 ="+str(z1))
	

	#print("rb="+str(rb))
	
#alice sends to bob (z0,z1)
#send2Bob(z0,z1)



	
	
	
	
	
####################################### Bob1 #################################################
	


	


if __name__ == '__main__':
	main()

