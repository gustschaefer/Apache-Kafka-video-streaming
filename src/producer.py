import sys
import time
import cv2
from kafka import KafkaProducer

import base64

topic = "distributed-video1"

def publish_video(video_file):
    """
    Publish given video file to a specified Kafka topic. 
    Kafka Server is expected to be running on the localhost. Not partitioned.
    """

    # Start up producer
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    # Open file
    video = cv2.VideoCapture(video_file)
    
    print('publishing video...')

    count = 0;
    while(video.isOpened()):
        success, frame = video.read()

        # Ensure file was read successfully
        if not success:
            print("bad read!")
            break
        
        # Convert image to png
        ret, buffer = cv2.imencode('.jpg', frame)
        #buffer = cv2.cvtColor(buffer, cv2.COLOR_BGR2RGB)

        base64_encoded_data = base64.b64encode(buffer)
        base64_frame = base64_encoded_data.decode('utf-8')

        b64 = base64.b64encode(buffer)

        # Convert to bytes and send to kafka
        producer.send(topic, b64)

        time.sleep(0.1) # 1 second delay
    video.release()
    print('publish complete')

    
def publish_camera():

    # Start up producer
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    
    camera = cv2.VideoCapture(0)
    try:
        while(True):
            success, frame = camera.read()
        
            ret, buffer = cv2.imencode('.jpg', frame)
            producer.send(topic, buffer.tobytes())
            
            # Choppier stream, reduced load on processor
            time.sleep(0.2)

    except:
        print("\nExiting.")
        sys.exit(1)

    
    camera.release()


if __name__ == '__main__':
    """
    Producer will publish to Kafka Server a video file given as a system arg. 
    Otherwise it will default by streaming webcam feed.
    """
    if(len(sys.argv) > 1):
        video_path = sys.argv[1]
        publish_video(video_path)
    else:
        print("publishing feed!")
        publish_camera() 