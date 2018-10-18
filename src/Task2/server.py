import socket
from cryptography.fernet import Fernet

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
		if("Client connected." in str(data)):
			conn.sendall(data)
		else:
			print("THE ORIGINAL MSG:\n", decryptIt(data))
			conn.sendall(data)

	except Exception as e:
		print("TCP connection failed: ", e)
		s.close()
		break;
