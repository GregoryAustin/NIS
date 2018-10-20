# NIS Assignment 2018

# David Jones - JNSDAV026
# Gregory Austin - ASTGRE002
# Joshua Abraham - ABRJOS005
# Matthew Young - YNGMAT005


# imports
import socket
import select
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
        print("here")
        
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
        
        # add timestamp
        current_time = datetime.datetime.now()
        msg = str(current_time) + msg
        
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

        # wait for confirmation of receival
        while(True):
            # resend message if no confirmation received after 10 seconds
            if(datetime.datetime.now() > current_time + timedelta(seconds = 10)):
                print("No confirmation received from the server. Resending message.")
                s.sendall(msg_enc)
                current_time = datetime.datetime.now()

            # only listen for 2 seconds at a time to receive a confirmation
            s.setblocking(0)
            ready = select.select([s], [], [], 2)
            if ready[0]:
                received = s.recv(PORT)     # receive the hash back from server to confirm message was received
                if not received:
                    break
                received = enc.decrypt(received)
                if(received != hash_value):
                    print("Wrong confirmation was received. Connection may be comprimised.")
                break
            print("Waiting for receival confirmation from server....")

        print("Your message was successfully received by the server.\n")

