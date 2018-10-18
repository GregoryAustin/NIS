
import socket
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# program title
print ("\nClient\n")

# The server's hostname or IP address
HOST = '127.0.0.1'

# The port used by the server
PORT = 0

# create socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# try connect to server
print ("Waiting for server...")
while (True):
    try:
        # check which port the server is on
        with open("port") as in_file:
            value = in_file.readlines()
            in_file.close()
        
        # set port that server is on
        if not (len(value) < 1):
            PORT = int(value[0])
          
        # try make connection
        s.connect((HOST, PORT))
        break
    
    # wait for connection
    except:
        continue

# connected to server
print ("Connected to server.")

# recieve key from server
key = s.recv(PORT)
enc = Fernet(key)

# user prompt
print ("You can now send messages to the server:\n")

# check 
while(True):
    # gather user input message to send
    msg = input()
    
    # if not a blank message
    if msg != '':
        
        # terminate connection if 'quit' is requested
        if msg == 'quit':
            s.close()
            break
        
        # add 512-bit hash cryptographic hash function value
        h = hashes.Hash(hashes.SHA512(), backend=default_backend())
        h.update(msg.encode('utf-8'))
        hash_value = h.finalize()
        
        # create data to send
        data = hash_value + msg.encode('utf-8')
        
        # encrypt message
        msg_enc = enc.encrypt(data)
        
        # send message
        s.sendall(msg_enc)
