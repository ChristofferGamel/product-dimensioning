import cv2
import numpy as np
from flask import Flask, Response, make_response
from main import Mask
import queue
import threading
import time

# Queues
awaiting_picture = queue.Queue()
awaiting_processing = queue.Queue()

camera_lock = threading.Lock() # Prevents overlapping picture taking
picture_taking_in_progress = False
processing_in_progress = False

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get-dimensions/<input>')
def serve_dimensions(input):
    print("Calculating for: ",input)
    awaiting_picture.put(input)
    # To handle the possibility of a camera failure / contouring failure
#    try:
    pictures = picture_loop()
    dict = process_images(pictures)
    return dict
#    except Exception as e:
#        print(e)
#        return make_response(str(e), 503)


def picture_loop():
    global picture_taking_in_progress

    if not picture_taking_in_progress:
        with camera_lock:
            try:
                picture_taking_in_progress = True
                input = awaiting_picture.get()
                pictures = take_pictures(input)
                awaiting_processing.put(pictures)
                return pictures
            finally:
                awaiting_picture.task_done()
                picture_taking_in_progress = False

    else:
        print("Picture lock")
        time.sleep(0.3)
        picture_loop()
    

def take_pictures(id):
    pictures_dict = Mask().take_pictures(id)
    return pictures_dict

def process_images(pictures):
    global processing_in_progress

    while not awaiting_processing.empty():
        if not processing_in_progress:
            try:
                processing_in_progress = True
                pictures = awaiting_processing.get()
                result = Mask().triangulate(pictures)
                return result
            finally:
                processing_in_progress = False
                awaiting_processing.task_done()
        else:
            time.sleep(1.3)
            print("processing lock")
            process_images(pictures)
        

if __name__ == '__main__':
    app.run(threaded=True)
