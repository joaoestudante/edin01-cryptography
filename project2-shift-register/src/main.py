def lfsr(polynomial, register, base):
	if register == [0, 0, 0, 0]:
		register.append(1) # returns to main cycle

	elif ((base == 2 and register == [1, 0, 0, 0]) or
		  (base == 5 and register == [2, 0, 0, 0])):
		register.append(0) # goes to all zero register

	else: # linear behaviour
		new_register_value = 0
		for coefficient, content in zip(polynomial, register):
			new_register_value += -coefficient * content

		register.append(new_register_value % base)

	return register.pop(0)

def main():
	register2 = [0, 0, 0, 1]
	register5 = [0, 0, 0, 1]

	z2_polynomial = [1, 0, 0, 1]
	z5_polynomial = [2, 0, 2, 1]

	with open("sequence.txt", "w") as output:
		for _ in range(10003):
			out_z2 = lfsr(z2_polynomial, register2, 2)
			out_z5 = lfsr(z5_polynomial, register5, 5)
			output.write(str((5*out_z2 + out_z5)))

main()