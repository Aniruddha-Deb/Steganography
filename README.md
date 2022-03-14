# Steganography

## Project Proposal

Steganography in images using Least Significant Bit is an area of research in data encryption wherein data (or a message) is hidden in images such that the changes made to the images are inconspicuous to the human eye. Through LSB steganography, the LSB of the red, green and blue values of each pixel are replaced with data bits. The process of steganography mainly involves two steps: firstly the secret message is encrypted with a password and embedded into the image in a specific pattern, and is then decoded by a program with knowledge of that pattern, given the password.

We propose to implement a steganography program which can embed text data inside an image: we plan to support password-protected encryption and decryption of both uncompressed images (BMP) and lossless compressed images (PNG, limited to 24 bit RGB and 32 bit RGBA),

## What is LSB steganography?

LSB steganography is used to hide data while preventing third parties to identify that data has been hidden. It involves hiding the messages are hidden inside an image by replacing the least significant bit of each pixel. 
The mesages are first converted into binary values using the corresponding ASCII values which then replace the least significant bits. 

## Method Followed

The method that we've used is as follows:
### Encryption

1. Encryption of message: Using the secret message and password(which is known only to the sender and receiver of the message), the encrypted text is obtained. 
Encrpted_text= F(password, secret_message)
The function used here is based on AES-256. 
AES is based on substitution-permutation network. It uses a fixed block size of 128 bits and a key size of 256 bits. 

2. Now, the encrypted text is hidden into the image using an encoding function. 
# EXPLAIN ENCODING FUNCTION

At this stage, the modified image with the encrypted text can be sent. 
As can be observed, the difference between the original and modified image is so subtle that it can't be observed by the human eye. 


### Decryption

Given the modified image containing the message and the password, the secret message is extracted from the image!

Message= F(image, password)

## Practical Application
LSB steganography has several applications such as Online transactions and military communication. 

## Acknowledgements


## TODO

- [X] Basic PoI 
- [ ] Modularize and think of overall library architecture (classes, files etc)
- [ ] Encrypting data before embedding (aes-256)
- [ ] Solidify for 24 bit and 32 bit PNG's
- [ ] Check whether change in image colour is noticeable
- [ ] Implement for uncompressed BMP 
- [ ] ? GUI
