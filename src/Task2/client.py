import socket
from cryptography.fernet import Fernet

def encryptIt(msg):
    # Generating symmetric encryption key:
    key = Fernet.generate_key()
    enc = Fernet(key)

    # Encrypting with said key:
    enc_msg = enc.encrypt(msg.encode('utf-8'))

    # Returning the [encryption key, encrypted message]
    return([enc_msg, key])

HOST = '127.0.0.1'  # The server's hostname or IP address
PORT = 65435        # The port used by the server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
s.sendall(b'Client connected.')
data = s.recv(1024)

print('Received', repr(data))

while(True):
    msg = input()

    if msg != '':
        if msg == 'quit':
            s.close()
            break
        msg = encryptIt(msg)
        print('Im here')
        print(msg)
        s.sendall(bytearray(msg))
