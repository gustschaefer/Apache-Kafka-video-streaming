#import pymongo
from pymongo import MongoClient
import numpy as np
import base64
from PIL import Image
import cv2
import io

client = MongoClient("localhost",27017)
db = client["bigdata"]
col = db["face"]

# function to return value for any key (k) in dict
def get_val(k, dict): 
	for key, value in dict.items(): 
		if k == key: 
			return value 

	return "value doesn't exist"

def decode_img(encoded):
	str_img = base64.b64decode(encoded)
	numpy_img = np.array(Image.open(io.BytesIO(str_img)))

	return numpy_img

''' structure of an element
{
	"face": b64_img,
	"frame": frame,
	"boundingbox": boundingbox_coords,
	"timestamp": timestamp
}
'''

# find one element
res = col.find_one({"frame": 71})

# find all elements
print("all images containing faces: ")
for res in col.find():
  print(get_val("frame", res))
  #print(res)

# manipulate single image
img_raw = get_val("face", res) # image taken from db (base64 format)
frame = get_val("frame", res)  # frame of img_raw

img_decoded = decode_img(img_raw) # convert img_raw (base64) to numpy array
print("\nthen: {} \nnow: {}".format(type(img_raw), type(img_decoded)))

name = "frame{}".format(frame)
cv2.imshow(name, img_decoded)
cv2.waitKey(0)
  
