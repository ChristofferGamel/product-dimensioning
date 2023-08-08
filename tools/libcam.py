import time, libcamera
from picamera2 import Picamera2, Preview

picam = Picamera2()
# picam.create_preview_configuration()
controls = {"ExposureTime": 1400, 
            "AnalogueGain": 1.0, 
            "Brightness": 0,
            "Sharpness":2,
            "AwbMode":5
            }
config = picam.create_preview_configuration(main={"size": (2304, 1296)}, controls=controls)
#config2 = picam.set_controls({"ExposureTime": 10000, "AnalogueGain": 1.0})
picam.configure(config)
time.sleep(2)

picam.start()
time.sleep(2)

# Capture the image with specific settings
picam.capture_file("test-python3.jpg")

picam.close()



