#!/usr/bin/env python
# works only on 24-bit PNG images at the moment, need to make more robust

from PIL import Image
import os, sys

helptext = """
steganography.py
encrypting/decrypting text with a password into an image

Usage:
./steganography.py encode <imagefile> <password>
./steganography.py decode <imagefile> <password>

both options take input from/output to stdin/stdout respectively, so if you want
to encrypt text stored in a file to an image, use redirection:

./steganography.py encode <imagefile> <password> < <textfile>

Similarly for decoding:

./steganography.py decode <imagefile> <password> < <textfile>

Authors: Aniruddha Deb, Riya Sawhney, Tanish Gupta
"""

def encode(source, str_to_encode, target):
	img = Image.open(source)
	data = img.load()
	strbytes = bytes(str_to_encode.encode())

	for i in range(len(strbytes)):
		for j in range(8):
			k = ((1<<j) & strbytes[i])>>j
			r,g,b = data[i,j]
			data[i,j] = (r,g,((b&0xFE)|k))

	img.save(target)

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

def main():
    print(helptext)

if __name__ == "__main__":
    main()

# encode("tgwok.png", "hello this is a test", "encr.png")
# print(decode("encr.png",20))
