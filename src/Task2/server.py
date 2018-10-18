import socket
from cryptography.fernet import Fernet

def decryptIt(msg):
    enc_msg = msg[0]
    enc = Fernet(msg[1])

    # Decrypting with the symmetric key:
    dec_msg = enc.decrypt(enc_msg)

    return(dec_msg)

HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65435        # Port to listen on (non-privileged ports are > 1023)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(0)
conn, addr = s.accept()
print('Connected by', addr)
while True:
    try:
        data = conn.recv(1024)

        if not data:
            break

        data = decryptIt(data)
        print(data)
        conn.sendall(data)

    except Exception:
        break;