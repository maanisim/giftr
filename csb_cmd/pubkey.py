from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import base64

# Generate a key on startup
key = RSA.generate(2048)

def get_pubkey():
  return base64.b64encode(key.publickey().exportKey('DER')).decode()

def decrypt(message):
  cipher = PKCS1_OAEP.new(key)
  return cipher.decrypt(base64.b64decode(message)).decode()
