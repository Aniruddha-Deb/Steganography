# works only on 24-bit PNG images at the moment, need to make more robust

from PIL import Image

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

# encode("tgwok.png", "hello this is a test", "encr.png")
# print(decode("encr.png",20))
