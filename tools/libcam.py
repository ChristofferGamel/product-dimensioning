import time, libcamera
from picamera2 import Picamera2, Preview

picam = Picamera2()



config = picam.create_preview_configuration(main={"size": (1920, 1080)})
config["transform"] = libcamera.Transform(hflip=0, vflip=0)
picam.configure(config)
picam.start_preview(Preview.QTGL)
picam.start()
time.sleep(2)
picam.capture_file("test-python.jpg")

picam.close()