'''
 Module for securely storing passwords in a database.
 Uses SHA-512 for password hashing
 Each password also has a 32-bit salt concatenated to the end for hashing
'''

import hashlib
import bcrypt

# returns true if the user authentication is successful
def authenticate(username, pw):
	# get salt and hashed pw from looking up username in db
	salt = lookup_salt(username)
	hashed_pw = lookup_hash(username)
	salted_pw = pw + salt
	hash_object = hashlib.sha512(salted_pw.encode('utf-8'))
	hex_digest = hash_object.hexdigest()
	return hex_digest == hashed_pw

# generate hash for password
# salt and pw params should be byte arrays
def hash_password(salt, pw):
	salted_pw = pw + salt
	hash_object = hashlib.sha512(salted_pw)
	hex_digest = hash_object.hexdigest()
	# store hex digest in db
	return hex_digest

# create salt for user
def gen_salt(username):
	salt = bcrypt.gensalt()
	# store salt in the database here
	return salt

print(hash_password(gen_salt('Katie'), b'katieiscool'))