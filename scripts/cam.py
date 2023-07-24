from picamera import PiCamera
import time
camera = PiCamera()
time.sleep(2)
camera.capture("/home/chris/Desktop/coding/autostoreHelpers/pik.jpg")
print("Done.")
