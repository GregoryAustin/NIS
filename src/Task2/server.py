#!/usr/bin/python3

import socket
from cryptography.fernet import Fernet
import datetime
from datetime import timedelta

def decryptIt(msg):
	key = "bLiurzCvdG9ootkn_U2n8abt6lL2r7E0e9HiLyUYYdg=".encode() # The symmetric key
	enc = Fernet(key)

	# Decrypting with the symmetric key:
	dec_msg = enc.decrypt(msg)

	# Returning the decrypted message
	return(dec_msg)

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65437		# Port to listen on (non-privileged ports are > 1023)

print("Starting server...")
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
print("\nWaiting for a connection...")
s.listen(0)
conn, addr = s.accept()
print('Connected by', addr)
while True:
	try:
		data = conn.recv(1024)

		if not data:
			break

		print("\nTHE RECEIVED MSG:\n", str(data))
		# Skip the initial data msg bc it bugs the link out for some reason
		if("Client connected." in str(data)):
			conn.sendall(data)
		else:
			msg = decryptIt(data)
			timestamp = datetime.datetime.strptime(msg[:26].decode(), '%Y-%m-%d %H:%M:%S.%f')	# turn from byte to string to datetime
			print("HERE NOW: ", datetime.datetime.now())
			msg = msg[26:]
			# Checking timestamps ... test by making range less than microseconds=1000
			if((timestamp - timedelta(microseconds=5000)) < datetime.datetime.now() < (timestamp + timedelta(microseconds=5000))):
				print("THE ORIGINAL MSG:\n", msg)
			else:
				print("POTENTIAL RELAY ATTACK HAS OCCURED.")
				print("THE DELIVERED MSG IS:\n", msg)
			conn.sendall(data)

	except Exception as e:
		print("TCP connection failed: ", e)
		s.close()
		break;
