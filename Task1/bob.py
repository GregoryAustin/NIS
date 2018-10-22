import socket
import utility 
import Crypto
from Crypto.PublicKey import RSA
from Crypto import Random
import ast
import math
import hashlib
import json
import sys

from base64 import (
    b64encode,
    b64decode,
)

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5

# CREATING PUBLIC PRIVATE KEYS AND SAVING THE PUBLIC KEY TO A FILE 
random_generator = Random.new().read
key = RSA.generate(2048, random_generator) #generate pub and priv key

binKey = key.publickey().exportKey('PEM') # exporting public key 

with open ("publicB.pem", "w") as prv_file:
    print("{}".format(binKey.decode()), file=prv_file) # exporting public key 



# get the hostname
host = socket.gethostname()
port = 5001  # initiate port no above 1024

server_socket = socket.socket()  # get instance
# look closely. The bind() function takes tuple as argument
server_socket.bind((host, port))  # bind host address and port together

# configure how many client the server can listen simultaneously
server_socket.listen(1)
conn, address = server_socket.accept()  # accept new connection
print("Connection from: " + str(address))

# getting Alice's key because she sent us a .pem file with it 
file = open("publicA.pem", "rb")
pkey = file.read()

publickey = RSA.importKey(pkey)
nonce = utility.generate_nonce()

secretkey = ''
# symmetric key distribution using assymetric 
while True: 
    data = conn.recv(2048).decode()
    data = data.replace("\r\n", '')

    decrypted = key.decrypt(ast.literal_eval(data)).decode('utf-8')
    print ("Recieved decrypted message: ", decrypted)

    jsonData = json.loads(decrypted)

    if 'ID' in jsonData and 'nonce' in jsonData:
        print("Recieved request for symmetric key from: " + str(jsonData["ID"]) + " nonce=" + str(jsonData["nonce"]))

        x = {
              "nonce1": jsonData["nonce"],
              "nonce2": nonce
            }
        msg = json.dumps(x)

        encryptedMsg = publickey.encrypt(msg.encode('utf-8'), 32) 
        print("Sending: ", msg)
        conn.send(str(encryptedMsg).encode()) # send message
    elif 'nonce2' in jsonData:
        if jsonData['nonce2'] == str(nonce):
            print("Nonce is same as the nonce I sent")

            msg = "ack"
            encryptedMsg = publickey.encrypt(msg.encode('utf-8'), 32) 
            print("Sending: ", msg)
            conn.send(str(encryptedMsg).encode()) # send message

            data = conn.recv(2048).decode() # receive response from Bob
            data = data.replace("\r\n", '')
            decrypted = key.decrypt(ast.literal_eval(data))
            
            # decrypted = (key.decrypt(ast.literal_eval(data))).decode()

            sig = decrypted 
            print ("Recieved signature... ") 
            print ("Recieved", b64encode(sig))
            print(len(str(decrypted)))
            msg = "ack"
            encryptedMsg = publickey.encrypt(msg.encode('utf-8'), 32) 
            print("Sending: ", msg)
            conn.send(str(encryptedMsg).encode()) # send message
            
            data = conn.recv(2048).decode() # receive response from Bob
            data = data.replace("\r\n", '')

            decrypted = key.decrypt(ast.literal_eval(data)).decode()
            # decrypted = (key.decrypt(ast.literal_eval(data))).decode()

            secretkey = decrypted 

            verified = utility.verify(secretkey.encode(), sig, publickey)

            if (verified):
                print ("WE BOTH HAVE THE SECRET KEY")
                print ("The secretkey: ", secretkey); 
                break;
            else: 
                print("Not verified!!!")
                sys.exit()
            
            # decrypted = 


        else:
            print("Nonce is not the same, this is noncesense!")
            print("Quitting at once!")
            sys.exit()



# while True:
#     # receive data stream. it won't accept data packet greater than 1024 bytes
#     data = conn.recv(2048).decode()
#     data = data.replace("\r\n", '')

#     # data = data.replace("encrypted_message=", '')


#     if not data:
#         # if data is not received break
#         break

#     # Decrypting using this private key (Bob)
#     decrypted = key.decrypt(ast.literal_eval(data)).decode('utf-8')
#     print("from connected user: " + str(decrypted))
#     data = input(' -> ')

#     # Encrypt using Alice's public key 
#     encryptedMsg = publickey.encrypt(data.encode('utf-8'), 32)

#     # send data to Bob client
#     conn.send(str(encryptedMsg).encode()) 

# conn.close()  # close the connection