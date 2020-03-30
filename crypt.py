from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import base64

# Generate a key on startup
key = RSA.importKey(base64.b64decode(input("RSA key: ")))
cipher = PKCS1_OAEP.new(key)

print(base64.b64encode(cipher.encrypt(input("Argument: ").encode())).decode())
