#!/usr/bin/env python
# works only on 24-bit PNG images at the moment, need to make more robust

from PIL import Image
import os, sys
import numpy as np
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

def decrypt(ciphertext, nonce, password):
    key = (sha256(password.encode()).digest())
    key = key[0:32]
    cipher = AES.new(key, AES.MODE_EAX, nonce = nonce)
    decrypted_text = cipher.decrypt(ciphertext)
    decrypted_text = decrypted_text.decode('utf-8')
    return decrypted_text
    # try:
    #     cipher.verify(tag)
    #     return decrypted_text
    # except ValueError:
    #     return None

def write_lsb(data, color, lsb, pos, w):
    t = data[(pos%w),(pos//w)]
    a = [n for n in t]
    a[color] = ((a[color]&0xFE)|lsb)
    data[pos%w,pos//w] = tuple(a)

def read_lsb(data, color, pos, w):
    t = data[pos%w,pos//w]
    a = [n for n in t]
    return (a[color]&0x01)

def get_enc_positions(password, totpixels, length):
    sha1 = sha256(f"{password}".encode()).digest()
    permutation = np.random.RandomState(seed=int.from_bytes(sha1[0:3], byteorder='big')).permutation(totpixels-(256+16))
    positions = []
    for i in range(length):
        positions.append((int(permutation[i])+(256+16),permutation[i]%3))
    return positions

def encode(input_img, password, text, output_img):

    # hash and encode text - tanish
    # encoding function - riya
    # encoding function gives us a sequence of pixel values from a lower bound
    # to 256. Different encoding algorithms are used for different image types
    # with diff specifics, but the fundamentals are the same: encode the n bits
    # one pixel at a time and one colour at a time, provided by the encoding
    # function
    #
    (ciphertext, tag, nonce) = encrypt(text, password)

    if (input_img.format != "PNG") and (input_img.format != "BMP"):
        raise ValueError("Input file is not a PNG or BMP image")
    if (input_img.mode != "RGB") and (input_img.mode != "RGBA"):
        raise ValueError("Input Color Mode is not compatiable")
    if (input_img.size < (128,128)):
        raise ValueError("Input Image is too small to encrypt (need > 128x128)")

    data = input_img.load()
    # encode text length in round robin manner (RGBRGB...) in first 16 pixels
    len_enc = len(ciphertext)
    for i in range(16):
        write_lsb(data,0,((1<<i)&len_enc)>>i,i,input_img.size[0])
    for i in range(16):
        for j in range(8):
            write_lsb(data,0,((1<<j)&nonce[i])>>j,(i+2)*8+j,input_img.size[0])

    bitarray = []

    for i in range(len(ciphertext)):
        for j in range(8):
            bitarray.append(((1<<j) & ciphertext[i])>>j)

    enc_positions = get_enc_positions(password, input_img.size[0]*input_img.size[1], len(bitarray))

    for i in range(len(bitarray)):
        (pos,color) = enc_positions[i]
        write_lsb(data, color, bitarray[i], pos, input_img.size[0])

    # print bitarray for now
    # print(bitarray)
    input_img.save(output_img)

    # write bitarray to image
    #for i in range(len(bitarray)):

def decode(input_img, password):

    if (input_img.format != "PNG") and (input_img.format != "BMP"):
        raise ValueError("Input file is not a PNG or BMP image")
    if (input_img.mode != "RGB") and (input_img.mode != "RGBA"):
        raise ValueError("Input Color Mode is not compatiable")
    if (input_img.size < (128, 128)):
        raise ValueError("Input Image is too small to encrypt")

    data = input_img.load()
    strbytes = bytearray()

    # get length of string to decode
    len_to_decode = 0
    for i in range(16):
        lsb = read_lsb(data, 0, i, input_img.size[0])
        len_to_decode = len_to_decode | (lsb<<i)

    print(len_to_decode)

    # get nonce encoded in image
    nonce = bytearray()
    for i in range(16):
        t = 0
        for j in range(8):
            pos = (i+2)*8+j
            b = read_lsb(data,0,pos,input_img.size[0])
            t = t | (b<<j)
        nonce.extend([t])

    # get encryption map from password
    enc_positions = get_enc_positions(password, input_img.size[0]*input_img.size[1], len_to_decode*8)

    for i in range(len_to_decode):
        t = 0
        for j in range(8):
            (pos, color) = enc_positions[i*8+j]
            b = read_lsb(data,color,pos,input_img.size[0])
            t = t | (b<<j)
        strbytes.extend([t])

    return decrypt(strbytes, nonce, password)

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
        try:
            img = Image.open(sys.argv[2])
            text = decode(img, sys.argv[3])
            print(text)
        except Exception as e:
            print("An error occured while decoding:")
            print(e)
    else:
        arg_error()

if __name__ == "__main__":
    main()

# encode("tgwok.png", "hello this is a test", "encr.png")
# print(decode("encr.png",20))
