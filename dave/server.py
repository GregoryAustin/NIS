
import sys
import socket
from cryptography.fernet import Fernet
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def hacked():
    print ("Warning, you may have been hacked.")
    file = open("log.txt", 'a')
    file.write("\nWarning, you may have been hacked.")
    file.close()    

# program title
print ("\nServer\n")

# clear log file
file = open("log.txt", 'w')
file.write("")
file.close()

# clear port file
file = open("port", 'w')
file.write("")
file.close()

# Standard loopback interface address (localhost)
HOST = '127.0.0.1'

# Port to listen on (non-privileged ports are > 1023)
PORT = 1024

# create server and look for an empty port
while (True):
    try:
        # try create a socket using current port number
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        file = open("port", 'w')
        file.write(str(PORT))
        file.close()
        break
    
    # if port is in use
    except:
        PORT += 1
        if (PORT > 9999):
            print ("No ports available.")
            sys.exit()

# wait for a client to connect
print ("Waiting for a client...")
s.listen(0)
conn, addr = s.accept()
file = open("port", 'w')
file.write("")
file.close()

# client connected
print("Connected: " + str(addr) + "\n")
file = open("log.txt", 'a')
file.write("\nConnected: " + str(addr) + "\n")
file.close()

# generate and send encryption key to client
key = Fernet.generate_key()
conn.sendall(key)
enc = Fernet(key)
file = open("log.txt", 'a')
file.write("\nKey: " + str(key)[2 : -1] + "\n")
file.close()

# keep track of the number of incoming messages
message_ID = 0

# check for incoming messages
while True:
    try:     
        # receive message
        enc_msg = conn.recv(PORT)
        if not enc_msg:
            break
        
        # log message ID
        file = open("log.txt", 'a')
        file.write("\nMessage ID: " + str(message_ID))
        file.close()
        message_ID += 1
        
        # decrypt message
        data = enc.decrypt(enc_msg)
        
        # check if message has been modified
        try:
            # separate message and 512-bit cryptographic hash value
            message = data
            hash_value = message[0 : int(512/8)]
            message = message[int(512/8) : ]
            
            # test has value
            h = hashes.Hash(hashes.SHA512(), backend=default_backend())
            h.update(message)
            test_hash_value = h.finalize()
            
            # check if has values match
            if (test_hash_value != hash_value):
                print ("Incorrect hash value.")
                file = open("log.txt", 'a')
                file.write("\nIncorrect hash value.")
                file.close()                
                hacked()
            
            # log the has value
            file = open("log.txt", 'a')
            file.write("\nHash value: " + str(hash_value)[2 : -1])
            file.close()
        
        # a possible error such as an array-out-of-bounds error indicates the message has been tampered with
        except:
            hacked()
        
        # display message
        print(str(message)[2 : -1])
        file = open("log.txt", 'a')
        file.write("\nMessage text: " + str(message)[2 : -1] + "\n")
        file.close()
    
    # end program if there is an exception
    except Exception:
        print ("An error occurred.")
        break