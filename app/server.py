import cv2
import numpy as np
from flask import Flask, Response
from multithreading import ThreadManager
import main

tm = ThreadManager(2)
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

#@app.route('/img')
#def serve_image():
#    img = np.zeros((512, 512, 3), np.uint8)
#    cv2.circle(img, (256, 256), 50, (0, 255, 0), -1)
#
#    _, buffer = cv2.imencode('.jpg', img)
#    jpg_as_text = buffer.tobytes()
#
#    response = Response(jpg_as_text, content_type='image/jpeg')
#    return response

@app.route('/get-dimensions/<input>')
def serve_dimensions(input):
    print("Input: ",input)
    width, depth, height = main.Mask()

@app.route('/<input>')
def serve_input(input):
    output = tm.start_task(input)
    print(output)
    return output

app.run(host='0.0.0.0', port=5000)
