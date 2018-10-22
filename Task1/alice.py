# NIS Assignment 2018

# David Jones - JNSDAV026
# Gregory Austin - ASTGRE002
# Joshua Abraham - ABRJOS005
# Matthew Young - YNGMAT005


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

# this is done by alice and she is exporting her public key 
with open ("publicA.pem", "w") as prv_file:
    print("{}".format(binKey.decode()), file=prv_file)  # exporting public key 

# getting bob's key because he sent us a .pem file with it 
file = open("publicB.pem", "rb")
pkey = file.read()

publickey = RSA.importKey(pkey)


host = socket.gethostname()  # as both code is running on same pc
port = 5001  # socket server port number

client_socket = socket.socket()  # instantiate
client_socket.connect((host, port))  # connect to the server

# symmetric key distribution using assymetric key (RSA) 
x = {
      "ID": "Alice",
      "nonce": utility.generate_nonce()
    }

msg = json.dumps(x)

encryptedMsg = publickey.encrypt(msg.encode('utf-8'), 32) 
print("Sending: ", msg)
client_socket.send(str(encryptedMsg).encode()) # send message

privateKey = ''
secretkey = utility.generate_nonce(); 

while True:
    data = client_socket.recv(2048).decode() # receive response from Bob
    data = data.replace("\r\n", '')

    decrypted = key.decrypt(ast.literal_eval(data)).decode('utf-8')
    # print (decrypted)
    print ("Recieved decrypted message: ", decrypted)

    jsonData = json.loads(decrypted)

    

    if 'nonce1' in jsonData and 'nonce2' in jsonData: 
        if jsonData["nonce1"] == x["nonce"]:
            print("Nonce is same as the nonce I sent")
            x = {
                  "nonce2": jsonData["nonce2"]
                }

            msg = json.dumps(x)

            encryptedMsg = publickey.encrypt(msg.encode('utf-8'), 32) 
            print("Sending: ", msg)
            client_socket.send(str(encryptedMsg).encode()) # send message


            data = client_socket.recv(2048).decode() # receive response from Bob
            data = data.replace("\r\n", '')

            decrypted = key.decrypt(ast.literal_eval(data)).decode('utf-8')

            if (decrypted == 'ack'):
                print ("Recieved acknowledgement")
                
                # digest = SHA128.new()
                # digest.update(secretkey.encode())

                # signer = PKCS1_v1_5.new(key)
                # sig = b64encode(signer.sign(digest))

                sig = utility.sign(secretkey.encode(), key, "SHA-1" )
                encryptedMsg = publickey.encrypt(sig, 32) 
                print("Sending: ", b64encode(sig))
                print(len(str(sig)))
                client_socket.send(str(encryptedMsg).encode()) # send message

                data = client_socket.recv(2048).decode() # receive response from Bob
                data = data.replace("\r\n", '')

                decrypted = key.decrypt(ast.literal_eval(data)).decode('utf-8')

                if (decrypted == 'ack'):
                    print ("Recieved acknowledgement")
                    encryptedMsg = publickey.encrypt(secretkey.encode(), 32) 

                    print("Sending: ", str(secretkey))
                    client_socket.send(str(encryptedMsg).encode()) # send message
                    break;
                else:
                    print("No acknowledgement... quitting.")
                    sys.exit()


            else:
                print("No acknowledgement... quitting.")
                sys.exit()


            
        else:
            print("Nonce is not the same, this is noncesense!")
            print("Quitting at once!")
            sys.exit()

    print("\n")


# message = input(" -> ")  # take input

# while message.lower().strip() != 'bye':
#     # encrypt message using Bob's public key 
#     encryptedMsg = publickey.encrypt(message.encode('utf-8'), 32) 

#     client_socket.send(str(encryptedMsg).encode()) # send message
#     data = client_socket.recv(2048).decode() # receive response from Bob
#     data = data.replace("\r\n", '')

#     # decyrypt using my private key (Alice)
#     decrypted = key.decrypt(ast.literal_eval(data)).decode('utf-8')
#     print('Received from server: ' + str(decrypted))  # show in terminal

#     message = input(" -> ")  # again take input

# client_socket.close()  # close the connection