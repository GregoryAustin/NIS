from cryptography.fernet import Fernet

msg = "This is the text that needs to be encrypted. Did it work?"
print("\nThis is the initial message:\n\"" + msg + "\"")

key = Fernet.generate_key()
print key
enc = Fernet(key)
print enc

enc_msg = enc.encrypt(msg)
print("\nThis is the encrypted message:\n" + enc_msg)

dec_msg = enc.decrypt(enc_msg)
print("\nThis is the decrypted message:\n\"" + dec_msg + "\"")