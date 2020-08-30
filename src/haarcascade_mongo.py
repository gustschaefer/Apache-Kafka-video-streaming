import numpy as np
import cv2
import time
import os
from pymongo import MongoClient

client = MongoClient("localhost",27017)
db = client["bigdata"]
col = db["face"]

# read in the cascade classifier for face
face_cascade = cv2.CascadeClassifier('./haarcascade_frontalface_default.xml') 

# check face
def is_face(img):

	face_rect = face_cascade.detectMultiScale(img, 
											scaleFactor = 1.2, 
											minNeighbors = 5) 

	if np.size(face_rect) > 0: # face was detected
		return True

	return False



# create a function to detect face 
def haarcascade_frontalface(img): 
	
	face_img = img.copy() 
	
	face_rect = face_cascade.detectMultiScale(face_img, 
											scaleFactor = 1.2, 
											minNeighbors = 5) 
	
	for (x0, y0, w, h) in face_rect: 
		x1, y1 = x0 + w, y0 + h
		cv2.rectangle(face_img, (x0, y0), (x1, y1), (0, 0, 255), 3)

	return face_img, [(x0, y0), (x1, y1)]

# save image in mongodb
def save_mongo(b64_img, frame, boundingbox_coords, timestamp):

	timeStr = time.ctime()

	res = col.insert_one(
		{
	  	 "face": b64_img,
	     "frame": frame,
	     "boundingbox": boundingbox_coords,
	     "timestamp": timestamp
  		}
	)

# save image in folder
def save_folder(boundingboxed_face, frame, boundingbox_coords, timestamp, folder):

	name = "face{} - {} - {}.jpg".format(frame, boundingbox_coords, timestamp)
	cv2.imwrite(os.path.join(folder, name), boundingboxed_face)


img = cv2.imread("../test_face.jpg")
cpy = img.copy()
marked, bb = haarcascade_frontalface(cpy)
save_folder(marked, 0, bb, time.ctime(), "../not_face")
cv2.imshow("face", marked)
cv2.waitKey(0)
