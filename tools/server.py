# Needs to be run with sudo

import cv2
import numpy as np
from flask import Flask, Response

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/img')
def serve_image():
    img = np.zeros((512, 512, 3), np.uint8)
    cv2.circle(img, (256, 256), 50, (0, 255, 0), -1)

    _, buffer = cv2.imencode('.jpg', img)
    jpg_as_text = buffer.tobytes()

    response = Response(jpg_as_text, content_type='image/jpeg')
    return response

app.run(host='0.0.0.0', port=81)