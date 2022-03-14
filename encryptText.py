from Crypto.Cipher import AES
from hashlib import sha256

#sudo pip install pycryptodome


def encrypt(text_to_excrypt, password):  #the text to encrypt is a string(utf-8)
    plaintext = bytes(text_to_excrypt, 'utf-8')
    key = sha256(password.encode()).digest()
    key = key[0:32]
    cipher = AES.new(key, AES.MODE_EAX)

    ciphertext, tag = cipher.encrypt_and_digest(plaintext)
    nonce = cipher.nonce
    return (ciphertext, tag, nonce)

def decrypt(ciphertext, tag, nonce, password):
    key = (sha256(password.encode()).digest())
    key = key[0:32]
    cipher = AES.new(key, AES.MODE_EAX, nonce = nonce)
    decrypted_text = cipher.decrypt(ciphertext)
    decrypted_text = decrypted_text.decode('utf-8')
    try:
        cipher.verify(tag)
        return decrypted_text
    except ValueError:
        return None


password = "This is a random password!"
testCipherText, testTag, testNonce = encrypt("Let's try this out for a random longggggg string!!!",  password)

print(f"The decrypted text is: {decrypt(testCipherText, testTag, testNonce, password)}")