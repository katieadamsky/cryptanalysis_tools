'''
 Script to brute force decrypt a cipher that is first enciphered with playfair, then with 
 columnar transposition. Use a multithreaded approach to test multiple attempts at once.

'''

import threading
from pycipher import ColTrans
from pycipher import Playfair
import itertools
import math
import sys

MAX_THREADS = 200

# trash
def swap(text, ch1, ch2):
	text = text.replace(ch2, '!',)
	text = text.replace(ch1, ch2)
	text = text.replace('!', ch1)
	return text

# check if plaintext contains the cribs
def check(plaintext):
	plaintext = ''.join(plaintext.split()).lower()
	if 'congressman' in plaintext or 'foolproof' in plaintext or 'liberation' in plaintext or 'congresxsman' in plaintext or 'foolproxof' in plaintext or 'foxolproof' in plaintext:
		return True
	else:
		return False

# checks if the given text is valid playfair ciphertext
def can_decipher(pf_text):
	# invalid playfair ciphertext will have pairs with duplicate letters
	text = list(pf_text)
	i = 0
	while (i < len(text)):
		if text[i] == text[i+1]:
			return False
		i += 2
	return True

def bruteforce_playfair(ciphertext):
	key = 'abcdefghiklmnopqrstuvwxyz'

	perm = list(key)
	weights = [0] * len(key)
	upper = 1
	while upper < len(perm):
		if weights[upper] < upper:
			lower = 0 if (upper % 2 == 0) else weights[upper]
			perm = swap(''.join(perm), perm[upper], perm[lower])
			text = Playfair(perm).decipher(ciphertext)
			if check(text):
				print perm
				print text
				sys.exit()
			perm = list(perm)
			weights[upper] += 1
			upper = 1
		else:
			weights[upper] = 0
			upper += 1
	return


ciphertext = 'mhstbtyifsaddntphrmlrdktohbobtpaztnfcqmqddsqcdxtermcsmbimmundckladrhcmcsmpbnbivhcmhmftmxtcthmcuepeucphhskrrrcdysgmmglezynfsxylmiaicetnqfwnnunqprcwbccfmtcsprkmctxgrtbqmrkyaxvqzgyanhwnahoqxfgmucnymmogkngnbtsfyddbwhroyanmdaxcizrqnweqqtbffszayoaibirshchsqfhdoqckecpereemakofrcxynlicqonnmiezfqxeecdcerlvsyzdytlcsikrlxccauiecmnvchkedgckhrnuyafuyuklrdzidkyhkeelcoonlxwfdcnddninqhacoxrbxnkkcbqemrknbcymeygzrgmdesizmqxkirairednaafiudmulioiimueezdxccdamhruothtdscmhksvheeehhesidyoklaqqbzstmystbxcieuuuicruaamqxqlqrmzhdsuysuxqmmzmemmqxkqfurmeefiempdnkukrgtofmnwgirmxodaruupxseceehoedrfeprsdiehethxaixtyeuqimneckyelccdmuytfcnnmznngoemcptciobphomckmncmceevzpcamosktzdccaxdhlihppemddqtxrhohkksrxhhkmixuvmicmxdqoeahumqzslcakhstqphippxuppchddtcmqyhnasoxpeumligmkeimpfqoacqplresdxscdfcdlcehhhcmdhbmuoqzapaccttmqrmpzeakcgsagpqsccitsfmmfoqmcfxeiirkdcmglhdmumixmfrpahvuaeuhmgncikhmpcxiplnqmplhcctpcqpxemskcecsdcmcuvqcsiseimtvmklsdcaimyhciqpqedahcycudahmxvxcqqurtgerchwfwdttcrecsebivrfrnqicnkyerqvnymyckpnsxgdepgsbmmrazhclcccqhsyhgcxymkyvrndigytcbgcnecshxfnctkeecpn'

# key length is not 6, as none of them generate valid playfair text
# try 9 - doesn't work
# try 12 - hypothesis: key is length 12
# all_ct_keys = permute('abcdefghiklm')

word = 'abcdefghij'


perm = list(word)
weights = [0] * len(word)
upper = 1
threads = []
unran = []

# iterate through every possible columnar transposition
while upper < len(perm):
	if weights[upper] < upper:
		lower = 0 if (upper % 2 == 0) else weights[upper]
		perm = swap(''.join(perm), perm[upper], perm[lower])
		pf_text = ColTrans(perm).decipher(ciphertext)
		if can_decipher(pf_text):
			# if valid playfair text is produced, start a new thread to attack the playfair
			t = threading.Thread(target = bruteforce_playfair, args = (pf_text,))
			threads.append(t)
			if len(threading.enumerate()) < MAX_THREADS:
				print perm
				t.start()
			else:
				unran.append(t)

		perm = list(perm)
		weights[upper] += 1
		upper = 1
	else:
		weights[upper] = 0
		upper += 1

# run the threads that got skipped before
if len(unran) > 0:
	for i in range(len(unran)):
		while len(threading.enumerate()) < MAX_THREADS:
			t = unran[i]
			t.start()

