
from Crypto.PublicKey import RSA


#this is bobs secret


def choose_random_b():
	return 1
	
def get_first_bit_of_string(s):
	return (ord(s[0]))%2
	
def get_from_alice():
	print("	this function is not ready yet!!!\n")
	aliceDate=("key0_from_soc","key1_from_soc")
	return(aliceDate) 	

def send2Alice(toSend):
	print("	this function is not ready yet!!!\n")		
	
	
	
#a random string uses for the transform	
def choose_random_s():
	return "aaa helow to you"	

#create r_b by the parms (s,b) of bob and the PKs from alice
#S is enc. with the relevate key choosen by b
def create_r_b(pk0,pk1,b,s):
	r_b=0
	
	if(b==0):
		r_b = pk0.encrypt(s, 32)
	else:
		r_b = pk1.encrypt(s, 32)
		
	return r_b
	


		

def main():

	print("Bob is running")
	print("--------------------------------------------------------------------------------\n")
	

########## Alice a1#####################################################################
#a_1.1 alice chooses x0 and x1
#a_1.2 Alice chooses two RSA key pairs, with public keys <n0, e0>, <n1,e1>
#a_1.3 Alice sends the public keys to Bob.
#a_1.4 send2Bob(  (pub_key0 ,  pub_key1 )




####################################### Bob b1  #################################################
#b_1.1 bob gets from alice 	(pub_key0,pub_key1)	
	print("getting public keys from alice:")
	(pub_key0,pub_key1)	= get_from_alice()

#b_1.2 bob chooses his bit b	
	b=choose_random_b()

#b_1.3 bob chooses random plaintext s 	
	s=choose_random_s()
	
#b_1.4 bob  sends rb=Enc_b[s] to Alice	- 	rb=s^eb mod nb	
	rb=create_r_b(pub_key0,pub_key1,b,s)
	send2Alice(rb)
	


########## Alice a2#####################################################################
	#a_2.1 alice gets rb from bob
	#a_2.2 dec rb with both keys
	#a_2.3 get the hardcore bit of the encryption
	#a_2.4 Alice calcs z0, z1, where zb=xb+B(sb)
	#a_2.5 alice sends to bob (z0,z1)	
####################################### Bob b2 #################################################
	


	


if __name__ == '__main__':
	main()

