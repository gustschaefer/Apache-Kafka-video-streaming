import datetime
from flask import Flask, Response
from kafka import KafkaConsumer

import base64
from PIL import Image
import cv2
import io
import numpy as np

# Fire up the Kafka Consumer
topic = "distributed-video1"

consumer = KafkaConsumer(
    topic, 
    bootstrap_servers=['localhost:9092'])


# Set the consumer in a Flask App
app = Flask(__name__)

@app.route('/video', methods=['GET'])
def video():
    """
    This is the heart of our video display. Notice we set the mimetype to 
    multipart/x-mixed-replace. This tells Flask to replace any old images with 
    new values streaming through the pipeline.
    """
    return Response(
        get_video_stream(), 
        mimetype='multipart/x-mixed-replace; boundary=frame')

def get_video_stream():
    """
    Here is where we recieve streamed images from the Kafka Server and convert 
    them to a Flask-readable format.
    """
    count = 0
    for msg in consumer:
        str_frame = base64.b64decode(msg.value)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpg\r\n\r\n' + str_frame + b'\r\n\r\n')

        img_decoded = np.array(Image.open(io.BytesIO(str_frame)))
        cv2.imwrite("./frames/frame%d.jpg" % count, img_decoded)
        
        if count == 0: 
            print("encoded: {}\ndecoded: {}".format(type(str_frame), 
                                                type(img_decoded)))
        count +=1


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)