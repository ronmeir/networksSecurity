
from garbledGate import garbled_gate 


def main():
	gate=garbled_gate('xor',Z0='z0 testing',Z1='z1 testing')
	gate.set_x(0)
	key_x= gate.get_THE_x_key()
	
	keys=gate.get_keys('y')
	
	vec= gate.get_garbled_output_vec()
	
	print gate.dec_vector(key_x,keys[0],vec)
	print gate.dec_vector(key_x,keys[1],vec)
	

	





if __name__ == '__main__':
	main()

