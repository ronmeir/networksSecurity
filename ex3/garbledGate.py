import random
from random import randint





#######################################################################################################################################	
#returns a random string to be used for the transform	
def choose_random_s(length):
	
	#s= [chr(random.choice([i for i in range(ord('A'),ord('z'))])) for r in xrange(50)] 
	#the string's LENGTH is a ramdom number from [1,120]!!!
	#otherwise alice, by the PT can easyly tell what key bob use => what is the number he wants to know (x0/x1)!!!
	
	s= [chr(random.choice([i for i in range(0,255)])) for r in xrange(length)] 
	s=''.join(s)

	return str(s)

				
#gets 2 string s1 and s2 and returns the xored string	
#the return value will be in the length of min(leng(s1),len(s2))!!!!
def xor_2_strings(s1,s2):
	return ''.join(chr(ord(a) ^ ord(b)) for a,b in zip(s1,s2))
				
############################################################################################################################################			
def key_length():
	return 10
	
def create_OTP_key():
	return 	choose_random_s(key_length())


def OTP(k,pt):
	return xor_2_strings(k,pt)




class garbled_gate:
	def __init__(self,gateType,X=-1):
		(self.K0_x,self.K1_x)=(create_OTP_key(),create_OTP_key())				# (k0x,k1x)
		(self.K0_y,self.K1_y)=(create_OTP_key(),create_OTP_key())				# (k0Y,k1Y)
		(self.K0_z,self.K1_z)=(create_OTP_key(),create_OTP_key())				# (k0Z,k1Z)
		
		self.x=X																# set x= {X,-1}={{1,0},-1}
		
		#ENC_Zs_with_y0= (OTP(self.K0_y,'yo_ko') ,OTP(self.K0_y,'yo_k1') ) 		# delete
		#ENC_Zs_with_y1= (OTP(self.K1_y,'y1_ko') ,OTP(self.K1_y,'y1_k1') ) 		# delete
		
		ENC_Zs_with_y0= (OTP(self.K0_y,self.K0_z),OTP(self.K0_y,self.K1_z))		# (Ek0y[k0z] , Ek0y[k1z])
		ENC_Zs_with_y1= (OTP(self.K1_y,self.K0_z),OTP(self.K1_y,self.K1_z))		# (Ek1y[k0z] , Ek1y[k1z])
		
		self.enc_vec=[]
		
		#construct a XOR gate										# 						XOR(X,Y):							
		if(gateType=='xor'):										#				  		X	Y	Z
			self.Ek0x_Ek0y_k1z=OTP(self.K0_x,ENC_Zs_with_y0[1])		# Ek0x[Ek0y[k1z]]		0	0	1   
			self.Ek0x_Ek1y_k0z=OTP(self.K0_x,ENC_Zs_with_y1[0])		# Ek0x[Ek1y[k0z]]		0	1	0	
			self.Ek1x_Ek0y_k0z=OTP(self.K1_x,ENC_Zs_with_y0[0])		# Ek1x[Ek0y[k0z]]		1	0	0
			self.Ek1x_Ek1y_k0z=OTP(self.K1_x,ENC_Zs_with_y1[1])		# Ek1x[Ek1y[k1z]]		1	1	1
			
			self.enc_vec= [self.Ek0x_Ek0y_k1z , self.Ek0x_Ek1y_k0z , self.Ek1x_Ek0y_k0z , self.Ek1x_Ek1y_k0z]
			
		
				
			
			
		
		#construct an AND gate										#						AND(X,Y):
		elif(gateType=='and'):										#				   		X	Y	Z
			self.Ek0x_Ek0y_k0z=OTP(self.K0_x,ENC_Zs_with_y0[0])		# Ek0x[Ek0y[k0z]]		0	0	0
			self.Ek0x_Ek1y_k0z=OTP(self.K0_x,ENC_Zs_with_y1[0])		# Ek0x[Ek1y[k0z]]		0	1	0	
			self.Ek1x_Ek0y_k0z=OTP(self.K1_x,ENC_Zs_with_y0[0])		# Ek1x[Ek0y[k0z]]		1	0	0
			self.Ek1x_Ek1y_k0z=OTP(self.K1_x,ENC_Zs_with_y1[1])		# Ek1x[Ek1y[k1z]]		1	1	1
		
			self.enc_vec=[self.Ek0x_Ek0y_k0z , self.Ek0x_Ek1y_k0z , self.Ek1x_Ek0y_k0z , self.Ek1x_Ek1y_k0z]
		
		
	def get__private_keys(self,whatKey):
		if(whatKey=='x'):
			return (self.K0_x,self.K1_x)	
		
		elif(whatKey=='y'):
			return (self.K0_y,self.K1_y)	
		
		elif(whatKey=='z'):
			return (self.K0_z,self.K1_z)	
		
	def set_x(self,X):
		self.x=X
	def get_x():
		return self.x
		
		

			


def main():
	
	gate=garbled_gate('xor')
	
	return 0

if __name__ == '__main__':
	main()


