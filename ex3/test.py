
from Crypto.PublicKey import RSA
import socket
import sys
from random import randint
import errno




def create_PK(RSA_key):
	return RSA_key.publickey()

 
def create_SK():
	RSAkey = RSA.generate(1024)
	return RSAkey

def enc(PK,m):
	return PK.encrypt(long(m), 32)

def dec(SK,CT):
	return SK.decrypt(CT)
	
def enc_list(PK,listToEnc):
	return [enc(PK,long(i))for i in listToEnc]

def dec_list(SK,listToDec):
	return [dec(SK,i) for i in listToDec]		
	
	
	
	


def main():
	'''RSA= create_key()
	m= (5,True,'test')
	CT=RSA.publickey().encrypt(long(True), 32)
	PT=RSA.decrypt(CT)
	print(PT)'''
	
	sk=create_SK()
	pk=create_PK(sk)
	
	
	m=[1,5,3,4]
	ct=enc_list(pk,m)
	pt= dec_list(sk,ct)
	print (pt,m)
	print(m==pt)








if __name__ == '__main__':
	main()

