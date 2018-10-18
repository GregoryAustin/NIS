#!/usr/bin/python3

import socket
from cryptography.fernet import Fernet
import datetime

def encryptIt(msg):
	key = "bLiurzCvdG9ootkn_U2n8abt6lL2r7E0e9HiLyUYYdg=".encode() # The symmetric key
	enc = Fernet(key)

	# Encrypting with said key:
	enc_msg = enc.encrypt(msg.encode('utf-8'))

	# Returning the [encryption key, encrypted message]
	return(enc_msg)

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65437		# The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b'Client connected.')
data = s.recv(1024)

print('Received', repr(data))

while(True):
	msg = input()
	
	if msg != '':
		if msg == 'quit':
			msg = "Closing connection...."
			s.sendall(msg.encode())
			print(msg)
			s.close()
			break
		msg = str(datetime.datetime.now()) + msg
		print("This is the message: ", msg)
		msg = encryptIt(msg)
		s.sendall(msg)
