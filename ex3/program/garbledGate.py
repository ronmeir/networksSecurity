import random
from random import randint





#######################################################################################################################################	
#returns a random string to be used for the transform	
def choose_random_s(length):
	
	#s= [chr(random.choice([i for i in range(ord('A'),ord('z'))])) for r in xrange(50)] 
	#the string's LENGTH is a ramdom number from [1,120]!!!
	#otherwise alice, by the PT can easyly tell what key bob use => what is the number he wants to know (x0/x1)!!!
	
	s= [chr(random.choice([i for i in range(ord('0'),ord('z'))])) for r in xrange(length)] 
	s=''.join(s)

	return str(s)

				
#gets 2 string s1 and s2 and returns the xored string	
#the return value will be in the length of min(leng(s1),len(s2))!!!!
def xor_2_strings(s1,s2):
	return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))
				
############################################################################################################################################			
def key_length():
	return 14
	
def create_OTP_key():
	return 	choose_random_s(key_length())


def OTP(k,pt):
	return xor_2_strings(k,pt)




class garbled_gate:
	def __init__(self,gateType,X=-1,Z0=-1,Z1=-1):
		if(not(X==0 or X==1 or X==-1)):
			raise Exception("x MUST be from {{0,1} U None} not:"+str(X))
		
		if(not(gateType=='xor' or gateType=='and')):
			raise Exception("gate type must be:{"+str('xor')+str('and'))
			
		
		self.gate_vec=[]														#vec[i+j]=Ek_i_x[Ek_j_y[k_z(i,j)]]
		
		(self.K0_x,self.K1_x)=(create_OTP_key(),create_OTP_key())				# (k0x,k1x)
		(self.K0_y,self.K1_y)=(create_OTP_key(),create_OTP_key())				# (k0Y,k1Y)
		(self.K0_z,self.K1_z)=(create_OTP_key(),create_OTP_key())				# (k0Z,k1Z)
		
		#this helps in debuging!!
		if(Z0!=-1 and Z1!=-1):
			(self.K0_z,self.K1_z)=(Z0,Z1)
		
		
		self.x=X																# set x= {X,-1}={{1,0},-1}
		
		ENC_Zs_with_y0= (OTP(self.K0_y,self.K0_z),OTP(self.K0_y,self.K1_z))		# (Ek0y[k0z] , Ek0y[k1z])
		ENC_Zs_with_y1= (OTP(self.K1_y,self.K0_z),OTP(self.K1_y,self.K1_z))		# (Ek1y[k0z] , Ek1y[k1z])
		#test:ENC_Zs_with_y0= (OTP(self.K0_y,'yo_ko') ,OTP(self.K0_y,'yo_k1') ) # delete it
		#test:ENC_Zs_with_y1= (OTP(self.K1_y,'y1_ko') ,OTP(self.K1_y,'y1_k1') )	# delete it	
		
		
		
		
		#construct a XOR gate										# 						XOR(X,Y):							
		if(gateType=='xor'):										#				  		X	Y	Z
			self.Ek0x_Ek0y_k1z=OTP(self.K0_x,ENC_Zs_with_y0[1])		# Ek0x[Ek0y[k1z]]		0	0	1   
			self.Ek0x_Ek1y_k0z=OTP(self.K0_x,ENC_Zs_with_y1[0])		# Ek0x[Ek1y[k0z]]		0	1	0	
			self.Ek1x_Ek0y_k0z=OTP(self.K1_x,ENC_Zs_with_y0[0])		# Ek1x[Ek0y[k0z]]		1	0	0
			self.Ek1x_Ek1y_k0z=OTP(self.K1_x,ENC_Zs_with_y1[1])		# Ek1x[Ek1y[k1z]]		1	1	1
			
			 #vec[i+j]=Ek_i_x[Ekjy[k_z(i,j)]]
			self.gate_vec= [self.Ek0x_Ek0y_k1z , self.Ek0x_Ek1y_k0z , self.Ek1x_Ek0y_k0z , self.Ek1x_Ek1y_k0z]
			
		
			
		#construct an AND gate										#						AND(X,Y):
		elif(gateType=='and'):										#				   		X	Y	Z
			self.Ek0x_Ek0y_k0z=OTP(self.K0_x,ENC_Zs_with_y0[0])		# Ek0x[Ek0y[k0z]]		0	0	0
			self.Ek0x_Ek1y_k0z=OTP(self.K0_x,ENC_Zs_with_y1[0])		# Ek0x[Ek1y[k0z]]		0	1	0	
			self.Ek1x_Ek0y_k0z=OTP(self.K1_x,ENC_Zs_with_y0[0])		# Ek1x[Ek0y[k0z]]		1	0	0
			self.Ek1x_Ek1y_k0z=OTP(self.K1_x,ENC_Zs_with_y1[1])		# Ek1x[Ek1y[k1z]]		1	1	1
		
			 #vec[i+j]=Ek_i_x[Ekjy[k_z(i,j)]]
			self.gate_vec=[self.Ek0x_Ek0y_k0z , self.Ek0x_Ek1y_k0z , self.Ek1x_Ek0y_k0z , self.Ek1x_Ek1y_k0z]
		
		
	def get_keys(self,whatKey):
		if(whatKey=='x'):
			return (self.K0_x,self.K1_x)	
		
		elif(whatKey=='y'):
			return (self.K0_y,self.K1_y)	
		
		elif(whatKey=='z'):
			return (self.K0_z,self.K1_z)		
	def set_x(self,X):
		if(X== 0 or X==1):
			self.x=X
		else:
			print self.x	
			raise Exception("x MUST be from {0,1}")			
	def get_x(self):
		return self.x
	
	#returns the relevat kx acording to the x value
	def get_THE_x_key(self):
		if(self.x==-1):
			raise Exception("gate MUST contain the x val!  use :set_x(X={0,1}) to fix it")
		else:
			return self.get_keys('x')[self.x] 
		
	
	
	#return the gate's output s.t vec[i+j]=Ek_i_x[Ekjy[k_z(i,j)]]
	def get_gate_output_vec(self):
		if(self.x==-1):
			raise Exception("gate MUST contain the x val!  use :set_x(X={0,1}) to fix it")
		else:
			return 	self.gate_vec
					
	#return the garbles gate's output - we can send it to the other side
	def get_garbled_output_vec(self):
		vec= self.get_gate_output_vec()
		vec=list(vec)
		random.shuffle(vec)
		return vec 	

	#gets a vector to decrypt and  keys=(kx,ky) and decrtypt thewhole vector
	def dec_vector(self,kx,ky,vec):
		return [OTP(ky,OTP(kx,i))for i in vec]
		
	#all the keys start with "true-" so we can know it the key is ok or not	
	def get_output_from_decrypted_vector(self,vec):
		ans= [vec[i] for i in xrange(len(vec)) if (vec[i].startswith("true -")or vec[i].startswith("false-") or vec[i].startswith("value-"))]
		return ans
		
	def get_key_length(self):
		return key_length()	
		
		


	

def main():
	

	

	return 0

if __name__ == '__main__':
	main()


