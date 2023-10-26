import cv2
import numpy as np
from flask import Flask, Response
from multithreading import ThreadManager
from main import Mask

tm = ThreadManager(2)
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/get-dimensions/<input>')
def serve_dimensions(input):
    print("Calculating for: ",input)
    #dict = Mask().triangulate(input)
    pictures = take_pictures(input)
    dict = process_images(pictures)
    return dict

def take_pictures():
    pictures_dict = Mask().take_pictures()
    return pictures_dict

def process_images(pictures):
    result = Mask().triangulate(pictures)
    return result

if __name__ == '__main__':
    app.run(threaded=True)
