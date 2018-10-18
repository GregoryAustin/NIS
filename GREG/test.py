
from base64 import (
    b64encode,
    b64decode,
)

from Crypto.Hash import SHA256
from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
import utility 
from Crypto import Random


message = utility.generate_nonce()

# Read shared key from file
private_key = False
random_generator = Random.new().read
key = RSA.generate(2048, random_generator) #generate pub and priv key

# Load private key and sign message
signer = PKCS1_v1_5.new(key)
sig = signer.sign(message)

# Load public key and verify message
verifier = PKCS1_v1_5.new(key.publickey())
verified = verifier.verify(message, sig)
assert verified, 'Signature verification failed'
print ('Successfully verified message')