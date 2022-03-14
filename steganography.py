#!/usr/bin/env python
# works only on 24-bit PNG images at the moment, need to make more robust

from PIL import Image
import os, sys
from Crypto.Cipher import AES
from hashlib import sha256

helptext = """
steganography.py
encrypting/decrypting text with a password into an image

Usage:
./steganography.py encode <input_image> <password> <output_image>
./steganography.py decode <input_image> <password>

both options take input from/output to stdin/stdout respectively, so if you want
to encrypt text stored in a file to an image, use redirection:

./steganography.py encode <input_image> <password> <output_image> < <textfile>

Similarly for decoding:

./steganography.py decode <imagefile> <password> < <textfile>

Authors: Aniruddha Deb, Riya Sawhney, Tanish Gupta
"""

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

def write_lsb(data, color, lsb, pos, w):
    t = data[pos//w,pos%w]
    a = [n for n in t]
    a[color] = (a[color]|lsb)
    data[pos//w,pos%w] = tuple(a)

def encode(input_img, password, text, output_img):
    print(f"encoding image, {password}, {text}")

    # hash and encode text - tanish
    # encoding function - riya
    # encoding function gives us a sequence of pixel values from a lower bound
    # to 256. Different encoding algorithms are used for different image types
    # with diff specifics, but the fundamentals are the same: encode the n bits
    # one pixel at a time and one colour at a time, provided by the encoding
    # function
    #
    (ciphertext, tag, nonce) = encrypt(text, password)
    # enc_positions = [(a_1,c_1), (a_2,c_2), ... , (a_n, c_n)]

    print(input_img.format)
    if (input_img.format != "PNG"):
        raise ValueError("Input file is not a PNG image")
    if (input_img.size < (256, 256)):
        raise ValueError("Input Image is too small to encrypt")

    data = input_img.load()
    # encode text length in round robin manner (RGBRGB...) in first 16 pixels
    len_enc = len(ciphertext)
    for i in range(16):
        write_lsb(data,i%3,((1<<i)&len_enc)>>i,i,input_img.size[0])

    bitarray = []

    for i in range(len(ciphertext)):
        for j in range(8):
            bitarray.append(((1<<j) & ciphertext[i])>>j)

    # print bitarray for now
    print(bitarray)

    # write bitarray to image
    #for i in range(len(bitarray)):
        
        

def decode(source, len_to_decode):
	simg = Image.open(source)
	data = simg.load()
	strbytes = bytearray()

	for i in range(len_to_decode):
		t = 0
		for j in range(8):
			r,g,b = data[i,j]
			t = t | ((b&0x01)<<j)
		strbytes.extend([t])
	
	return strbytes.decode()

def arg_error():
    print("Argument Error: incomplete or incorrect arguments. Exiting.")
    print(helptext)   

def main():

    print(sys.argv)

    # rudimentary argument parsing
    if (len(sys.argv) < 4):
        print("Argument Error: Too few or incomplete arguments")
        print(helptext)
    elif (sys.argv[1] == "encode"):
        if len(sys.argv) < 5:
            print("Argument Error: Too few or incomplete arguments")
            print(helptext)
            return

        # accept text
        input_str = sys.stdin.read()
        try:
            img = Image.open(sys.argv[2])
            encode(img, sys.argv[3], input_str, sys.argv[4])
        except Exception as e:
            print("An error occured while encoding:")
            print(e)

    elif (sys.argv[1] == "decode"):
        print("decoding")
    else:
        arg_error()

if __name__ == "__main__":
    main()

# encode("tgwok.png", "hello this is a test", "encr.png")
# print(decode("encr.png",20))
