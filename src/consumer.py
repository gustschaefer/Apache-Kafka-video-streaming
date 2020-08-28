import datetime
from flask import Flask, Response
from kafka import KafkaConsumer

import base64
from PIL import Image
import cv2
import io
import numpy as np
import os
import time

import haar_cascades as hc

# Set the Kafka Consumer
topic = "distributed-video1"

consumer = KafkaConsumer(
    topic, 
    bootstrap_servers=['localhost:9092'])


# Set the consumer in a Flask App
app = Flask(__name__)

@app.route('/video', methods=['GET'])
def video():
    """
    Set the mimetype to multipart/x-mixed-replace. 
    Flask replace any old images with new values streaming through the pipeline.
    """
    return Response(
        get_video_stream(), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

def get_video_stream():
    """
    Recieve streamed images from the Kafka Server and convert 
    to Flask-readable format.
    """
    frame = 0
    for msg in consumer:
        str_frame = base64.b64decode(msg.value) # decode base64 image
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + str_frame + b'\r\n\r\n')

        img_decoded = np.array(Image.open(io.BytesIO(str_frame))) # convert decoded base64 image to numpy array

        if hc.is_face(img_decoded): # a face was detected

            timestamp = time.ctime() # get timestamp when an image is detected
            marked_face, boundingbox_coords = hc.haarcascade_frontalface(img_decoded) # get the boundingboxed face and boundingbox coordinates

            hc.save_mongo(msg.value, frame, boundingbox_coords, timestamp) # save image in mongodb (b64 img, frame, bb coords, timestamp)

            hc.save_folder(marked_face, frame, boundingbox_coords, timestamp,'../faces') # save image in folder (same as above)

            print("face detected!")

        else:
            folder = '../not_face'
            frame_name = "not_face{}.jpg".format(frame)
            cv2.imwrite(os.path.join(folder, frame_name), img_decoded)

        print(frame)
        if frame == 0: 
            print("Types - encoded: {}\ndecoded: {}".format(type(str_frame), # print type of the first frame
                                                type(img_decoded)))
        frame +=1 # next frame


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)