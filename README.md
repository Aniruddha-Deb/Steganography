# Steganography

## Project Proposal

Steganography in images using Least Significant Bit is an area of research in data encryption wherein data (or a message) is hidden in images such that the changes made to the images are inconspicuous to the human eye. Through LSB steganography, the LSB of the red, green and blue values of each pixel are replaced with data bits. The process of steganography mainly involves two steps: firstly the secret message is encrypted with a password and embedded into the image in a specific pattern, and is then decoded by a program with knowledge of that pattern, given the password.

We propose to implement a steganography program which can embed text data inside an image: we plan to support password-protected encryption and decryption of both uncompressed images (BMP) and lossless compressed images (PNG, limited to 24 bit RGB and 32 bit RGBA),

## TODO

- [X] Basic PoI 
- [ ] Modularize and think of overall library architecture (classes, files etc)
- [ ] Encrypting data before embedding (aes-256)
- [ ] Solidify for 24 bit and 32 bit PNG's
- [ ] Check whether change in image colour is noticeable
- [ ] Implement for uncompressed BMP 
- [ ] ? GUI
