# NIS Assignment 2018

# David Jones - JNSDAV026
# Gregory Austin - ASTGRE002
# Joshua Abraham - ABRJOS005
# Matthew Young - YNGMAT005


# imports
import sys
import socket
import datetime
from datetime import timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# if a security measure fails
def hacked(attack):
    print ("Warning, you may have been hacked.")
    print ("Potential " + attack + " attack.")
    file = open("log.txt", 'a')
    file.write("\nWarning, you may have been hacked.")
    file.write("\nPotential " + attack + " attack.")
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
file.write(str(PORT))
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
file.write("\nKey: " + key.decode() + "\n")
file.close()

# keep track of the number of incoming messages
message_ID = 0

# most recent timestamp
current_time = datetime.datetime.now()

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
        
        # check if message hash been modified
        try:
            # separate message and 512-bit cryptographic hash value
            message = data
            hash_value = message[0 : int(512/8)]
            message = message[int(512/8) : ]
            
            # test hash value
            h = hashes.Hash(hashes.SHA512(), backend=default_backend())
            h.update(message)
            test_hash_value = h.finalize()
            
            # check if hash values match
            if (test_hash_value != hash_value):
                print ("Incorrect hash value.")
                file = open("log.txt", 'a')
                file.write("\nIncorrect hash value.")
                file.close()                
                hacked("modification")
            
            # log the hash value
            file = open("log.txt", 'a')
            file.write("\nHash value: " + str(hash_value)[2 : -1])
            file.close()
            
            # check for relay attack
            timestamp = datetime.datetime.strptime(message[:26].decode(), '%Y-%m-%d %H:%M:%S.%f')
            message = message[26:]
            
            # log the timestamp
            file = open("log.txt", 'a')
            file.write("\nTimestamp: " + str(timestamp))
            file.close()
            
            # if the timestamp is older than the most recent timestamp - possible attack
            print(current_time)
            if (current_time - timestamp >= timedelta(microseconds = 0)):
                hacked("replay")
            else:
                current_time = timestamp
            
            # if the timestamp is older than 3 seconds - possible attack
            if (datetime.datetime.now() - timestamp > timedelta(microseconds = 3000000)):
                hacked("replay")
        
        # a possible error such as an array-out-of-bounds error indicates the message has been tampered with
        except:
            hacked("modification")
        
        # display message
        print(message.decode())

        # let client know the message was received
        conn.sendall(enc.encrypt(hash_value))

        # log the message
        file = open("log.txt", 'a')
        file.write("\nMessage text: " + message.decode() + "\n")
        file.close()
    
    # end program if there is an exception
    except Exception:
        print ("An error occurred.")
        break  