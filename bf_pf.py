'''Bruteforce just playfair cipher'''
''' 
plan: use simulated annealing to hill climb to maximize the correlation to English 
When a peak is reached, print it and start over
'''


from pycipher import Playfair
import threading
import math
import sys
import numpy


# one thread for each hill being climbed
MAX_THREADS = 600

def check(plaintext):
	# frequency distribution of regular english
	english = [8.167,1.492,2.782,4.253,12.702,2.228,2.015,6.094,
		6.966,0.153,0.772,4.025,2.406,6.749,7.507,1.929,
		0.095,5.987,6.327,9.056,2.758,0.978,2.360,0.150,1.974,0.074]
	# count frequency of each letter in the plaintext
	freq = [0]*26
	plaintext = plaintext.lower()
	for letter in plaintext:
		freq[ord(letter) - 97] += 1
	for i in range(len(freq)):
		temp = freq[i]
		temp = (float(temp)/len(plaintext))*100
		freq[i] = temp
	return numpy.corrcoef(english, freq)[0,1]

def swap(text, ch1, ch2):
	text = text.replace(ch2, '!',)
	text = text.replace(ch1, ch2)
	text = text.replace('!', ch1)
	return text


#climb one hill in search space 
def hillclimb_playfair(key, ciphertext):

	perm = list(key)
	weights = [0] * len(key)
	upper = 1
	while upper < len(perm):
		if weights[upper] < upper:
			lower = 0 if (upper % 2 == 0) else weights[upper]
			perm = swap(''.join(perm), perm[upper], perm[lower])
			text = Playfair(perm).decipher(ciphertext)
			if check(text) > 0.8:
				print perm
				print text
				return
			perm = list(perm)
			weights[upper] += 1
			upper = 1
		else:
			weights[upper] = 0
			upper += 1
	return



key = 'etaoinshrdlubcfgkmpqvwxyz'
key2 = 'ghiklabcdefmnopqrstuvwxyz'
key3 = 'ghiklfmnopqabcderstuvwxyz'
ciphertext = 'tilcmuufgvnloemvuwolucdiitquuemlqkmvwmmurnflqlunuhgxsaciowcthugcgfurqopodgwmaqxcbnlodlnuuxeiudikavrueuldwrgvvnznurncmzqnmvtywagwzukfgapouretsricduadzkcuufuhmukfbzrhkyleapeuldqladuksivduzxccurnknqokltgawgslogxcyhuklotrueyoeveucuhoneuwufueuaqzoxcfllcmuuvdupikiflivmlxcfhadamcwkffgieowimvliclzipreloaxeiudlwxcnuurfgucxccnnkaiknzneurgkfadmzzuawawygmqowticfbdcypocunfomtiknvocurhqnlzurmluvxcnwwgfmsgwuciopylxcklicnblhmurngdurnuugbvopfmmuvglymgvnuemucinmfmsgwueupmlvgxkffmmlicqzmnlobnqodipobqucocmvfdqliemlpdwgwdogekeucnrlcxaqrumvxcfktnlorilvonrlcxingtclvyhinwlohugogaflqlzneurgkfunzoebdupnkffdpaflimhlkfawbchlnwzmtnopqlgbqatezmluurgukfgbknylnuxgknlbuceynmnicaicuvmuciknucydaqknxcbndaavbqawbcficirxrncnbgicnblhmurubnowwqagvmwqevnbxcgvgxnaflimruzuqwsfncvahufcwmlcuzxccifldeloamevurxceuhbnwawliydaqikuzucvtniudopylxcklicnblhmufmomylcieulrzmloeuucicmzeulggvancrgokiwuxfgwbnxcnlnkworuxfgwbnxcnlnkwolofuvsimvprbtcgbknylnuwguzxccnqnnuuzxccinemonwnkizxgqoxrnwnkuhxcgwzueyzbnvmumzkfavrxwagvpavrcigwvnoevmtgkfogekeufhpffloldimzozqolhvtkfxccixcknlwivloopiceuifmzrlgweulmfufmsgwugwvnolguqwnaqz'

threads = []
while len(threading.enumerate()) < MAX_THREADS:
	t = threading.Thread(target = hillclimb_playfair, args = (ciphertext,key,))
	threads.append(t)
	key = ''.join(numpy.random.permutation(list(key)))
	t.start()


print "All threads generated. Just sit tight for a million years"

