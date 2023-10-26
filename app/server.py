import cv2
import numpy as np
from flask import Flask, Response
from main import Mask
import queue
import threading
import time

# Queues
awaiting_picture = queue.Queue()
awaiting_processing = queue.Queue()

camera_lock = threading.Lock() # Prevents overlapping picture taking
picture_taking_in_progress = False

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get-dimensions/<input>')
def serve_dimensions(input):
    print("Calculating for: ",input)
    awaiting_picture.put(input)


    pictures = picture_loop()
    # pictures = take_pictures()
    dict = process_images(pictures)
    return dict

def picture_loop():
    global picture_taking_in_progress

    if not picture_taking_in_progress:
        with camera_lock:
            picture_taking_in_progress = True
            input = awaiting_picture.get()
            pictures = take_pictures(input)
            awaiting_picture.task_done()
            awaiting_processing.put(pictures)
            picture_taking_in_progress = False
            return pictures
    else:
        print("Picture lock")
        time.sleep(0.3)
        picture_loop()
        

def take_pictures(id):
    pictures_dict = Mask().take_pictures(id)
    return pictures_dict

def process_images(pictures):
    while not awaiting_processing.empty():
        pictures = awaiting_processing.get()
        result = Mask().triangulate(pictures)
        awaiting_processing.task_done()
        return result

if __name__ == '__main__':
    app.run(threaded=True)
