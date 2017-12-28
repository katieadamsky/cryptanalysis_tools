import utility
import binascii

# Decode single-byte XOR cipher
# ciphertext should be a hex-encoded string
# key should be a single character
def decodeXOR(ciphertext, key):
	btext = [ord(binascii.unhexlify(ciphertext[i: i+2])) for i in range(0, len(ciphertext), 2)]
	bkey = bytearray(key)
	plaintext = ''
	for i in range(len(btext)):
		plaintext += chr(btext[i] ^ bkey[0])
	return plaintext

# Encode message using single-byte character as the key to a bitwise XOR cipher	
def encodeXOR(plaintext, key):
	btext = bytearray(plaintext)
	bkey = bytearray(key)
	message = ''
	for i in range(len(btext)):
		message += chr(btext[i] ^ bkey[0])
	return binascii.hexlify(message)

# given just ciphertext, try all possible 1-byte keys until text is revealed
def bruteforceXOR(ciphertext):
	min_score = 10000
	message = ''
	for i in range(0, 255):
		text = decodeXOR(ciphertext, chr(i))
		score = utility.score(text)
		if score < 100000 :
			if score < min_score:
				message = text
				min_score = score
	return message


file = open('test.txt', 'r')
candidates = []
minscore = 100000
linenum = 1
for line in file:
	message = bruteforceXOR(line.strip())
	score = utility.score(message)
	for ch in message:
		if ord(ch) < 31:
			continue
	if score < 60:
		print message + ' ' + str(score)
		print line + ' ' + str(linenum)
	linenum += 1

# print bruteforceXOR('1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736')
