# NIS Assignment 2018

# David Jones - JNSDAV026
# Gregory Austin - ASTGRE002
# Joshua Abraham - ABRJOS005
# Matthew Young - YNGMAT005


# imports
import os
import sys
import shutil
import socket
import datetime
from datetime import timedelta
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

# socket variables
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 1024         # Port to listen on (non-privileged ports are > 1023)

# if a security measure fails
def hacked(attack):
    print ("Warning, you may have been hacked.")
    print ("Potential " + attack + " attack.")
    with os.fdopen(os.open(LOG_FILE, FLAG, PERM), 'a') as fout:
        fout.write("\nWarning, you may have been hacked.")
        fout.write("\nPotential " + attack + " attack.")

# program title
print ("\nServer\n")

# create server and look for an empty port
while (True):
    try:
        # try create a socket using current port number
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((HOST, PORT))
        # create new port file once available port is found
        file = open('port', 'w')
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

# client connected
print("Connected: " + str(addr))

# create the log file
LOG_FILE = datetime.datetime.now().strftime("%Y %m %d %H %M %S %f").replace(' ', '') + '.log'
FLAG = os.O_WRONLY | os.O_CREAT     # read write only | create if doesnt exist
PERM = 0o644                        # u:rw g:r o:r
with os.fdopen(os.open(LOG_FILE, FLAG, PERM), 'w') as fout:
    fout.write("\nConnected: " + str(addr) + "\n")
print("Logging messages in: " + LOG_FILE + "\n")

# generate and send encryption key to client
key = Fernet.generate_key()
conn.sendall(key)
enc = Fernet(key)
with os.fdopen(os.open(LOG_FILE, FLAG, PERM), 'a') as fout:
    fout.write("\nKey: " + key.decode() + "\n")

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
        with os.fdopen(os.open(LOG_FILE, FLAG, PERM), 'a') as fout:
            fout.write("\nMessage ID: " + str(message_ID))
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
                with os.fdopen(os.open(LOG_FILE, FLAG, PERM), 'a') as fout:
                    fout.write("\nIncorrect hash value.")
                hacked("modification")
            
            # log the hash value
            with os.fdopen(os.open(LOG_FILE, FLAG, PERM), 'a') as fout:
                fout.write("\nHash value: " + str(hash_value)[2 : -1])
            
            # check for relay attack
            timestamp = datetime.datetime.strptime(message[:26].decode(), '%Y-%m-%d %H:%M:%S.%f')
            message = message[26:]
            
            # log the timestamp
            with os.fdopen(os.open(LOG_FILE, FLAG, PERM), 'a') as fout:
                fout.write("\nTimestamp: " + str(timestamp))
            
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
        with os.fdopen(os.open(LOG_FILE, FLAG, PERM), 'a') as fout:
            fout.write("\nMessage text: " + message.decode() + "\n")
    
    # end program if there is an exception
    except Exception:
        print ("An error occurred.")
        break

# move the log file to the log folder
if not os.path.exists("logs"):
    os.makedirs("logs")
shutil.move(LOG_FILE, "logs/" + LOG_FILE)