import time
from picamera2 import Picamera2

# Create a camera object for the specific camera
picam = Picamera2(camera_num=1)  # 0 for the first camera, 1 for the second camera, and so on

controls = {"ExposureTime": 1600, 
                    "AnalogueGain": 1.2, 
                    "Brightness": 0.08,
                    "Sharpness":3,
                    "AwbMode":5
                    }
config = picam.create_preview_configuration(main={"size": (2304, 1296)}, controls=controls)
picam.configure(config)

time.sleep(2)
picam.start()
time.sleep(2)

picam.capture_file("test.jpg")

picam.close()