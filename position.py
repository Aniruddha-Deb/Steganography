#sudo pip install pycryptodome


from Crypto.Cipher import AES
from hashlib import sha256

def position(password, index, range):
    sha1= sha256(password+index)
    print(sha1[0:range])
    rgb= sha1[63] %3
    return (sha1[0:range], rgb)


