import time, libcamera
from picamera2 import Picamera2, Preview

picam = Picamera2()
# picam.create_preview_configuration()
config = picam.create_preview_configuration(main={"size": (1920, 1080)}, controls={"ExposureTime": 2000, "AnalogueGain": 1.0})
#config2 = picam.set_controls({"ExposureTime": 10000, "AnalogueGain": 1.0})
picam.configure(config)
#picam.configure(config2)
#picam.start_preview(Preview.QTGL)

# Set ISO and shutter speed settings
# picam.iso = 160  # Set the desired ISO value
# picam.shutter_speed = 100  # Set the desired shutter speed in microseconds

# Allow sensor to stabilize with new settings
# picam.exposure_mode = 'off'
time.sleep(2)

picam.start()
time.sleep(2)

# Capture the image with specific settings
picam.capture_file("test-python2.jpg")

picam.close()



