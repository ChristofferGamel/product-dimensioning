from picamera import PiCamera
import time

class Picture():
    def __init__(self):
        self.camera = PiCamera()
        self.source = "/home/chris/Desktop/coding/autostoreHelpers/captured_images/right.jpg"
        self.capture()
        
    def capture(self):
        time.sleep(2)
        self.camera.capture(self.source)
        print("Done.")

if __name__ == "__main__":
    app = Picture()
