#sudo pip install pycryptodome


from Crypto.Cipher import AES
from hashlib import sha256
import numpy as np

def all_positions(password, totpixels, length):
    positions = []
    for i in range(length):
        positions.append(position(password,i,totpixels))
    return positions

def position(password, totpixels, length):
    sha1 = sha256(f"{password}".encode()).digest()
    permutation = np.random.RandomState(seed=int.from_bytes(sha1[0:3], byteorder='big')).permutation(totpixels-(256+16))
    positions = []
    for i in range(length):
        positions.append((permutation[i],permutation[i]%3))
    return positions

print(position("password", 65536, 12))
