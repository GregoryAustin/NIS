from cryptography.fernet import Fernet

msg = b"This is the text that needs to be encrypted. Did it work?"
print("\nThis is the initial message:\n\"" + str(msg) + "\"")

'''
print(isinstance(msg, basestring))
print(isinstance(msg, str))
print(isinstance(msg, bytes))
'''

key = "bLiurzCvdG9ootkn_U2n8abt6lL2r7E0e9HiLyUYYdg=".encode()	# The symmetric key
enc = Fernet(key)

enc_msg = enc.encrypt(msg)
print("\nThis is the encrypted message:\n" + str(enc_msg))
'''
print(isinstance(enc_msg, basestring))
print(isinstance(enc_msg, str))
print(isinstance(enc_msg, bytes))

# Modiifying the message messes up decryption... I don't know if that's a 'good enough' prevention or not?
#enc_msg = (enc_msg[:1] + 'z' + enc_msg[2:]).encode()
print(isinstance(enc_msg, basestring))
print(isinstance(enc_msg, str))
print(isinstance(enc_msg, bytes))

print("\nThis is the encrypted message after modification:\n" + enc_msg)
'''

enc_msg = bytes(enc_msg)
key = bytes(key)
enc = Fernet(key)

dec_msg = enc.decrypt(enc_msg)
print("\nThis is the decrypted message:\n\"" + str(dec_msg) + "\"")