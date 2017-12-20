

def convert_64(hex_string):
	return hex_string.decode("hex").encode("base64")

def produce_xor(str1, str2):
	binary1 = str1.decode("hex")
	binary2 = str2.decode("hex")
	xor = "".join(chr(ord(b1) ^ ord(b2)) for b1, b2 in zip(binary1, binary2))
	return xor.encode("hex")


print(produce_xor("1c0111001f010100061a024b53535009181c","686974207468652062756c6c277320657965"))